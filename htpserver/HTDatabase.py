import logging
import os
import re

import mysql.connector


# TODO: I know it's a bad thing to use SQL inline, this should definitely be changed to using prepared statements afterwards
class HTDatabase:
    def __init__(self, working_dir):
        # Search the DB settings for Hashtopolis
        path = working_dir + "/../db.php"
        self.db = None
        if not os.path.exists(path):
            logging.error("DB connection file of Hashtopolis is not present!")
            raise RuntimeError()
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

        self.db = mysql.connector.connect(host=self.host, user=self.user, passwd=self.password, port=self.port, database=self.db)
        if not self.db.is_connected():
            logging.error("Connection to Database failed!")
            raise RuntimeError()

    def get_file_entries(self):
        if self.db is None:
            return []
        cur = self.db.cursor(dictionary=True)
        cur.execute("SELECT * FROM FileDownload WHERE status IN (0,-1)")
        return cur.fetchall()

    def get_file(self, file_id):
        if self.db is None:
            return []
        cur = self.db.cursor(dictionary=True)
        cur.execute("SELECT * FROM File WHERE fileId=" + str(int(file_id)))
        return cur.fetchall()[0]

    def update_entry(self, status, file_id):
        if self.db is None:
            return
        cur = self.db.cursor()
        cur.execute("UPDATE FileDownload SET status=" + str(int(status)) + " WHERE fileId=" + str(int(file_id)))

    def get_config(self):
        if self.db is None:
            return []
        cur = self.db.cursor(dictionary=True)
        # we load the config section for the runner
        cur.execute("SELECT * FROM Config WHERE configSectionId=6")
        return cur.fetchall()
