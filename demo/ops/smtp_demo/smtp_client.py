# coding: utf-8
"""
    :Author: linshukai
    :Descrption: About Smtp Client
    :Date: 2024-3-15
"""


from email.header import Header
from email.mime.text import MIMEText
import smtplib
import sys

sys.path.insert(0, "/data/PythonDemo/")

from setting import CompanyMailSetting as my_mail

# from setting import PMSMailSetting as my_mail


class SmtpClient:
    def __init__(
        self, smtp_server: str, smtp_port: int, email_username: str, email_password: str
    ):
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.email_username = email_username
        self.email_password = email_password

    def __enter__(self):
        self.server = smtplib.SMTP_SSL(self.smtp_server, self.smtp_port)
        self.server.set_debuglevel(1)
        self.server.login(self.email_username, self.email_password)
        return self

    def __exit__(self, exc_type, exc_value, traceback):
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


if __name__ == "__main__":
    with SmtpClient(
        my_mail.SMTP_SERVER,
        my_mail.SMTP_PORT,
        my_mail.SMTP_USERNAME,
        my_mail.SMTP_PASSWORD,
    ) as s:
        print("sending msg...")
        s.send_msg(my_mail.FROM_ADDR, my_mail.TO_ADDR, "test send email", "hello,world")
