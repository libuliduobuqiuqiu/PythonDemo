# coding: utf-8
"""
    :date: 2024-1-3
    :author: linshukai
    :description: About adops config file parse
"""
from update_project import update_project_excutable

update_project_excutable()

from storage.mysql_demo.pymysql_example import exec_sql
from setting import CompanySetting57


def get_config_json():
    setting = CompanySetting57()
    result = exec_sql(setting, "adops", "select * from config", [])

    for item in result:
        print(item)


if __name__ == "__main__":
    get_config_json()
