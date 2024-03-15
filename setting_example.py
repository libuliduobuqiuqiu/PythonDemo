# coding: utf-8
"""
    :date: 2023-11-10
    :author: linshukai
    :description: About Setting Demo
"""


class MysqlSetting:
    HOST = ""
    USERNAME = ""
    PORT = 3306
    PASSWORD = ""

    MONGODB_HOST = ""
    MONGODB_USERNAME = ""
    MONGODB_PASSWORD = ""
    MONGODB_PORT = 0


class MailSetting:
    SMTP_SERVER = ""
    SMTP_PORT = 0
    SMTP_USERNAME = ""
    SMTP_PASSWORD = ""
    FROM_ADDR = ""
    TO_ADDR = ""


class AliyunSetting(MysqlSetting):
    pass


class CompanySetting(MysqlSetting):
    pass


class PersonalMailSetting(MailSetting):
    pass


class CompanyMailSetting(MailSetting):
    pass
