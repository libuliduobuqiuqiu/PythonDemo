# coding: utf-8
"""
    :date: 2023-11-10
    :author: linshuaki
    :description: About Pymysql Example. how to use pymysql lib.
"""

from setting import CompanySetting, MysqlSetting
import re
import pymysql
import pymysql.cursors
from collections import defaultdict
from CompanyDemo.cmdb_update import get_models


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


def get_tables(name: str = "adops", company_setting=CompanySetting(), prefix=""):
    # Get Table Info

    db_name = "information_schema"
    sql_str = f"select * from tables where TABLE_SCHEMA = %s"
    results = exec_sql(company_setting, db_name, sql_str, [name])

    ad_tables = []
    for item in results:
        table_name = item["TABLE_NAME"]
        if prefix != "":
            if not re.match(prefix, table_name):
                continue

        ad_tables.append(table_name)
    return ad_tables


def count_table_rows():
    # Count Adops table rows
    ad_tables = get_tables()

    for tmp_name in ad_tables:
        db_name = "adops"
        sql_str = f"select count(*) from {tmp_name}"
        results = exec_sql(CompanySetting(), db_name, sql_str, [])
        print(tmp_name, results)


# Count Adops Table's fields about someone type
def count_table_fields(
    ad_tables: list,
    db_name="adops",
    company_setting=CompanySetting(),
    field_type="datetime",
    prefix="",
    max_length=0,
):
    count = 0
    if len(ad_tables) == 0:
        ad_tables = get_tables(
            name=db_name, company_setting=company_setting, prefix=prefix
        )
    fields = defaultdict(list)

    for tmp_name in ad_tables:
        sql_str = f"describe {tmp_name}"
        field_results = exec_sql(company_setting, db_name, sql_str, [])

        for field in field_results:
            # if field["Type"].find("text") > -1 or field["Type"].find("bigint") > -1:
            if field["Type"].find(field_type) > -1:
                # print(tmp_name, field["Field"], field["Type"])
                regex = field_type + r"\((\d+)\)"
                result = re.search(regex, field["Type"])

                if result:
                    length = result.group(1)
                    if int(length) > max_length:
                        fields[tmp_name].append(
                            {"Field": field["Field"], "Type": field["Type"]}
                        )
                        count += 1
                else:
                    fields[tmp_name].append(
                        {"Field": field["Field"], "Type": field["Type"]}
                    )
                    count += 1
    print(f"总计{field_type}类型字段：{count}")
    return fields


# 查看当前表中的索引
def show_table_index(company_setting):
    db_name = "adops"
    ad_tables = get_tables(company_setting=company_setting)

    index_fields = defaultdict(list)

    for tmp_name in ad_tables:
        count = 0
        primary_key = []
        sql = f"show index from {tmp_name}"
        results = exec_sql(company_setting, db_name, sql, [])

        for field in results:
            if field["Key_name"] != "PRIMARY":
                tmp = {
                    "Key_name": field["Key_name"],
                    "Column_name": field["Column_name"],
                }
                index_fields[tmp_name].append(tmp)
            else:
                count += 1
                primary_key.append(field["Column_name"])

        if count > 1:
            print(tmp_name, primary_key)

    return index_fields


def gen_model_datetime_fields():
    # 筛选模型中datetime的字段
    count = 0
    datetime_fields = count_table_datetime_fields([])

    for table, fields in datetime_fields.items():
        table = table.split("instance_")[-1]
        model_info = get_models(table)

        for item in model_info["items"]:
            model_fields = item["fields"]

            for field in model_fields:
                if field["name"] in fields:
                    field["type"] = "timestamp"
                    # update_model_field(field)
                    print(table, field["name"])
                    count += 1


if __name__ == "__main__":
    gen_model_datetime_fields()
