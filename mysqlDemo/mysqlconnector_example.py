# -*- coding: utf-8 -*-

from mysql.connector import cursor
from setting import HOST, USERNAME, PASSWORD
import mysql.connector


if __name__ == "__main__":
    conn = mysql.connector.connect(
        host=HOST,
        user=USERNAME,
        password=PASSWORD,
        database='test'
    )
    cursor = conn.cursor()
    sql = "select * from user where user_name = '林树楷'"
    cursor.execute(sql)
    data = cursor.fetchall()
    print(data)