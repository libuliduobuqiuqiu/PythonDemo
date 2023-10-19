# coding: utf-8
"""
    :author: linshukai
    :description: datetime Demo
"""

from DatetimeExample import MyDate

if __name__ == "__main__":
    a = MyDate(year=2023, month=9, day=23)
    print(format(a, "mdy"))
