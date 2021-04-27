# -*- coding: utf-8 -*-
from socket import socket, AF_INET, SOCK_STREAM
import time

def request_handler():
	start_time = time.time()
	sock_client = socket(AF_INET, SOCK_STREAM)
	sock_client.connect(('localhost', 5000))
	
	book_content = ""
	with open("send_books.txt", "r") as f:
		book_content = f.read()
	
	content_list = book_content.split("\n")
	for content in content_list:
		if content:
			sock_client.send((content).encode())
			time.sleep(2)
			response = sock_client.recv(8192)
			print(response)

	end_time = time.time()
	print("总共耗时:", end_time-start_time)

		

if __name__ == "__main__":
	request_handler()

