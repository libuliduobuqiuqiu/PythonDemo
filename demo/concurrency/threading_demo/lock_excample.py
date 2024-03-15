# coding: utf-8
"""
    :date: 2023-10-27
    :author: linshukai
    :description: About Threading Lock Demo
"""

from threading import Lock, RLock
import time


class SharedCounter:
    def __init__(self, initial_value=0):
        self._value = initial_value
        self._lock = RLock()

    def incr(self, delta=1):
        self._lock.acquire()
        self._value += delta
        print("incr: ", self._value)
        time.sleep(2)
        self._lock.release()

    def decr(self, delta=1):
        self._lock.acquire()
        self._value -= delta
        print("decr: ", self._value)
        time.sleep(2)
        self._lock.release()

    def get_value(self):
        print("Now Value: ", self._value)


if __name__ == "__main__":
    counter = SharedCounter()
    counter.incr()
    counter.decr()
    counter.get_value()