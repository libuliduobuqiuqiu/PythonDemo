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


if __name__ == "__main__":
    with time_block("counting"):
        n = 1000000
        while n > 0:
            n -= 1
