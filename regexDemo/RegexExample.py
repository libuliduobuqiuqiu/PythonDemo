# -*- coding: utf-8 -*-

from xeger import Xeger
import random
import re


def check_strong_password(password: str) -> int:
    """
    检测密码强度
    :param password:
    :return:
    """
    regex_list = [r"[a-z]+", r"[A-Z]+", r"[0-9]+", r"\W+"]

    strength = 0
    for regex in regex_list:
        if re.search(regex, password):
            strength += 1

    return strength


def generate_id() -> str:
    regex = r"^[1-9]\d{5}(18|19|([2-3]\d))\d{2}((0[1-9])|10|11|12)(([0-2][1-9])|10|20|30|31)\d{3}[0-9xX]$"

    x = Xeger()
    new_id = x.xeger(regex)
    return new_id


def split_num(num: str):
    regex = r"(?!^)(?=(\d{3})+$)"
    result = re.sub(regex, ",", num)
    return result


def split_phone(phone_num: str):
    """
    电话号码3-4-4分割
    :param phone_num:
    :return:
    """
    regex = r"(?=(\d{4})+$)"
    result = re.sub(regex, ',', phone_num)
    return result

def g():
    d = {}
    def f():
        d["a"] = 1
        pass
    return f

if __name__ == "__main__":
    # for  i in range(10):
    #     num = random.randint(15000000000, 18000000000)
    #     print(split_phone(str(num)))
    code = g().__code__
    print("cellvars", code.co_cellvars)
    print("freevars", code.co_freevars)

