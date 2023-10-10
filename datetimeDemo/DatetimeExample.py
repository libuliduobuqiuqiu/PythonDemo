# -*- coding: utf-8 -*-

from itertools import chain
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


# 计算上个星期几是多少号
def datetime_handle(spec: str):
    weekdays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday',
                'Friday', 'Saturday', 'Sunday']

    if spec not in weekdays:
        print("无效的星期，仅支持：", weekdays)

    start_date = datetime.today()
    week_day = start_date.weekday()
    day_target = weekdays.index(spec)
    days_ago = (7 + week_day - day_target) % 7
    if days_ago == 0:
        days_ago = 7

    target_date = start_date - timedelta(days=days_ago)
    print(target_date)


class Node:
    def __init__(self, value):
        self.value = value
        self.children = []

    def __repr__(self):
        return f"Node({self.value})"

    def __iter__(self):
        return iter(self.children)

    def add_children(self, node):
        self.children.append(node)

    def depth_first(self):
        yield self

        for c in self:
            yield from c.depth_first()


_formats = {
    'ymd': '{d.year}-{d.month}-{d.day}',
    'mdy': '{d.month}/{d.day}/{d.year}',
    'dmy': '{d.day}/{d.month}/{d.year}'
}


class MyDate:
    def __init__(self, year, month, day):
        self.year = year
        self.month = month
        self.day = day

    def __format__(self, code):
        if code == "":
            code = "ymd"

        fmt = _formats[code]
        return fmt.format(d=self)


if __name__ == "__main__":
    a = MyDate(year=2023, month=9, day=23)
    print(format(a, "mdy"))
