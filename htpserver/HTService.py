import logging
import subprocess
import time
from logging.handlers import SysLogHandler

from service import Service, find_syslog

from htpserver.Config import Config
from htpserver.HTDatabase import HTDatabase


class HTService(Service):
    def __init__(self, *args, **kwargs):
        self.working_dir = ""
        if 'working_directory' in kwargs:
            self.working_dir = str(kwargs['working_directory'])
            del kwargs['working_directory']
        super(HTService, self).__init__(*args, **kwargs)

        # Use syslog for catching fatal problems which are not logged otherwise
        self.logger.addHandler(SysLogHandler(address=find_syslog(), facility=SysLogHandler.LOG_DAEMON))
        self.logger.setLevel(logging.WARN)

        self.database = None
        self.config = None

    def run(self):
        log_format = '[%(asctime)s] [%(levelname)-5s] %(message)s'
        date_format = '%Y-%m-%d %H:%M:%S'
        logfile = self.working_dir + '/service.log'
        log_level = logging.INFO
        logging.basicConfig(filename=logfile, level=log_level, format=log_format, datefmt=date_format)
        logging.getLogger().addHandler(logging.StreamHandler())

        try:
            self.database = HTDatabase(self.working_dir)
            self.config = Config(self.database)
        except RuntimeError:
            return  # abort if there are problems

        while not self.got_sigterm():
            entries = self.database.get_file_entries()
            logging.info("Retrieved " + str(len(entries)) + " file download entries.")

            for file_download in entries:
                file = self.database.get_file(file_download['fileId'])

                # Build command
                # ./uftp -z -I <interface> -Ctfmcc / -R <rate> <file>
                cmd = self.working_dir + "/uftp -z -I "
                if self.config.get_value('serviceInterface'):
                    cmd += str(self.config.get_value('serviceInterface')) + ' '
                else:
                    cmd += "eth0 "  # just if we are lucky it's eth0
                if self.config.get_value('serviceTransmissionRateEnabled') and self.config.get_value('serviceTransmissionRate'):
                    cmd += "-R " + str(self.config.get_value('serviceTransmissionRate')) + ' '
                else:
                    cmd += "-Ctfmcc "  # flow-control enabled (default)
                cmd += self.working_dir + "/../files/" + file['filename']
                logging.debug("CALL: " + cmd)
                process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                process.wait()
                output, err = process.communicate()

                status = 1
                for line in err:
                    logging.error("Error from UFTP: " + line)
                    status = -1

                # parse output and check if all completed successfully
                for line in output:
                    # TODO: parse
                    pass

                self.database.update_entry(status, file['fileId'])
            time.sleep(5)
