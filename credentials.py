import getpass
import os


class Credentials(object):
    CONFIG = 'config.cfg'

    def __init__(self):
        self.name = ''
        self.user = ''
        self.password = ''

        self.try_load_config()
        self.load_missing_params()

    def set_params(self, name, user_email, password):
        self.name = name
        self.user = user_email
        self.password = password

    def load_missing_params(self):
        if self.name == '':
            self.name = 'temporary'
        if self.user == '':
            self.user = 'temporary_email_account'
        if self.password == '':
            self.password = getpass.getpass(prompt='Enter GMail password: ')

    @staticmethod
    def config_exists():
        return os.access(Credentials.CONFIG, os.R_OK)

    def try_load_config(self):
        if self.config_exists():
            print 'Found config file'
            pass
