# coding: utf-8
"""
    :date: 2023-11-27
    :author: linshukai
    :description: About Getattr Function
"""


class Person:
    name = "zhansan"
    age = 12

    def hello(self):
        raise RuntimeError("hello function is error.")


def person_hello():
    a = Person()

    try:
        a.hello()
    except RuntimeError as err:
        raise ConnectionError("test connection error.") from None


if __name__ == "__main__":
    person_hello()
