# -*- coding: utf-8 -*-

from datetime import datetime, timedelta, timezone

import asyncio
import time


def datetime_example():
    # 将当前时间转换成utc时间
    now_date = datetime.strptime("2022-06-22 22:21:10", "%Y-%m-%d %H:%M:%S")
    now_date_utc = now_date.replace(tzinfo=timezone.utc)
    now_timestamp = now_date_utc.timestamp()

    # 将utc时间转换成东八区时间
    temp_datetime = now_date_utc.astimezone(timezone(timedelta(hours=8)))
    print(temp_datetime.strftime("%Y-%m-%d %H:%M"))


async def main():
    print("hello")
    time.sleep(1)
    print("world")


if __name__ == "__main__":
    t_main = main()
    print(type(t_main))
    asyncio.run(t_main)