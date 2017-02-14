import getpass
import json
import os
from base64 import b64encode, b64decode

import ConfigParser
from Crypto.Cipher import AES

from config import ConfigHelper

class SimpleEncryption(object):
    # based on http://www.codekoala.com/posts/aes-encryption-python-using-pycrypto/
    # Note: this code is good for simple projects, but not for actual production use.
    BLOCK_SIZE = 16
    PADDING = '{'

    @staticmethod
    def pad(s):
        return s + (SimpleEncryption.BLOCK_SIZE - len(s) % SimpleEncryption.BLOCK_SIZE) * SimpleEncryption.PADDING

    # one-liners to encrypt/encode and decrypt/decode a string
    # encrypt with AES, encode with base64
    @staticmethod
    def encode(c, s):
        return b64encode(c.encrypt(SimpleEncryption.pad(s)))

    @staticmethod
    def decode(c, e):
        return c.decrypt(b64decode(e)).rstrip(SimpleEncryption.PADDING)

    @staticmethod
    def get_cipher(key):
        return AES.new(key)

    @staticmethod
    def generate_key():
        return os.urandom(SimpleEncryption.BLOCK_SIZE)


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
        self._settings = {}
        self._init_settings()
        self._dirty = False

        if config_file != '':
            self.config_file = config_file
        self.try_load_config()

        # We always keep the key base 64 encoded.
        if self.secret_key == '':
            self._settings[self.SECRET_KEY_NAME] = b64encode(SimpleEncryption.generate_key())

    @property
    def secret_key(self):
        return b64decode(self._settings[self.SECRET_KEY_NAME])

    def get_property(self, key):
        return self._settings[key]

    def _init_settings(self):
        for key in self.SETTINGS_PLAIN_TEXT:
            self._settings[key] = ''
        for key in self.SETTINGS_ENCRYPTED:
            self._settings[key] = ''

    def get_setting_from_user(self):
        for key in self.SETTINGS_PLAIN_TEXT:
            if self._settings[key] == '':
                value = raw_input('Enter {}: '.format(key))
                self._settings[key] = value
                self._dirty = True

        for key in self.SETTINGS_ENCRYPTED:
            if self._settings[key] == '':
                value = getpass.getpass('Enter {}: '.format(key))
                self._settings[key] = value
                self._dirty = True

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
            self._settings[key] = value

        cipher = SimpleEncryption.get_cipher(self.secret_key)
        for key in self.SETTINGS_ENCRYPTED:
            try:
                value = config.get(self.CONFIG_SECTION_NAME, key)
                value = SimpleEncryption.decode(cipher, value)
            except ConfigParser.NoOptionError:
                print "'{}' not found in config file.".format(key)
                value = ''
            self._settings[key] = value

    def save_config(self):
        config_helper = ConfigHelper(self.config_file)
        config = config_helper.config
        config.add_section(self.CONFIG_SECTION_NAME)

        for key in self.SETTINGS_PLAIN_TEXT:
            config.set(self.CONFIG_SECTION_NAME, key, self._settings[key])

        cipher = SimpleEncryption.get_cipher(self.secret_key)
        for key in self.SETTINGS_ENCRYPTED:
            value = self._settings[key]
            value = SimpleEncryption.encode(cipher, value)
            config.set(self.CONFIG_SECTION_NAME, key, value)
        config_helper.save()

    def show(self):
        print "Showing config: <encrypted values hidden>"
        settings = self._settings.copy()
        for key in self.SETTINGS_ENCRYPTED:
            settings[key] = '<encrypted value, hidden>'
        print json.dumps(settings, indent=2, sort_keys=True)