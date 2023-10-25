# coding: utf-8

from collections.abc import Iterable


class MyList(Iterable):
    def __init__(self, my_list):
        self._my_list = my_list

    def __iter__(self):
        return iter(self._my_list)


class A:
    def __init__(self, name):
        self.name = name

    def hello(self):
        print(f"Hello,World {self.name}")


class B:
    def __init__(self):
        self._a = A("B")

    def speak(self):
        print("I'm B")

    def __getattr__(self, item):
        return getattr(self._a, item)


if __name__ == "__main__":
    b = B()
    b.speak()
    b.hello()