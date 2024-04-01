# coding: utf-8
"""
    :Author: linshukai
    :Description: Test SMTP Client
    :Date: 2024-3-13
"""

from unittest import TestCase
import sys

sys.path.insert(0, "/data/PythonDemo/")

from demo.ops.smtp_demo.smtp_client import SmtpClient

# from demo.setting import PersonalMailSetting as mail
from demo.setting import CompanyMailSetting as mail


class TestSmtpClient(TestCase):
    def test_send_mail(self):
        with SmtpClient(
            mail.SMTP_SERVER, mail.SMTP_PORT, mail.SMTP_USERNAME, mail.SMTP_PASSWORD
        ) as client:
            client.send_msg(mail.FROM_ADDR, mail.TO_ADDR, "SMTP TEST", "hello,world")
