# -*- coding: utf-8 -*-


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
    a = TestSingleton("lisi")
    b = TestSingleton("zhangsan")
    print(a.get_name)
    print(b.get_name)
    print(a == b)
    print(id(a), id(b))

