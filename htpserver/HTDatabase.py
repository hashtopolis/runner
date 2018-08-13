import logging
import os
import re

import mysql.connector


class HTDatabase:

    def __init__(self, working_dir):
        # Search the DB settings for Hashtopolis
        path = working_dir + "/../db.php"
        self.db = None
        if not os.path.exists(path):
            logging.error("DB connection file of Hashtopolis is not present!")
            return
        with open(path) as f:
            content = f.read().splitlines()

        self.user = ""
        self.password = ""
        self.host = ""
        self.db = ""
        self.port = 3306

        for line in content:
            if line.find("CONN['user']") != -1:
                m = re.search('= \'(.*?)\';', line)
                self.user = m.group(1)
            if line.find("CONN['pass']") != -1:
                m = re.search('= \'(.*?)\';', line)
                self.password = m.group(1)
            if line.find("CONN['server']") != -1:
                m = re.search('= \'(.*?)\';', line)
                self.host = m.group(1)
            if line.find("CONN['db']") != -1:
                m = re.search('= \'(.*?)\';', line)
                self.db = m.group(1)
            if line.find("CONN['port']") != -1:
                m = re.search('= \'(.*?)\';', line)
                self.port = int(m.group(1))

        self.db = mysql.connector.connect(host=self.host, user=self.user, passwd=self.password, port=self.port)
