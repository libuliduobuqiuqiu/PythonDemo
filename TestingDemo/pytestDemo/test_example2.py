# -*- coding: utf-8 -*-

import pytest


@pytest.fixture(scope="function")
def func_scope():
    print("func_scope")


@pytest.fixture(scope="module")
def mod_scope():
    print("mod_scope")


@pytest.fixture(scope="session")
def sess_scope():
    print("session_scope")


def test_scope(sess_scope, mod_scope, func_scope):
    pass


def test_scope2(sess_scope, mod_scope, func_scope):
    pass