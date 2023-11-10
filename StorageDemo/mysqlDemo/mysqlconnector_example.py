# -*- coding: utf-8 -*-

from mysql.connector import cursor
from setting import AliyunSetting
import mysql.connector

if __name__ == "__main__":
    conn = mysql.connector.connect(
        host=AliyunSetting.HOST,
        user=AliyunSetting.USERNAME,
        password=AliyunSetting.PASSWORD,
        database='test'
    )
    cursor = conn.cursor()
    sql = "select * from user where user_name = 'mbb'"
    cursor.execute(sql)
    data = cursor.fetchall()
    print(data)
