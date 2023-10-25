# coding: utf-8
"""
    :date: 2023-10-24
    :author: linshukai
    :description: About Lazy Connection about SocketDemoSocketDemo demo
"""

from socket import AF_INET, SOCK_STREAM, socket
from functools import partial
from threading import Thread
import threading


class LazyConnection:

    def __init__(self, address, family=AF_INET, sock_type=SOCK_STREAM):
        self.address = address
        self.family = family
        self.sock_type = sock_type
        self._local = threading.local()

    def __enter__(self):
        if hasattr(self._local, "sock"):
            raise RuntimeError("Already connected.")

        self._local.sock = socket(self.family, self.sock_type)
        self._local.sock.connect(self.address)
        return self._local.sock

    def __exit__(self, exc_ty, exc_val, tb):
        if hasattr(self._local, "sock"):
            self._local.sock.close()
            del self._local.sock

def test(conn):
    with conn as s:
        s.send(b'GET /index.html HTTP/1.0\r\n')
        s.send(b'Host: www.python.org\r\n')

        s.send(b'\r\n')
        resp = b''.join(iter(partial(s.recv, 8192), b''))

    print('Got {} bytes'.format(len(resp)))


if __name__ == "__main__":
    conn = LazyConnection(('www.python.org', 80))

    t1 = Thread(target=test, args=(conn,))
    t2 = Thread(target=test, args=(conn,))

    t1.start()
    t2.start()
    t1.join()
    t2.join()