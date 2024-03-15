# -*- coding: utf-8 -*-
import requests


def test_example():
    response = requests.get("https://www.baidu.com")
    status_code = response.status_code
    assert status_code == 200
