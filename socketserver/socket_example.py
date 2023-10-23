# coding: utf-8

"""
    :date: 2023-10-19
    :author: linshukai
    :description: About SocketServer Example
"""
import time
import socket
from socketserver import BaseRequestHandler, StreamRequestHandler, TCPServer, UDPServer


class EchoHandler(BaseRequestHandler):
    def handle(self) -> None:

        print(f"Got Connection from {self.client_address}")

        while True:
            msg = self.request.recv(8192)
            print(f"Go msg: {msg}")
            if not msg:
                break

            self.request.send(msg)


class StreamEchoHandler(StreamRequestHandler):
    timeout = 5

    def handle(self) -> None:
        print(f"Got Connection from {self.client_address}")

        try:
            for line in self.rfile:
                print(f"Got msg: {line}")
                self.wfile.write(line)
        except socket.timeout:
            print("Sock Timeout.")


class UdpEchoHandler(BaseRequestHandler):
    def handle(self) -> None:
        msg, sock = self.request
        resp = time.ctime()
        sock.sendto(resp.encode("ascii"), self.client_address)


if __name__ == "__main__":
    server = UDPServer(("", 8992), UdpEchoHandler)
    server.serve_forever()
