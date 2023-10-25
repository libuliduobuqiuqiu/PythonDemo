# -*- coding: utf-8 -*-

from unittest import TextTestRunner, TestSuite
from unittest import TestLoader

import HtmlTestRunner
import unittest
import math
import pytest
import logging



def test_num():
    """
    测试统计内容
    :param a:
    :return:
    """
    logging.warn("asuccess")
    assert len([1]) == 1


def test_count():
    """
    测试统计
    :return:
    """
    assert len([1, 2, 3]) != 3
