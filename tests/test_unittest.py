# -*- coding: utf-8 -*-

from unittest import TestCase
import unittest
import sys


class TestExample(TestCase):

    def setUp(self):
        print("start")

    def tearDown(self) -> None:
        print("end")

    @unittest.skipIf(sys.version_info > (3, 7), "only support 3.7-")
    def test_print_version(self):
        self.assertTrue(sys.version_info > (3, 7))

    def test_print_system(self):
        print(sys.platform)
        self.assertTrue(sys.platform == 'win32')
