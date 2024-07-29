import sys
import smtplib
import getpass

class EmailUtils:
    conn: None
    username: str | None = None
    password: str | None = None
    sender: str = "do-not-reply@iwa.onfortify.com"

    def __init__(self, server_name, server_port=587, username="", password=""):
        self.username = username
        self.password = password
        EmailUtils.conn = smtplib.SMTP(server_name, server_port)

    def send(self, receiver, message): # this is an instance method
        print("sending email to {} message: {}".format(self.name, self.message))
        EmailUtils.conn.ehlo()
        EmailUtils.conn.starttls()
        EmailUtils.conn.login(self.username, self.password)
        EmailUtils.conn.sendmail(self.sender, receiver, message)
        EmailUtils.conn.quit()




