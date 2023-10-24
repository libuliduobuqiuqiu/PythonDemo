# coding: utf-8
"""
    :date: 2023-10-24
    :author: linshukai
    :description: About ThreadPoolExecutor Demo
"""

from concurrent.futures import ThreadPoolExecutor
from socket import AF_INET, SOCK_STREAM, socket


def echo_client(sock, client_address):
    print("Got Connection ", client_address)

    while True:

        msg = sock.recv(65535)
        if not msg:
            break
        sock.sendall(msg)

    print("Close Connection ", client_address)
    sock.close()


def echo_server(address):
    pool = ThreadPoolExecutor(128)

    sock = socket(AF_INET, SOCK_STREAM)
    sock.bind(address)
    print('Server Listening.....')
    sock.listen(5)

    while True:
        client_sock, client_address = sock.accept()
        pool.submit(echo_client, client_sock, client_address)


if __name__ == "__main__":
    echo_server(("", 8992))

