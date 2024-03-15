# -*- coding: utf-8 -*-
# 装饰器模式
import time
import atexit


from multiprocessing import Process
import threading
import os


def memorize(func):
    known = {}

    def memorizer(*args):
        if args not in known:
            known[args] = func(*args)
        return known[args]
    return memorizer


@memorize
def fib(n):
    if n < 0:
        raise ValueError("不能小于0")
    return n if n in (0, 1) else fib(n-1) + fib(n-2)


class dec:
    def __init__(self, prefix_time):
        self.prefix = prefix_time

    def __call__(self, func):
        def wrapper(*args, **kwargs):
            start = time.time()
            ret = func(*args, **kwargs)
            print(self.prefix, time.time()-start)
            return ret
        return wrapper


@dec("hello: ")
def f_cls(x):
    print(os.getpid())
    print(x, threading.current_thread())
    time.sleep(1)
    return x


def t():
    def f():
        print(os.getpid())
        print(threading.current_thread())
        print("hello,world")
    atexit.register(f)


if __name__ == "__main__":
    print(os.getpid())
    print(threading.current_thread())
    p = Process(target=t)
    p.start()
    p.join()

    f_cls(10)