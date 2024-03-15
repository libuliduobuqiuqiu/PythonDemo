# coding: utf-8
"""
    :date: 2024-1-31
    :author: linshukai
    :description: About Count Company's tables index;
"""
import sys

from pymysql import FIELD_TYPE


sys.path.insert(0, "/data/PythonDemo/")

from StorageDemo.mysqlDemo.pymysql_example import (
    exec_sql,
    get_tables,
    show_table_index,
    count_table_fields,
)
from setting import CompanySetting, CompanySetting57, CompanySetting72


# 统计所有表的索引，以及多个主键索引
def print_tables_index():
    company_setting = CompanySetting57()
    fields = show_table_index(company_setting)
    print("-----------Count-------------")

    for k, v in fields.items():
        print("Table: ", k)
        for column in v:
            print("Index: ", v)
        print("-------------------------")


# 统计所有表的datieme类型字段
def print_tables_datetime():
    fields = count_table_fields([], company_setting=CompanySetting57())
    print("-----------Count-------------")

    for k, v in fields.items():
        print("Table: ", k)
        print("Coulumn: ", v)
        print("-------------------------")


# 统计所有表的text类型字段
def print_tables_text():
    fields = count_table_fields(
        [], company_setting=CompanySetting57(), field_type="varchar", max_length=255
    )
    print("-----------Count57-------------")

    for k, v in fields.items():
        print("Table: ", k)
        print("Coulumn: ", v)
        print("-------------------------")
    return fields


def print_72tables_text():
    fields = count_table_fields(
        [],
        company_setting=CompanySetting72(),
        db_name="cmdb",
        field_type="text",
        prefix="instance_ad",
    )
    print("-----------Count72-------------")

    for k, v in fields.items():
        print("Table: ", k)
        print("Coulumn: ", v)
        print("-------------------------")
    return fields


def count_dg_rows(dg_id, sg_id):
    dg_list = []
    sg_list = []
    unkown_list = []

    cmdb_tables = get_tables(name="cmdb")
    for table in cmdb_tables:
        if "instance_ad" in table:
            sql = f"DESCRIBE  {table}"
            result = exec_sql(
                setting=CompanySetting(), db_name="cmdb", sql_str=sql, sql_args=[]
            )
            key_list = [x["Field"] for x in result]

            if "device_group_id" in key_list:
                dg_list.append(table)
                continue

            if "syn_group_id" in key_list:
                sg_list.append(table)
                continue

            unkown_list.append(table)

    print("device_group", dg_list)
    print("syn_grou", sg_list)
    print("unkonw_list", unkown_list)

    for dg in dg_list:
        sql = f"SELECT COUNT(*) FROM {dg} where device_group_id = '{dg_id}'"
        result = exec_sql(
            setting=CompanySetting(), db_name="cmdb", sql_str=sql, sql_args=[]
        )
        print(dg, result)

    for sg in sg_list:
        sql = f"SELECT COUNT(*) FROM {sg} where syn_group_id = '{sg_id}'"
        result = exec_sql(
            setting=CompanySetting(), db_name="cmdb", sql_str=sql, sql_args=[]
        )
        print(sg, result)


if __name__ == "__main__":
    # print_tables_datetime()
    # print_tables_index()

    # tmp_fields = print_72tables_text()
    # fields = print_tables_text()
    #
    # for k, v in tmp_fields.items():
    #     tmp_k = k.split("instance_ad_")
    #     if len(tmp_k) > 1:
    #         k = tmp_k[1]
    #     else:
    #         k = tmp_k[0]
    #     if k not in fields:
    #         print(k, v)
    # count_dg_rows("1750427107516743680", "1750427180791234560")
    print_tables_text()
