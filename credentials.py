import getpass
import os

import ConfigParser


class Credentials(object):
    DEFAULT_CONFIG = 'config.cfg'

    SETTINGS_PLAIN_TEXT = ['name', 'email']
    SETTINGS_ENCRYPTED = ['password']

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
            if settings[key] == '':
                value = raw_input('Enter {}'.format(key))
                self.settings[key] = value

        for key in self.SETTINGS_ENCRYPTED:
            if settings[key] == '':
                value = getpass.getpass('Enter {}'.format(key))
                self.settings[key] = value

    def config_exists(self):
        return os.access(self.config_file, os.R_OK)

    def try_load_config(self):
        if self.config_exists():
            print "Found config file."
        else:
            print "Config file missing."


