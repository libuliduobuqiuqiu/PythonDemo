# coding: utf-8
"""
    :date: 2023-10-27
    :author: linshukai
    :description: About Queue Demo
"""

from threading import Thread
from queue import Queue
import time


_senti = object()

def producer(data: list, deque: Queue):
    for item in data:
        print("Producer: ", item)
        deque.put(item)
        time.sleep(2)

    deque.put(_senti)

def consumer(deque:Queue):
    while True:
        item = deque.get()

        if item is _senti:
            break

        print("Consumer: ", item)


if __name__ == "__main__":
    print("starting....")
    deq = Queue()
    c_data = ["zhangdan", "Guangdong", "China", 222, 20310203, "ifconfig", "netstat -tualnp", "hello,world"]

    p = Thread(target=producer, args=(c_data, deq))
    c = Thread(target=consumer, args=(deq,))

    p.start()
    c.start()

    deq.join()
    print("end....")