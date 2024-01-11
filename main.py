# coding: utf-8
"""
    :date: 2023-12-19
    :author: linshukai
    :description: PythonDemo Main.py to setup script
"""

from StorageDemo.mysqlDemo.pymysql_example import (
    count_table_rows,
    count_table_datetime_fields,
)


if __name__ == "__main__":
    # count_table_rows()
    results = count_table_datetime_fields()
    for table, fields in results.items():
        print(table, fields)
