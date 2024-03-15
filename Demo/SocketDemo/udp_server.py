# -*- coding: utf-8

from socket import socket, AF_INET, SOCK_DGRAM


def echo_handler(address):
	server = socket(AF_INET, SOCK_DGRAM)
	server.bind(address)
	
	while True:
		msg, addr = server.recvfrom(8192)
		if not msg:
			break

		print(f"Got Message From: {addr} \n {msg}")
		server.sendto(msg, addr)

if __name__ == "__main__":
	echo_handler(("", 8888))
		
