# coding: utf-8

"""
    :author: linshukai
    :description: About Rpc Demo
"""

import pickle

from multiprocessing.connection import Listener
from threading import Thread


class RpcHandler:

    def __init__(self):
        self._functions = {}

    def register_func(self, name, func):
        self._functions[name] = func

    def handle_connection(self, connection):
        try:
            while True:
                func, args, kwargs = pickle.loads(connection.recv())

                try:
                    r = self._functions[func](*args, **kwargs)
                    connection.send(pickle.dumps(r))
                except Exception as e:
                    connection.send(pickle.dumps(e))
        except EOFError:
            pass


def rpc_server(handler, address, auth_key):
    sock = Listener(address, authkey=auth_key)

    while True:
        client = sock.accept()
        t = Thread(handler.handle_connection, args=(client,))
        t.daemon = True
        t.start()


def add(x, y):
    return x + y


def sub(x, y):
    return x - y


if __name__ == "__main__":
    rpc_handler = RpcHandler()
    rpc_handler.register_func("add", add)
    rpc_handler.register_func("sub", sub)
    rpc_server(rpc_handler, ("", 8992), auth_key=b"china")
