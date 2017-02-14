import ConfigParser


class Configuration(object):
    def __init__(self, filename):
        self.config = ConfigParser.RawConfigParser()
        self.file = filename

    def config_exists(self):
        return os.access(self.file, os.R_OK)