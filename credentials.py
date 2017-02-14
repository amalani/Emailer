import getpass
import os
import json
import ConfigParser

from config import ConfigHelper

class Credentials(object):
    '''
    Basic credential/config storage. Allows encrypting/decrypting sensitive data using a key.
    '''
    DEFAULT_CONFIG = 'config.cfg'

    # key is the secret key used to encrypt/decrypt the password. All other keys are optional.
    SECRET_KEY_NAME = 'key'
    SETTINGS_PLAIN_TEXT = [SECRET_KEY_NAME, 'name', 'email']
    SETTINGS_ENCRYPTED = ['password']

    CONFIG_SECTION_NAME = 'configuration'

    def __init__(self, config_file=''):
        assert self.SECRET_KEY_NAME in self.SETTINGS_PLAIN_TEXT, "secret key required"
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
            self._load_config()
        else:
            print "Config file missing."

    def _load_config(self):
        config_helper = ConfigHelper(self.config_file)
        config_helper.read()
        config = config_helper.config
        for key in self.SETTINGS_PLAIN_TEXT:
            try:
                value = config.get(self.CONFIG_SECTION_NAME, key)
            except ConfigParser.NoOptionError:
                print "'{}' not found in config file.".format(key)
                value = ''
            self.settings[key] = value

        for key in self.SETTINGS_ENCRYPTED:
            try:
                value = config.get(self.CONFIG_SECTION_NAME, key)
            except ConfigParser.NoOptionError:
                print "'{}' not found in config file.".format(key)
                value = ''
            self.settings[key] = value

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