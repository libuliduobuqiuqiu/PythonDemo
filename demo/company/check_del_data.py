# coding: utf-8
"""
    :Date: 2024-1-22
    :Author: linshukai
    :Description: About Check data after delete device and device Group
"""

from os import device_encoding
import sys

sys.path.insert(0, "/data/PythonDemo/")

from setting import CompanySetting
from storage.mysqlDemo.pymysql_example import *


def select_ad_tables():
    db_name = "cmdb"
    tables = get_tables(db_name)

    public_model = [
        "instance_device_inspection",
        "instance_device_backup",
        "instance_device_conf",
    ]

    ad_tables = []
    for table_name in tables:
        if table_name.startswith("instance_ad_") or table_name in public_model:
            ad_tables.append(table_name)

    with open("instance_ad_tables.txt", "r") as f:
        tmp_tables = f.readlines()

    tmp_tables = list(map(lambda x: x.strip(), tmp_tables))
    print(tmp_tables)
    for t in ad_tables:
        if t not in tmp_tables:
            print(t)


def count_ad_tables(device_id: str):
    with open("instance_ad_tables.txt", "r") as f:
        tmp_tables = f.readlines()

    ad_tables = []
    for t in tmp_tables:
        table_name = t.strip()
        if table_name:
            ad_tables.append(table_name)

    # dev_sql = "select * from instance_ad where id = %s"
    # results = exec_sql(CompanySetting(), "cmdb", dev_sql, [device_id])

    results = [
        {
            "device_group_id": "1694968171335004160",
            "syn_group_id": "1694968171444056064",
        }
    ]

    if results:
        dg_id = results[0]["device_group_id"]
        sg_id = results[0]["syn_group_id"]

        if dg_id:
            public_dg = [
                "instance_ad_dns_listener",
                "instance_ad_traffic_group",
                "instance_ad_llb_outbound",
            ]
            for t in ad_tables:
                if t.startswith("instance_ad_slb") or t in public_dg:
                    print(t, ":")
                    tmp_sql = f"select count(*) from {t} where device_group_id = %s"
                    results = exec_sql(CompanySetting(), "cmdb", tmp_sql, [dg_id])
                    print(results)

            tmp_sql = f"select count(*) from instance_ad_device_group where id = %s"
            results = exec_sql(CompanySetting(), "cmdb", tmp_sql, [dg_id])
            print("instance_ad_device_group", results)
        if sg_id:
            for t in ad_tables:
                if t == "instance_ad_dns_prober_pool_member":
                    print(t, ":")
                    tmp_sql = f"select count(*) from instance_ad_dns_prober_pool_member m join instance_ad_dns_prober_pool p on m.dns_prober_pool_id = p.id where p.syn_group_id = %s "
                    results = exec_sql(CompanySetting(), "cmdb", tmp_sql, [sg_id])
                    print(results)
                    continue

                if t.startswith("instance_ad_dns") and t != "instance_ad_dns_listener":
                    print(t, ":")
                    tmp_sql = f"select count(*) from {t} where syn_group_id = %s"
                    results = exec_sql(CompanySetting(), "cmdb", tmp_sql, [sg_id])
                    print(results)
            tmp_sql = "select count(*) from instance_ad_syn_group where id = %s"
            results = exec_sql(CompanySetting(), "cmdb", tmp_sql, [sg_id])
            print("instance_ad_syn_group", results)


if __name__ == "__main__":
    count_ad_tables("1750412621875511296")
