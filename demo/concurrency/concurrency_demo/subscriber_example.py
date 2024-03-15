# coding: utf-8
"""
    :date: 2023-10-25
    :author: linshukai
    :description: About Subscriber Demo
"""

from collections import defaultdict


class Exchange:
    def __init__(self):
        self._subscribers = set()

    def attach(self, subscriber):
        self._subscribers.add(subscriber)

    def detach(self, subscriber):
        self._subscribers.remove(subscriber)

    def send(self, msg):
        for subscriber in self._subscribers:
            subscriber.send(msg)


ex = defaultdict(Exchange)


def get_exchange(name):
    return ex[name]


class Task:
    def __init__(self, name):
        self._name = name

    def send(self, msg):
        print(f"{self._name} Got {msg}")


if __name__ == "__main__":
    task_a = Task("A")
    task_b = Task("B")

    tmp_ex = get_exchange("name")
    tmp_ex.attach(task_a)
    tmp_ex.attach(task_b)

    tmp_ex.send("hello")
    tmp_ex.send('world')
