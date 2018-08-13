import logging


class Config:
    config = {}
    database = None

    def __init__(self, db):
        # load from database
        self.database = db
        self.update()

    def update(self):
        entries = self.database.get_config()
        for entry in entries:
            logging.info(str(entry))
            self.__set_value(entry['item'], entry['value'])
        logging.info("Loaded config from server: " + str(self.config))

    def get_value(self, key):
        if key in self.config:
            return self.config[key]
        return ''

    def __set_value(self, key, val):
        self.config[key] = val
