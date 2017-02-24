import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from credentials import Credentials

# http://stackoverflow.com/questions/882712/sending-html-email-using-python

class Message(object):
    def __init__(self, mail_from='', subject='', body=''):
        self.mail_from = mail_from
        self.to = []
        self.cc = []
        self.bcc = []
        self.subject = subject
        self.body = body
        self.is_html_email = False
        self.body_html = ''

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

        if not self.is_html_email:
            message = MIMEText(self.body)
        else:
            # HTML Email
            message = MIMEMultipart('alternative')
            part1 = MIMEText(self.body, 'plain')
            part2 = MIMEText(self.body_html, 'html')
            message.attach(part1)
            message.attach(part2)

        message['From'] = self.mail_from
        message['Subject'] = self.subject
        message['To'] = ', '.join(self.to)
        if len(self.cc) > 0:
            message['Cc'] = ', '.join(self.cc)

        return message.as_string()


    def set_html_content(self, content):
        self.body_html = content
        self.is_html_email = True


class EmailSender(object):

    def __init__(self, user_creds):
        # type: (Credentials) -> None
        self.server = None
        self.credentials = user_creds
        self.email_from = self.credentials.get_property('email')

    def connect(self):
        if self.server is None:
            try:
                self.server = smtplib.SMTP_SSL('smtp.gmail.com')
                self.server.ehlo()
                self.server.login(self.credentials.get_property('email'),
                                  self.credentials.get_property('password'))
            except Exception as e:
                print e

    def disconnect(self):
        if self.server:
            self.server.close()

    def send_mail(self, message):
        result = self.server.sendmail(
            message.mail_from,
            message.get_recipients(),
            message.get_message())
        print result
        return result


credentials = Credentials()

# Load settings, and save config file
# credentials.get_setting_from_user()
# credentials.save_config()

# print
# credentials.show()
# m = Message(credentials.get_property('name'), 'test subject', 'body text\n lets see if this works')
# m.add_to('testuser@mailinator.com')

# email_sender = EmailSender(credentials)
# email_sender.connect()
# email_sender.send_mail(m)
# email_sender.disconnect()
