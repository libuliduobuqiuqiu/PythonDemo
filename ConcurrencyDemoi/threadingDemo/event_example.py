# coding: utf-8
"""
    :date: 2023-10-27
    :author: linshukai
    :description: About Threading Event Demo
"""

from threading import Thread, Event
import time


def count_down(n, start_event):
    print("counting down start....")

    while n >0:
        print("T-minus: ", n)
        n -= 1
        time.sleep(5)
    start_event.set()


if __name__ == "__main__":
    event = Event()
    t = Thread(target=count_down, args=(5, event))
    t.start()

    event.wait()
    print("count down end....")