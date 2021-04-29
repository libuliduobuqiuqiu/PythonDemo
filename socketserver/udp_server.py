# -*- coding: utf-8 -*-

from socketserver import BaseRequestHandler, UDPServer


class EchoHandler(BaseRequestHandler):

	def handle(self):
		print(f"Got Connections From: {self.client_address}")	

		data, sock = self.request
		print(data)

		if data:
			sock.sendto(data, self.client_address)

if __name__ == "__main__":
	server = UDPServer(("", 8888), EchoHandler)
	server.serve_forever()	
