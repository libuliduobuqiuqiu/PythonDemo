# -*- coding: utf-8 -*-

from concurrent.futures import ThreadPoolExecutor
from threading import Lock
import time


class TestLock:
    def __init__(self, name):
        self.name = name
        self.lock = Lock()

    def hello(self):
        with self.lock:
            print(f"hello, {self.name}")
            time.sleep(10)


if __name__ == "__main__":
    t_lock = TestLock("linshukai")
    t_lock2 = TestLock("zhangsan")
    with ThreadPoolExecutor(4) as executor:
        executor.submit(t_lock.hello)
        executor.submit(t_lock2.hello)