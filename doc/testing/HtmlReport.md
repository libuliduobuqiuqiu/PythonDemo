## 背景
最近开发有关业务场景的功能时，涉及的API接口比较多，需要自己模拟多个业务场景的自动化测试（暂时不涉及性能测试），并且在每次测试完后能够生成一份测试报告。
考虑到日常使用python自带的unittest，所以先从官方文档下手，了解到有相关的TestTextRunner:

> https://docs.python.org/zh-cn/3/library/unittest.html?highlight=unittest#unittest.TextTestRunner

自带的TextTestRunner每次能把测试结果输出到流中的测试运行器，可以简单根据verbosity调整每次测试结果输出的信息，但是都太基础了，如果我想在测试过程中打印一些请求参数或者docstring，看了一下unittest内置的方法，实现过程可能会比较繁琐。  
然后在网上找了一下轮子工具，html-testrunner,beautifulreport，这些工具生成的网页css、js都是使用公网的CDN，由于内网环境，不适合。后面看了一些技术文章很多都是使用pytest，之前有相关pytest的基础使用经验，大概了解一下，决定根据pytest+pytest-html满足当前测试场景，以下是有关pytest和pytest-html的官方文档：

> https://docs.pytest.org/en/7.1.x/how-to/index.html  
> https://pytest-html.readthedocs.io/en/latest/


## 模块安装
```
pip install pytest
pip install pytest-html
```


## 方案设计

### pytest.ini
首先定义pytest.ini（pytest的基础配置文件，和测试文件在同一目录，使用pytest命令时会先读取该文件）
```
[pytest]
log_cli = True
log_cli_level = INFO

```
备注：开启日志消息打印，设置日志记录捕获的最低消息级别为INFO

### conftest.py

设置conftest.py（没有自己创建，同样是和测试文件同个目录下，用于pytest-html生成测试报告的配置文件）
```
# --*-- coding: utf-8 --*--
from datetime import datetime
from py.xml import html
import pytest


def pytest_html_report_title(report):
    report.title = "测试报告"


def pytest_html_results_table_header(cells):
    cells.insert(2, html.th("Description"))
    cells.insert(1, html.th("Time", class_="sortable time", col="time"))
    cells.pop()


def pytest_html_results_table_row(report, cells):
    cells.insert(2, html.td(report.description))


def pytest_html_results_table_row(report, cells):
    cells.insert(2, html.td(report.description))
    cells.insert(1, html.td(datetime.utcnow(), class_="col-time"))
    cells.pop()


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    report.description = str(item.function.__doc__)
```
通过设置钩子函数分别修改测试报告的列，添加描述列，测试用例耗时时间列，删除链接列，我这里是直接参考官方文档中给出的示例
```
https://pytest-html.readthedocs.io/en/latest/user_guide.html#creating-a-self-contained-report
```
有兴趣的可以研究一下，


### 测试用例
根据pytest的官方文档，pytest同样是支持unittest的功能，所以可以在原有的基础上直接运行pytest
```python
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
    pytest.main(["pytest_example.py", "--html=report.html", "--self-contained-html"])
```
备注：
简单的写了几个测试用例，需要特别说明的是可以通过pytest.main()方法，直接在python代码中调用pytest，所以我每次只需要执行这个脚本就行，当然也可以选择在命令行界面通过pytest命令调用指定测试文件执行指定测试用例。  
另外一个地方需要注意的是--self-contained-html这个参数主要是针对pytest-html模块，由于默认pytest-html中生成测试报告的网页和CSS文件都是分开来存储的，如果想直接将css文件合并到html中，这样分享测试报告的时候也更加方便，所以只需要加入这个参数即可--self-contained-html。


## 预期会出现的问题

pytest中使用requests，抛出错误，但不影响测试结果，抛出的异常：
```
Windows fatal exception: code 1073807366
```
解决方式，降低pytest为4.6.11版本后，异常就不会抛出，但是pytest-html需要6.0版本上的pytest，由于不影响测试结果，更加完善的解决方法后续再研究；

## 备注
后续关于pytest和pytest-html生成测试报告的方案后期如果有什么问题，或者优化的地方都会不断完善更新，欢迎讨论。。。


