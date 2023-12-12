# coding: utf-8
"""
    :date: 2023-11-28
    :author: linshukai
    :description: About ContextVars Using Demo
"""

from contextvars import ContextVar
from operator import attrgetter

_cv_app = ContextVar("python_demo")


class Person:
    flag = True

    def __init__(self, name):
        self.name = name

    def __get__(self, instance, owner):
        print("instance:", instance, owner, type(owner))
        return self.name

    def __set__(self, instance, value):
        self.name = value

    def __setattr__(self, key, value):
        print(key, type(key), value, type(value))
        super().__setattr__(key, value)


class PersonManger:
    p = Person("PersonManager")

    def __init__(self, count):
        self.count = count

    def __getattr__(self, item):
        print("test: ", str(item))


def get_name(name, p):
    f = attrgetter(name)
    print(f(p))


if __name__ == "__main__":
    p = PersonManger(12)
    print(p.count)
    print(p.p)
    p.p = "PersonManager(S)"
    print(p.p)
    print(p.age)

    flask_app = ContextVar("flask_app")
    flask_app.set(p)
    flask_app.set(p)
    print(flask_app.get())
    print(flask_app.get())
