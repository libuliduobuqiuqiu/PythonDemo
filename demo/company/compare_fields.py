# coding: utf-8
"""
    :date: 2023-11-15
    :author: linshukai
    :description: Compare Tables Fields
"""

from setting import CompanySetting
from StorageDemo.mysqlDemo.pymysql_example import exec_sql

if __name__ == "__main__":
    db_name = "cmdb"
    ad_fields = []
    sql_str = f"DESCRIBE instance_ad"
    filed_results = exec_sql(CompanySetting(), db_name, sql_str, [])
    for item in filed_results:
        ad_fields.append(item["Field"])

    ad_device_fields = []
    sql_str = f"DESCRIBE instance_ad_device"
    filed_results = exec_sql(CompanySetting(), db_name, sql_str, [])
    for item in filed_results:
        ad_device_fields.append(item["Field"])

    tmp_list1 = [a for a in ad_fields if a not in ad_device_fields]
    print("需要补充：", tmp_list1)
    tmp_list2 = [a for a in ad_device_fields if a not in ad_fields]
    print("缺少的字段：", tmp_list2)
