import getpass
import os
import json

from config import ConfigHelper

class Credentials(object):
    DEFAULT_CONFIG = 'config.cfg'

    SETTINGS_PLAIN_TEXT = ['name', 'email', 'salt']
    SETTINGS_ENCRYPTED = ['password']

    CONFIG_SECTION_NAME = 'configuration'

    def __init__(self, config_file=''):
        self.config_file = self.DEFAULT_CONFIG
        self.settings = {}
        self._init_settings()

        if config_file != '':
            self.config_file = config_file

        self.try_load_config()

    def _init_settings(self):
        for key in self.SETTINGS_PLAIN_TEXT:
            self.settings[key] = ''
        for key in self.SETTINGS_ENCRYPTED:
            self.settings[key] = ''

    def set_params(self, name, email, password):
        self.settings['name'] = name
        self.settings['email'] = email
        self.settings['password'] = password

    def get_setting_from_user(self):
        for key in self.SETTINGS_PLAIN_TEXT:
            if self.settings[key] == '':
                value = raw_input('Enter {}: '.format(key))
                self.settings[key] = value

        for key in self.SETTINGS_ENCRYPTED:
            if self.settings[key] == '':
                value = getpass.getpass('Enter {}: '.format(key))
                self.settings[key] = value

    def config_exists(self):
        return os.access(self.config_file, os.R_OK)

    def try_load_config(self):
        if self.config_exists():
            print "Found config file."
        else:
            print "Config file missing."

    def save_config(self):
        config_helper = ConfigHelper(self.config_file)
        config = config_helper.config
        config.add_section(self.CONFIG_SECTION_NAME)
        for key in self.SETTINGS_PLAIN_TEXT:
            config.set(self.CONFIG_SECTION_NAME, key, self.settings[key])
        for key in self.SETTINGS_ENCRYPTED:
            config.set(self.CONFIG_SECTION_NAME, key, self.settings[key])
        config_helper.save()

    def show(self):
        print "Config: "
        print json.dumps(self.settings, indent=2, sort_keys=True)