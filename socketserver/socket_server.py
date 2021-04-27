# -*- coding: utf-8 -*-

from socketserver import BaseRequestHandler, StreamRequestHandler
from socketserver import TCPServer, ThreadingTCPServer


class SingleHandler(BaseRequestHandler):
	def handle(self):
		print("Got Connections From: %s" % str(self.client_address))
		
		while True:
			msg = self.request.recv(8192)
			print(f"Got msg: {msg}")
			if not msg:
				break
			self.request.send(msg)

class StreamHandler(StreamRequestHandler):
	def handle(self):
		print("Got Connection From: %s" % str(self.client_address))
		
		for line in self.rfile:
			print(line)
			self.wfile.write(line)


if __name__ == "__main__":
	# server = TCPServer(("", 5000), SingleHandler)
	# server = TCPServer(("", 5000), StreamHandler)
	server = ThreadingTCPServer(("", 5000), StreamHandler)
	server.serve_forever()


