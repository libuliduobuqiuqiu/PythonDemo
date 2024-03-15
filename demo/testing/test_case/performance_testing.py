# coding: utf-8
"""
    :date: 2023-10-25
    :author: linshukai
    :description: About Performance Testing Demo
"""

from functools import wraps
from contextlib import contextmanager
import time


def time_count(func):
    @wraps(func)
    def count(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        end = time.perf_counter()
        print(f"{func.__module__}.{func.__name__}: {end - start}")
        return result

    return count


@contextmanager
def time_block(label):
    start = time.perf_counter()
    try:
        yield
    finally:
        end = time.perf_counter()
        print(f"{label}: {end - start}")


@time_count
def hello_world():
    print("hello")
    time.sleep(2)
    print("world")


def next_word(a, b,  *, x, y):
    print(a, b, x, y)


if __name__ == "__main__":
    next_word(1, 2, x=3, y=4)
