# -*- coding: utf-8 -*-
from socket import socket, AF_INET, SOCK_STREAM
from threading import Thread
import threading
import time


def echo_handler(sock ,address):
	print("Get Connection from address:", address)

	while True:
		response = sock.recv(8192)
		if not response:
			break
		print("当前运行的线程数量:",len(threading.enumerate()))
		print(f"Got {response}")
		sock.sendall(response)

def echo_server(address, back_log=5):
	sock = socket(AF_INET, SOCK_STREAM)
	sock.bind(address)
	sock.listen(back_log)

	while True:
		sock_client, address = sock.accept()
		thread = Thread(target=echo_handler, args=(sock_client, address))
		thread.start()

if __name__ == "__main__":
	echo_server(('localhost', 5000))

