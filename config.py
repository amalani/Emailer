import getpass


class Credentials(object):
    def __init__(self, name, user_email):
        self.name = name
        self.user = user_email
        self.password = getpass.getpass(prompt='Enter GMail password: ')
