# coding: utf-8
"""
    :date: 2023-11-29
    :author: linshukai
    :description: About Werkzeug LocalProxy Object Demo
"""

from werkzeug.local import LocalProxy
from contextvars import ContextVar


class Info:
    pass


class Person:
    def __init__(self):
        self.info = Info()


if __name__ == "__main__":
    flask_var = ContextVar("flask.context")
    p = Person()
    flask_var.set(p)

    proxy = LocalProxy(flask_var, "info", unbound_message="Error bound msg")
    proxy.name = "zhangsan"
    proxy.age = 12
    print(p.info.name, p.info.age)
