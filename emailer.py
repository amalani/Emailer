import smtplib
from email.mime.text import MIMEText
from credentials import Credentials


class Message(object):
    def __init__(self, mail_from='', subject='', body=''):
        self.mail_from = mail_from
        self.to = []
        self.cc = []
        self.bcc = []
        self.subject = subject
        self.body = body

    def add_to(self, email):
        self.to.append(email)

    def add_cc(self, email):
        self.cc.append(email)

    def get_recipients(self):
        recipients = self.to
        recipients.extend(self.cc)
        recipients.extend(self.bcc)
        return recipients

    def get_message(self):
        assert len(self.to) > 0
        assert self.subject != ''
        assert self.body != ''
        assert self.mail_from != ''

        message = MIMEText(self.body)
        message['Subject'] = self.subject
        message['From'] = self.mail_from
        message['To'] = ', '.join(self.to)
        if len(self.cc) > 0:
            message['Cc'] = ', '.join(self.cc)
        return message.as_string()


class EmailSender(object):

    def __init__(self, credentials):
        self.server = None
        self.credentials = credentials
        self.email_from = self.credentials.email

    def connect(self):
        if self.server is None:
            try:
                self.server = smtplib.SMTP_SSL('smtp.gmail.com')
                self.server.ehlo()
                self.server.login(self.credentials.user, self.credentials.password)
            except Exception as e:
                print e

    def disconnect(self):
        if self.server:
            self.server.close()

    def sendmail(self, message):
        result = self.server.sendmail(
            message.mail_from,
            message.get_recipients(),
            message.get_message())
        print result
        return result




credentials = Credentials()

# m = Message(credentials.name, 'subject', 'body text\n lets see if this works')
# m.add_to('to@email.com')

#
# email_sender = EmailSender(credentials)
# email_sender.connect()
# email_sender.sendmail(m)
# email_sender.disconnect()
