# coding: utf-8
"""
    :date: 2023-11-10
    :author: linshukai
    :description: 更新部分模型的约束
"""

import requests
from collections import defaultdict


def gen_update_table():
    # 生成需要更新字段的字典
    with open("AD_Table.txt", "r") as f:
        tables = f.readlines()

    print("总共需要更新：", len(tables))

    table_map = defaultdict(list)
    for content in tables:
        model_name, model_field, field_type = content.split()
        model_name = model_name.split("instance_")[1]
        table_map[model_name].append({"field_name": model_field, "field_type": field_type})
    return table_map


def init_connect():
    cookie = "iam.session=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjo1NTgxMDMsImp0aSI6IkozTlVTM0Q0WXpXbTZ0OVlyMFBwdGwiLCJpYXQiOjE3MDEwNDg1MzYsImV4cCI6MTcwMTA0MTMzNn0K.rnB8b2Dgr0U36RSthRSxfkvtyeQCE4WkyHaWsAKC8Uc; sr.access_token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjo1NTgxMDMsInNlcnZpY2VfaWQiOjU2MSwiZ3R5cCI6MiwianRpIjoibExaZ3Y3Qzg3TXBJUDRNWmRaa3FJIiwiaWF0IjoxNzAxMDQ4NTQwLCJleHAiOjE3MDEwNDEzNDB9Cg.1U0BOhHpmy2IZtv3OCwe_scTBs8T99HIueBIK7yALUs; sr.refresh_token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjo1NTgxMDMsInNlcnZpY2VfaWQiOjU2MSwiZ3R5cCI6MiwianRpIjoiTjRLa2M5anJWQkNZUmVtYXh5RXBZIiwiaWF0IjoxNzAxMDQ4NTQwLCJleHAiOjE3MDEwMzQxNDB9Cg.Tslf7JX1bjVpfA9STAxUQ8Pe69wSAZ1yvwCUws72Sag"
    headers = {"Cookie": cookie, "Content-Type": "application/json"}
    session = requests.session()
    session.headers = headers
    return session


def get_models(model_name):
    url = f"http://10.21.21.230/cmdb/models/{model_name}/fields"

    session = init_connect()
    response = session.get(url)

    if response.status_code > 200:
        print(response.text)
        return

    data = response.json()
    return data


def gen_update_field():
    count = 0
    update_field_list = []
    update_field_dict = gen_update_table()
    constraints_rule = {"bigint": 11, "text": 256, "mediumtext": 65536, "longtext": 16777216}

    for model_name, field_list in update_field_dict.items():

        model_info = get_models(model_name)
        field_dict = {v["field_name"]: v["field_type"] for v in field_list}
        for item in model_info["items"]:
            model_fields = item["fields"]
            for field in model_fields:
                if field["name"] in field_dict:

                    field_type = field_dict[field["name"]]

                    if field_type.find("bigint") != -1:
                        field["constraints"] = [{"max_length": constraints_rule["bigint"]}]
                    elif field_type in constraints_rule:
                        field["constraints"] = [{"max_length": constraints_rule[field_type]}]
                    else:
                        print("无法匹配：", field["name"], field_type)
                        continue

                    update_field_list.append(field)
                    count += 1
    print("预计更新：", count)
    return update_field_list


def update_model_field():
    # 读取扫描的特殊Field字段类型的文件 -》 读取对应模型下Field信息 -》 匹配插入对应字段类型的约束 -》 执行接口更新操作
    field_list = gen_update_field()

    count = 0
    for field in field_list:
        url = f"http://10.21.21.230/cmdb/models/{field['model_id']}/fields/{field['id']}"
        print(url)

        session = init_connect()
        response = session.put(url, json=field)

        if response.status_code > 200:
            print(response.text)
            return

        count += 1
        print(field)

    print("已更新：", count)


if __name__ == "__main__":
    update_model_field()
