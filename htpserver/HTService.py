import logging
import time
from logging.handlers import SysLogHandler

from service import Service, find_syslog

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

    def run(self):
        log_format = '[%(asctime)s] [%(levelname)-5s] %(message)s'
        date_format = '%Y-%m-%d %H:%M:%S'
        logfile = self.working_dir + '/service.log'
        log_level = logging.INFO
        logging.basicConfig(filename=logfile, level=log_level, format=log_format, datefmt=date_format)
        logging.getLogger().addHandler(logging.StreamHandler())

        self.database = HTDatabase(self.working_dir)
        while not self.got_sigterm():
            logging.info("I'm working...")
            time.sleep(5)