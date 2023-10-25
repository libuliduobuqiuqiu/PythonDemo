# -*- coding: utf-8 -*-

from socket import socket, AF_INET, SOCK_DGRAM
import time


def request_handler(addr):
	client = socket(AF_INET, SOCK_DGRAM)
	
	book_content = ""
	with open("send_books.txt", "r") as f:
		book_content = f.read()

	book_list = book_content.split("\n")
	for content in book_list:
		if content:
			client.sendto(content.encode(), addr)
			response = client.recv(8192)
			print(response)
		time.sleep(1)

if __name__ == "__main__":
	addr = ("localhost", 8888)
	request_handler(addr)
	
