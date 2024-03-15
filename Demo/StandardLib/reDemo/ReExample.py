# coding: utf-8

import re


def search_text():
    text = 'Today is 11/27/2012. PyCon starts 3/13/2013.'

    # 替换字符串
    tmp_text = re.sub(r"(\d+)/(\d+)/(\d+)", r"\3-\2-\1", text)
    print(tmp_text)

    # 搜索字符串
    text_list = re.findall(r"(\d+)/(\d+)/(\d+)", text)
    print(text_list)


if __name__ == "__main__":
    search_text()