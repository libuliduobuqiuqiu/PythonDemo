# -*- coding: utf-8 -*-
import concurrent.futures
from unittest import TestCase
from concurrent.futures import ThreadPoolExecutor

import unittest
import logging
import threading
import warnings


class MyTest(TestCase):
    _num = 0

    def setUp(self) -> None:
        self.logger = logging.getLogger(__name__)

    def add(self):
        self._num += 1

    def sub(self):
        self._num -= 1

    def count(self):
        self.add()
        self.sub()
        self.logger.info(self._num)
        self.logger.info(f"活跃的线程:{threading.active_count()}")

    def test_correct_num(self):
        with ThreadPoolExecutor(128) as pool:
            all_task = [pool.submit(self.count) for _ in range(200)]

        concurrent.futures.wait(all_task)
        self.assertEquals(self._num, 0)


def use_logfile(logfile=None):
    if logfile is not None:
        warnings.warn('logfile argument deprecated', DeprecationWarning)


if __name__ == "__main__":
    unittest.main()
