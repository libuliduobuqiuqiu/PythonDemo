# coding: utf-8
"""
    :date: 2023-10-23
    :author: linshukai
    :description About Multiprocessing Pipe Demo
"""

from multiprocessing.reduction import recv_handle, send_handle
import multiprocessing
import socket

def worker(in_p, out_p):
    out_p.close()

    while True:
        fd = recv_handle(in_p)

        print("Got Child FD: ", fd)
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM, fileno=fd) as s:
            while True:
                msg = s.recv(1024)
                if not msg:
                    break
                print(f"Child recv: {msg}")
                s.send(msg)


def server(address, in_p, out_p, worker_pid):
    in_p.close()

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)
    s.bind(address)
    s.listen(1)

    while True:
        client, addr = s.accept()
        print("Server: Got Connection from: ", addr)
        send_handle(out_p, client.fileno(), worker_pid)
        client.close()


if __name__ == "__main__":
    c1, c2 = multiprocessing.Pipe()
    worker_p = multiprocessing.Process(target=worker, args=(c1, c2))
    worker_p.start()

    server_p = multiprocessing.Process(target=server, args=(("", 8992), c1, c2, worker_p.pid))
    server_p.start()

    c1.close()
    c2.close()