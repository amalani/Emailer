import os
from configparser import ConfigParser


class ConfigHelper(object):
    def __init__(self, filename):
        self.config = ConfigParser()
        self.file = filename

    def config_exists(self):
        return os.access(self.file, os.R_OK)

    def save(self):
        with open(self.file, 'wb') as config_file:
            self.config.write(config_file)

    def read(self):
        if self.config_exists():
            self.config.read(self.file)
        else:
            print("config not found")


# config = ConfigParser.ConfigParser({}, collections.OrderedDict)
# config.read('testfile.ini')
# # Order the content of each section alphabetically
# for section in config._sections:
#     config._sections[section] = collections.OrderedDict(sorted(config._sections[section].items(), key=lambda t: t[0]))

# # Order all sections alphabetically
# config._sections = collections.OrderedDict(sorted(config._sections.items(), key=lambda t: t[0] ))

# # Write ini file to standard output
# config.write(sys.stdout)