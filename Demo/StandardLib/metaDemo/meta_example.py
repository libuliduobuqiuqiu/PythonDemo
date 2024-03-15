# coding: utf-8
import inspect
import operator
from inspect import Parameter, Signature

from StandardLib.collectionsDemo import *


def make_sig(*names):
    params = [Parameter(name, Parameter.POSITIONAL_OR_KEYWORD) for name in names]
    return Signature(params)


class StructTupleMeta(type):
    def __init__(cls, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for n, name in enumerate(cls._fields):
            setattr(cls, name, property(operator.itemgetter(n)))


class StructTuple(tuple, metaclass=StructTupleMeta):
    _fields = []

    def __new__(cls, *args):
        if len(args) != len(cls._fields):
            raise ValueError(f"{len(cls._fields)} arguments required")
        return super().__new__(cls, args)


class Stock(StructTuple):
    _fields = ["name", "shares", "price"]


class Point(StructTuple):
    _fields = ["X", "Y"]


class NoMixedClassMeta(type):
    def __new__(cls, clsname, bases, clsdict):
        for name in clsdict:
            if name.lower() != name:
                raise TypeError("Bad Attribute name: ", name)
        return super().__new__(cls, clsname, bases, clsdict)


class Root(metaclass=NoMixedClassMeta):
    pass


class A(Root):
    def print_bar(self):
        pass


class B:
    def Print_Bar(self):
        pass


class Singleton(type):
    def __init__(self, *args, **kwargs):
        self._instance = None
        super().__init__(*args, **kwargs)

    def __call__(self, *args, **kwargs):
        if self._instance is None:
            self._instance = super().__call__(*args, **kwargs)
        return self._instance


class MyMeta(type):
    def __init__(cls, *args, **kwargs):
        print("My Meta")
        super().__init__(cls, args, kwargs)


class Spam(metaclass=Singleton):

    def __init__(self, x):
        self.x = x

    @staticmethod
    def grok():
        print("spam.gork: ")

    def print_x(self):
        print(self.x)


if __name__ == "__main__":
    s = Stock("zhangsan", 22, 22)
    p = Point(11, 22)

    print(s, s.name, s.price)
    print(p)

    a = A()
    b = B()
    a.print_bar()
    b.Print_Bar()


1