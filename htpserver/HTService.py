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

        logging.info("Starting Hashtopolis service runner v0.1.0...")

        try:
            self.database = HTDatabase(self.working_dir)
            self.config = Config(self.database)
        except RuntimeError:
            return  # abort if there are problems

        while not self.got_sigterm():
            entries = self.database.get_file_entries()
            if entries:
                logging.info("Retrieved " + str(len(entries)) + " file download entries.")

            for file_download in entries:
                db_file = self.database.get_file(file_download['fileId'])

                # Build command
                # ./uftp -z -I <interface> -Ctfmcc / -R <rate> <file>
                cmd = self.working_dir + "/uftp -z -I "
                if self.config.get_value('multicastDevice'):
                    cmd += str(self.config.get_value('multicastDevice')) + ' '
                else:
                    cmd += "eth0 "  # just if we are lucky it's eth0
                if int(self.config.get_value('multicastTransferRateEnable')) == 1 and int(self.config.get_value('multicastTranserRate')) > 0:
                    cmd += "-R " + str(self.config.get_value('multicastTranserRate')) + ' '
                else:
                    cmd += "-Ctfmcc "  # flow-control enabled (default)
                cmd += self.working_dir + "/../../files/" + db_file['filename']
                logging.info("CALL: " + cmd)
                output = []
                try:
                    output = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT)
                except subprocess.CalledProcessError as exc:
                    print("Status : FAIL", exc.returncode, exc.output)
                    logging.error("Error from UFTP: " + str(exc.returncode) + "/" + str(exc.output))

                # parse output and check if all completed successfully
                status = 1
                for line in output:
                    logging.info("UFTP-OUT: " + str(line))
                    if str(line).startswith("Host: "):
                        if str(line).find("Status: Completed") != -1:
                            pass  # good
                        elif str(line).find("Status: Skipped") != -1:
                            pass # good
                        else:
                            # status is not good -> we will need to resend it
                            # TODO: maybe this checks need to be extended to improve checking for errors
                            status = -1

                self.database.update_entry(status, db_file['fileId'])
            time.sleep(5)
