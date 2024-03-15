# -*- coding: utf-8 -*-
"""
    :date: 2023-10-31
    :author: linshukai
"""

from abc import ABCMeta


class SingletonMeta(type):
    def __call__(cls, *args, **kwargs):
        print("__call__")
        if not hasattr(cls, "_instance"):
            cls._instance = super().__call__(*args, **kwargs)
        return cls._instance


class S1(metaclass=SingletonMeta):
    def __init__(self):
        print("__init__")
        self._name = None

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, tmp_name):
        self._name = tmp_name

    @name.getter
    def name(self):
        return self._name


class Singleton:
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, "_instance"):
            _instance = object.__new__(cls)
            cls._instance = _instance
        return cls._instance


class TestSingleton(Singleton):
    def __init__(self, new_value):
        self._name = new_value

    @property
    def get_name(self):
        return self._name


def Singleton2(class_):
    _instances = {}

    def get_instances(*args, **kwargs):
        if class_ not in _instances:
            _instances[class_] = class_(*args, **kwargs)
        return _instances[class_]

    return get_instances


@Singleton2
class TestSingleton2:
    def __init__(self, new_value):
        self._name = new_value

    @property
    def get_name(self):
        return self._name


if __name__ == "__main__":
    print("starting")
    s1 = S1()
    s2 = S1()
    print(s1 == s2, id(s1), id(s2))

    s1.name = "zhangsan"
    print(s2.name)
