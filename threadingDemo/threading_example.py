# coding: utf-8
"""
    :date: 2023-10-23
    :author: linshukai
    :description: About Threading Demo
"""

from threading import Thread, Lock
from queue import Queue
import time


def count_down(n):
    while n > 0:
        print("T-minus: ", n)
        time.sleep(2)
        n -= 1


def producer(in_deq: Queue, data: list):
    for item in data:
        tmp_item = f"Item {item}"
        print("Produced: ", tmp_item)
        in_deq.put(tmp_item)
        time.sleep(2)


def consumer(deq: Queue):

    while True:
        data = deq.get()

        if data is None:
            break

        print("Consumed: ", data)
        deq.task_done()


class SharedCounter:
    _value_lock = Lock()

    def __init__(self, value):
        self._value = value

    def incr(self, delta=1):
        with self._value_lock:
            self._value += delta

    def decr(self, delta=1):
        with self._value_lock:
            self._value -= delta


if __name__ == "__main__":
    deq = Queue()
    con = Thread(target=consumer, args=(deq,))

    data = ["zhangsan", 2,3, 1, "wangwu", 333, "ifnconfig"]
    pro = Thread(target=producer, args=(deq, data))

    con.start()
    pro.start()

    pro.join()
    deq.put(None)
    print("end.")