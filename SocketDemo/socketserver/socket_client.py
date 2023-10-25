# coding: utf-8

"""
    :date: 2023-10-19
    :author: linshukai
    :description: About SocketDemo client
"""

from socket import AF_INET, SOCK_STREAM, SOCK_DGRAM
from socket import socket

from xmlrpc.client import ServerProxy


def xml_rpc_client():
    client = ServerProxy("http://127.0.0.1:9992", allow_none=True)
    client.set("name", "linshukai")
    client.set("age", 22)
    print(client.keys())
    try:
        print(client.get("name"), client.get("address"))
    except Exception as e:
        print(e)

    client.set("address", "GuangDong DongGuan")
    print(client.exists("address"))
    print(client.get("address"))


def udp_client():
    s = socket(AF_INET, SOCK_DGRAM)
    s.connect(("localhost", 8992))

    s.send(b'hello,world\nSocketDemo demo')
    msg = s.recv(8192)
    print(f"Got msg: {msg}")
    s.close()


if __name__ == "__main__":
    xml_rpc_client()
