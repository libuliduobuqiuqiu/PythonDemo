# -*- coding: utf-8 -*-
# @Author: linshukai
# @Desc: pytestc测试用例
# @Date: 20220827

import unittest
import pytest
import logging

import requests


class TestString(unittest.TestCase):
    def test_upper_method(self):
        """
        测试字符串大写
        """
        self.assertEqual("linshukai".upper(), "LINSHUKAI")
        logging.info("测试linshukai")

    def test_lower_method(self):
        """
        测试字符串小写
        """
        self.assertEqual( "ZhangSan".lower(), "zhangsan")
        logging.info("测试ZhangSan")

    def test_count_method(self):
        """
        测试字符串长度统计
        """
        self.assertEqual( len("zhangsan"), 8)
        logging.info("测试Zhangsan")


class TestString2(unittest.TestCase):

    def test_get_html(self):
        """
        测试请求网页状态码是否正常
        """
        response = requests.get("http://www.baidu.com")
        self.assertEqual(response.status_code, 500)


if __name__ == "__main__":
    pytest.main(["test_example.py", "--html=report.html", "--self-contained-html"])