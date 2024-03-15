# coding: utf-8
"""
    :date: 2023-11-17
    :author: linshukai
    :description: About Device
"""

ad_fields = """
    project_id,
    name,
    ip,
    ssh_port,
    api_port,
    web_url,
    auth_password_id,
    access_password_id,
    provider_name,
    device_group_id,
    syn_group_id,
    remote_url,
    upload_credentials,
    maintenance_start,
    maintenance_end 
"""

ad_device_fields = """
    project_id,
    name,
    address,
    ssh_port,
    api_port,
    web_url,
    password_policy_id,
    credential_policy_id,
    provider_name,
    device_group_id,
    syn_group_id,
    remote_url,
    upload_credentials,
    maintenance_start_date,
    maintenance_end_date 
"""

from cmdb_update import init_connect
from setting import CompanySetting
from storage.mysql_demo.pymysql_example import exec_sql

import datetime


def gen_ad_data():
    tmp_ad_fields = "".join(ad_fields.split())
    tmp_ad_device_fields = "".join(ad_device_fields.split())
    ad_field_list = [field for field in tmp_ad_fields.split(",")]
    ad_device_field_list = [field for field in tmp_ad_device_fields.split(",")]

    print(len(ad_field_list), ad_field_list)
    print(len(ad_device_field_list), ad_device_field_list)

    post_data = []
    db_name = "cmdb"
    sql_str = "select * from instance_ad_device"
    results = exec_sql(CompanySetting(), db_name, sql_str, [])
    for item in results:
        tmp_dict = {}
        for k, field in enumerate(ad_field_list):
            tmp_value = item[ad_device_field_list[k]]
            if isinstance(tmp_value, datetime.date):
                tmp_value = tmp_value.strftime("%Y-%m-%d")

            tmp_dict[field] = tmp_value
        tmp_dict["occupied_u"] = 1
        tmp_dict["auth_password_id"] = str(tmp_dict["auth_password_id"])
        tmp_dict["access_password_id"] = str(tmp_dict["access_password_id"])
        post_data.append(tmp_dict)
        print(tmp_dict)

    url = "http://10.21.21.230/cmdb/models/ad/instances"
    session = init_connect()

    for data in post_data:
        resp = session.post(url, json=data)

        print(resp.status_code, resp.text)
        if resp.status_code != 200:
            print(resp.json())
            return


if __name__ == "__main__":
    gen_ad_data()
