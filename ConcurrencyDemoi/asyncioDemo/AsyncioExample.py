# -*- coding: utf-8 -*-
# 异步IO模块

from bs4 import BeautifulSoup

import asyncio
import requests
import time


async def f():
    print("hello")
    await asyncio.sleep(1)
    print("world")


def get_bili():
    url = "https://www.bilibili.com"
    response = requests.get(url)

    bs = BeautifulSoup(response.text, "html.parser")
    title = bs.find("title")
    print(title.text)

get_bili()