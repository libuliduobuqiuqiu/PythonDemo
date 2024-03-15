# coding: utf-8
"""
    :date: 2023-10-25
    :author: linshukai
    :description: About Actor Mode
"""

from threading import Thread, Event
from queue import Queue
import time


class ActorExit(Exception):
    pass


class Actor:
    def __init__(self):
        self._mail_queue = Queue()

    def send(self, msg):
        self._mail_queue.put(msg)

    def recv(self):
        msg = self._mail_queue.get()
        if msg is ActorExit:
            raise ActorExit()
        return msg

    def close(self):
        self.send(ActorExit)

    def run(self):
        while True:
            self.recv()

    def _bootstrap(self):
        try:
            self.run()
        except ActorExit:
            pass
        finally:
            self._terminated.set()

    def join(self):
        self._terminated.wait()

    def start(self):
        self._terminated = Event()
        t = Thread(target=self._bootstrap)
        t.daemon = True
        t.start()


class PrintActor(Actor):
    def run(self):
        while True:
            msg = self.recv()
            print(f"Got {msg}")


if __name__ == "__main__":
    p = PrintActor()
    p.start()
    p.send("hello")
    time.sleep(2)
    p.send('world')
    p.close()
    p.join()

