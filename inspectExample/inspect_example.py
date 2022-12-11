# -*- coding: utf-8 -*-

import inspect
import time
from objprint import op
import dis
import sys


def f():
    frame = inspect.currentframe()
    print(frame.f_back.f_code.co_filename)
    print(frame.f_back.f_lineno)


class Timer:
    def __init__(self, func):
        self.func = func

    def __call__(self, *args, **kwargs):
        start = time.time()

        ret = self.func(*args, **kwargs)

        end = time.time()
        print(end - start)

        return ret


class Timer2:
    def __init__(self, prefix_time):
        self.prefix_time = prefix_time

    def __call__(self, func):
        def wrapper(*args, **kwargs):
            start = time.time()

            ret = func(*args, **kwargs)

            end = time.time()
            print(self.prefix_time, end - start)
            return ret

        return wrapper


@Timer
def add(a, b):
    time.sleep(1)
    return a + b


@Timer2(prefix_time="current time: ")
def add2(a, b):
    time.sleep(1)
    return a + b


class NodeIter:
    def __init__(self, node):
        self.current_node = node

    def __next__(self):
        node, self.current_node = self.current_node, self.current_node.next
        return node

    def __iter__(self):
        return self


class Node:
    def __init__(self, name):
        self.name = name
        self.next = None

    def __iter__(self):
        return NodeIter(self)


class Node2:
    def __init__(self, name):
        self.name = name
        self.next = None

    def __iter__(self):
        node = self
        while node is not None:
            yield node.name
            node = node.next


def gen(num):
    while num > 0:
        temp = yield num

        if temp is not None:
            temp = num
        num -= 1


def f1(self):
    print(self.name)

def __init__(self):
    self.name = "linshukai"

temp_dict = {
    "name": "linshukai",
    "f": f1
}

B = type("A", (), temp_dict)
print(B.__dict__, B.__name__)
a = B()
a.f()

