# coding: utf-8
"""
    :date: 2023-11-10
    :author: linshuaki
    :description: About Pymysql Example. how to use pymysql lib.
"""

from setting import MysqlSetting
import pymysql
import pymysql.cursors
from collections import defaultdict
from CompanyDemo.cmdb_update import get_models


class MysqlClient:
    def __init__(self, setting: MysqlSetting, db_name: str):
        self.setting = setting
        self.db_name = db_name

    def __enter__(self):
        self.connect = pymysql.connect(host=self.setting.HOST,
                                       user=self.setting.USERNAME,
                                       password=self.setting.PASSWORD,
                                       port=self.setting.PORT,
                                       database=self.db_name,
                                       cursorclass=pymysql.cursors.DictCursor)
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


def get_table_info():
    # 获取表信息
    from setting import CompanySetting
    count = 0

    db_name = "information_schema"
    sql_str = f"select * from tables where TABLE_SCHEMA = %s"
    results = exec_sql(CompanySetting(), db_name, sql_str, ['adops'])

    ad_tables = []
    for item in results:
        table_name = item["TABLE_NAME"]
        if table_name.find("instance_ad") > -1:
            ad_tables.append(table_name)

    datetime_fields = defaultdict(list)
    for tmp_name in ad_tables:
        db_name = "adops"
        sql_str = f"DESCRIBE {tmp_name}"
        filed_results = exec_sql(CompanySetting(), db_name, sql_str, [])

        for field in filed_results:
            # if field["Type"].find("text") > -1 or field["Type"].find("bigint") > -1:
            if field["Type"].find("datetime") > -1:
                # count_text.append(f"{tmp_name} {field['Field']} {field['Type']}")
                print(tmp_name, field["Field"], field["Type"])
                datetime_fields[tmp_name].append(field["Field"])
                count += 1

    print("预计更新：", count)
    return datetime_fields


def gen_model_datetime_fields():
    # 筛选模型中datetime的字段
    count = 0
    datetime_fields = get_table_info()

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
