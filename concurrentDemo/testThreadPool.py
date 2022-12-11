# -*- coding: utf-8 -*-

from concurrent.futures import ThreadPoolExecutor
import requests


def get_html(url: str) -> int:
    response = requests.get(url)
    status_code = response.status_code
    return status_code


if __name__ == "__main__":
    url_list = [
        "http://www.baidu.com",
        "http://www.douban.com",
        "http://www.weibo.com",
        "http://www.jd.com"
    ]
    all_task = []
    with ThreadPoolExecutor(4) as executor:
        for url in url_list:
            all_task.append(executor.submit(get_html, url))

    for task in all_task:
        print(task.result(), task)
