# coding: utf-8
"""
    :date: 2023-11-10
    :author: linshuaki
    :description: About Pymysql Example. how to use pymysql lib.
"""

from setting import MysqlSetting
import pymysql
import pymysql.cursors


class MysqlClient:
    def __init__(self, setting: MysqlSetting, db_name: str):
        self.setting = setting
        self.db_name = db_name

    def __enter__(self):
        self.connect = pymysql.connect(
            host=self.setting.HOST,
            user=self.setting.USERNAME,
            password=self.setting.PASSWORD,
            port=self.setting.PORT,
            database=self.db_name,
            cursorclass=pymysql.cursors.DictCursor,
        )
        return self.connect

    def __exit__(self, exc_type, exc_value, traceback):
        if hasattr(self, "connect"):
            self.connect.close()


def exec_sql(setting: MysqlSetting, db_name: str, sql_str: str, sql_args: list):
    with MysqlClient(setting, db_name) as connect:
        with connect.cursor() as cursor:
            cursor.execute(sql_str, sql_args)
            result = cursor.fetchall()
            return result
