## 背景
关于Python Socket编程，首先需要了解几个计算机网络的知识，通过以下的几个问题，有助于更好的理解Socket编程的意义，以及整个框架方面的知识：

- TCP和UDP协议本质上的区别？
> TCP协议，面向连接，可靠，基于字节流的传输层通信协议；UDP协议无连接，不可靠，基于数据包的传输层协议。<br>
TCP协议在建立连接的过程需要经历三次握手，断开连接则需要经历四次挥手，而这建立连接的过程增加了传输过程中的安全性。
而建立连接的过程则会消耗系统的资源，消耗更多的时间，而相比较UDP协议传输过程则不会出现这种问题。<br>
总结来讲，基于TCP协议传输，需要不断的确认对方是否收到信息，从而建立连接（确认过程次数有限制，即三次握手），UDP协议传输则
不需要确认接收端是否收到信息，只需要将信息发给对方。

- TCP/IP协议栈、HTTP协议、Socket之间的区别和联系？
> TCP/IP协议栈就是一系列网络协议，可以分为四层模型来分析：应用层、传输层、网络层、链路层；<br>
HTTP协议（超文本传输协议）就是在这一协议栈中的应用层协议；HTTP协议简单来说，它的作用就是规范数据的格式，让程序能够方便的识别，并且收发双方都需要遵循同样的协议格式进行数据传输。(应用层的协议也和HTTP协议的作用类似，不一样的是定义不同的数据格式。)<br>
Socket可以理解为TCP/IP协议栈提供的对外的操作接口，即应用层通过网络协议进行通信的接口。Socket可以使用不同的网络协议进行端对端的通信；

- TCP Socket服务器的通信过程？
> Server端：<br>
建立连接（socket()函数创建socket描述符、bind()函数绑定特定的监听地址（ip+port)、listen()函数监听socket、accept()阻塞等待客户端连接）<br>
数据交互（read()函数阻塞等待客户端发送数据、write()函数发送给客户端数据）<br>
Client端：<br>
建立连接（socket()函数创建socket描述符、connect()函数向指定的监听地址发送连接请求）<br>
数据交互（wirte()函数发送服务端数据、read()函数足阻塞等待接受服务端发送的数据）<br>

- socket和websocket之间的联系？
> webosocket是一种通信协议，不同于HTTP请求，客户端请求服务端资源，服务端响应的通信过程；websocket允许服务端主动
向客户端推送消息，同时做到客户端和服务端双向通讯的协议。（具体底层原理有待后面实践，暂时未接触）

- HTTP,WSGI协议的联系和区别？
> HTTP协议（超文本传输协议），属于TCP/IP协议栈中应用层的协议。用于规范传输数据的格式，是一种客户端和服务端传输的规则。<br>
WSGI协议则是Python定义的Web服务器和框架程序通信的接口规则。两者联系不大，强行说的话，Python框架程序主要处理的是HTTP请求。<br>
（后期可以实现一个WSGI协议的Python框架，用于处理HTTP请求的实验。）

- 主流Web框架，异步Web框架？
> 主流Web框架：Django、Flask<br>
> 异步Web框架：Tornado（内置异步模块）、Snaic（Python自带asyncio)、FastAPI（基于Starlette库） 、aiohttp（基于asyncio）

- asyncio，aiohttp之间的联系？（异步编程）
> asyncio是一个异步IO库，aiohttp就是基于asyncio的异步HTTP框架（支持客户端/服务端）

## 代码设计
Python提供了基本的socket模块：
1. socket模块；提供了标准的BSD Sockets API；
2. socketserver模块：提供了服务器中心类，简化服务器的开发；

### TCP Socket服务端
**socket模块：**
```python
# -*- coding: utf-8 -*-
from socket import socket, AF_INET, SOCK_STREAM

def echo_handler(sock ,address):
	print("Get Connection from address:", address)

	while True:
		response = sock.recv(8192)
		if not response:
			break
		print(f"Got {response}")
		sock.sendall(response)

def echo_server(address, back_log=5):
	sock = socket(AF_INET, SOCK_STREAM)
	sock.bind(address)
	sock.listen(back_log)

	while True:
		sock_client, address = sock.accept()
		echo_handler(sock_client, address)

if __name__ == "__main__":
	echo_server(('localhost', 5000))
```

代码详解：
- 创建一个基于IPV4和TCP协议的Socket，这里AF_INET指的是使用IPV4协议，SOCK_STREAM指定使用面向流的TCP协议，绑定监听端口，设置等待连接的最大数量
- 创建一个永久循环，获取客户端请求的连接，accept()会等待并返回一个客户端的连接；
- 连接建立后，等待客户端数据，接受完客户端数据，然后返回数据给客户端，最后关闭连接

存在的问题：当出现多个客户端请求时，由于是单个线程会发生阻塞的情况，所以如果需要多线程处理多个客户端请求，可以这样改；
```python
from threading import Thread

while True:
        client_sock, address = sock.accept()
        thread = Thread(target=echo_handler, args=(client_sock, address))
        thread.start()
```
这样的话，就会在每个客户端请求的时候，生成一个子线程然后处理请求；
（但是存在一个问题：当突然大量请求连接，消耗系统资源达到上限后，很可能造成程序无法处理后续请求。）

**socketserver模块：**
```python
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
```

代码详解：
- 处理多个客户端，初始化一个ThreadingTCPServer实例，ThreadingTCPServer处理客户端的连接，会为每个客户端创建一个线程进行交互。
- 设置绑定的IP地址和端口，以及处理类；
- 可以直接使用BaseRequestHandler，这个所有请求处理类的父类，子类处理请求则需要重写handle()方法，该模块是和服务类组合来处理请求；
- 使用StreamRequestHandler（使用流的请求处理程序类，类似file-like对象，提供标准文件接口简化通信过程），重写里面的handle方法，获取请求数据，返回数据给客户端；
- 使用StreamRequestHandler处理类时，在读取客户端发送的数据，会将recv()多次调用，直到遇到换行符为止，所以客户端在发送数据的末尾需要加上换行符

### TCP Socket客户端
**socket模块：**
```python
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
			# 要在每段发送的内容结尾加上换行符，用于StreamRequestHandler识别	
			sock_client.send((content+"\n").encode())
			time.sleep(1)
			response = sock_client.recv(8192)
			print(response)

	end_time = time.time()
	print("总共耗时:", end_time-start_time)

if __name__ == "__main__":
	request_handler()
```


### UDP Socket
**Socket模块：**
```python
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
```
> 代码不详解，和之前的差不多，注意不同的协议就完事了

客户端测试：
```python
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
```

**socketserver模块：**
```python
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
```
> 代码不在赘述，如果需要多线程处理并发操作可以使用ThreadingUDPServer


### 总结
> 关于本篇介绍Python Socket编程，大都是皮毛，只是谈到了Python实际处理socket的几个模块，
关于socket底层方面的知识并未提及，先了解个大概，从实际使用方面出发，在实际使用过程中结合
计算机网络知识，能够理解socket在整个TCP/IP协议栈中的作用。<br>
socket和socketserver模块都可以用来编写网络程序，不同的是socketserver省事很多，你可以专注
业务逻辑，不用去理会socket的各种细节，包括不限于多线程/多进程，接收数据，发送数据，通信过程。<br>
