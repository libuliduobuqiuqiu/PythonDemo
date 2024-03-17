# coding: utf-8
"""
    :Author: linshukai
    :Descrption: About Smtp Client
    :Date: 2024-3-15
"""


from email.header import Header
from email.mime.text import MIMEText
import smtplib


class SmtpClient:
    def __init__(
        self, smtp_server: str, smtp_port: int, email_username: str, email_password: str
    ):
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.email_username = email_username
        self.email_password = email_password

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

    def connect(self):
        self.server = smtplib.SMTP_SSL(self.smtp_server, self.smtp_port)
        self.server.set_debuglevel(1)
        self.server.login(self.email_username, self.email_password)

    def close(self):
        if hasattr(self, "server"):
            self.server.quit()

    def send_msg(self, from_addr: str, to_addr: str, subject: str, content: str):
        msg = MIMEText(content, "plain", "utf-8")
        msg["From"] = from_addr
        msg["To"] = to_addr
        msg["Subject"] = Header(subject, "utf-8").encode()

        if not hasattr(self, "server"):
            raise Exception("Smtp Server not connected. Please check the code.")

        self.server.sendmail(from_addr, [to_addr], msg.as_string())
