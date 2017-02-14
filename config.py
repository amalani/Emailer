import ConfigParser


class ConfigHelper(object):
    def __init__(self, filename):
        self.config = ConfigParser.RawConfigParser()
        self.file = filename

    def config_exists(self):
        return os.access(self.file, os.R_OK)

    def save(self):
        with open(self.file, 'wb') as config_file:
            self.config.write(config_file)