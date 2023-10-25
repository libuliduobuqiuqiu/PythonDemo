# coding: utf-8
# description: 用于处理魔方选手页面的数据

from bs4 import BeautifulSoup
import pandas as pd
import requests
import urllib3
import json


def handle_person_page(excel_writer: pd.ExcelWriter, wc_id: str, user_name: str):
    # 处理个人页表格

    person_page_url = f"https://www.worldcubeassociation.org/persons/{wc_id}"
    response = requests.get(person_page_url, verify=False)

    html_doc = BeautifulSoup(response.text, 'html.parser')
    personal_records = html_doc.select_one('div.personal-records')
    personal_table = personal_records.select('table')

    df = pd.read_html(str(personal_table[0]))[0]
    df.to_excel(excel_writer, sheet_name=user_name, index=False)


def get_person_info(user_name: str) -> str:
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    base_url = "https://www.worldcubeassociation.org"
    base_headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json, text/javascript',
        'X-Requested-With': 'XMLHttpRequest'
    }

    person_find_url = base_url + f"/persons?search={user_name}&page=1&region=all"
    response = requests.get(person_find_url, verify=False, headers=base_headers)

    if response.status_code >= 400:
        raise Exception(f"{user_name}选手没有匹配到比赛记录")

    # 处理获取wca_id
    wca_id = ""
    base_person_info = response.json()
    if base_person_info.get("rows"):
        rows = base_person_info["rows"]
        if isinstance(rows, list) and len(rows) > 0:
            person_info = rows[0]
            wca_id = person_info['wca_id']

    if not wca_id:
        raise Exception(f"{user_name}选手没有扫描到wca_id")

    return wca_id


if __name__ == "__main__":
    user_list = ["王鹰豪", "王艺衡", "许瑞航", "韩业臻", "张博藩"]

    excel_writer = pd.ExcelWriter("D:\\选手统计表格.xlsx", engine="openpyxl")

    for user in user_list:
        wca_id = get_person_info(user)
        handle_person_page(excel_writer, wca_id, user)

    excel_writer.close()