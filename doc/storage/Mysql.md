## Python Mysql驱动
- mysql-connector-python（MYSQL官方纯Python驱动）
> pip install mysql-connector-python<br>
import mysql.connector

- MySQL-python(封装MYSQL C驱动的Python驱动，不支持Python3)
> pip install MySQL-python<br>
import MySQLdb

- mysqlclient（mysqlclient 完全兼容MySQLdb，同时支持python3）
> pip install mysqlclient<br>
import MySQLdb

- PyMySQL
> pip install PyMySQL<br>
import pymysql


## 操作示例

mysql.connector
```python
#!/usr/bin/python
# -*- coding: utf-8 -*-

import mysql.connector
import json


if __name__ == "__main__":
    user = "root"
    password = "root"
    database = "music"
    host = "127.0.0.1"
    conn = mysql.connector.connect(host=host, user=user, password=password,
                                   database=database, charset='utf8')
    cursor = conn.cursor(dictionary=True)

    # 更新/插入/删除
    try:
        sql = "delete from music_music where id=149"
        cursor.execute(sql)

        u_sql = "update music_music set music_author=%s, music_name=%s where id=147"
        data = ("liubei", "sanguo")
        cursor.execute(u_sql, data)
        conn.commit()
    except Exception as e:
        conn.rollback()
        print(str(e))

    # 查询
    try:
        sql = "select * from music_music"
        cursor.execute(sql)
        query_data = cursor.fetchall()
        print(json.dumps(query_data, indent=2, ensure_ascii=False))
    except Exception as e:
        print(str(e))
```

pymysql
```python
import pymysql

# Connect to the database
connection = pymysql.connect(host='localhost',
                             user='user',
                             password='passwd',
                             database='db',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

with connection:
    with connection.cursor() as cursor:
        # Create a new record
        sql = "INSERT INTO `users` (`email`, `password`) VALUES (%s, %s)"
        cursor.execute(sql, ('webmaster@python.org', 'very-secret'))

    # connection is not autocommit by default. So you must commit to save
    # your changes.
    connection.commit()

    with connection.cursor() as cursor:
        # Read a single record
        sql = "SELECT `id`, `password` FROM `users` WHERE `email`=%s"
        cursor.execute(sql, ('webmaster@python.org',))
        result = cursor.fetchone()
        print(result)
````

## 备注：
> SQLAlchemy是一个ORM框架，并不提供底层的数据库操作，本质是借助MySQLdb和PyMySQL来完成数据库操作。常见于各种Web框架中。

参考：
> https://juejin.cn/post/6844903824356802573
> https://pymysql.readthedocs.io/en/latest/user/examples.html#
