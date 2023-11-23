# -*- coding: utf-8 -*-
# 异步IO模块

from bs4 import BeautifulSoup

import asyncio
import requests
import time

import asyncio
import aiohttp


async def f():
    print("hello")
    await asyncio.sleep(1)
    print("world")


async def fetch_data(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.text()


def get_bili():
    url = "https://www.bilibili.com"
    response = requests.get(url)

    bs = BeautifulSoup(response.text, "html.parser")
    title = bs.find("title")
    print(title.text)


async def main():
    url_list = ["http://www.baidu.com", "http://www.bilibili.com", "http://www.qq.com"]

    tasks = [fetch_data(url) for url in url_list]
    results = await asyncio.gather(*tasks)

    for r in results:
        print(r)

if __name__ == "__main__":
    asyncio.run(main())


