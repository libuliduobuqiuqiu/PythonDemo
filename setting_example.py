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


class AliyunSetting(MysqlSetting):
    pass


class CompanySetting(MysqlSetting):
    pass
