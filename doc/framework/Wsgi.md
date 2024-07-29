## 导语
> 在总结Python项目部署的细节时，粗略的写过有关WSGI协议的内容，接下来这篇讲讲有关WSGI设计思路，以及如何手写一个WSGI的应用程序？

什么是WSGI协议？WSGI的作用？
> WSGI不是Python模块，框架，API，本质来讲就是Web服务器和Web应用程序通信的接口规范，也能理解为提供一个相对简单但全面的接口，用来支持Web服务器和Web应用程序交互；

## WSGI
WSGI协议主要分为Server(服务器)和Application(应用程序)两部分：
- Server（服务器）：从客户端接收请求，将请求传给应用程序处理，然后将应用程序处理后返回的响应，发送给客户端；
- Application（应用程序）：接收从WSGI服务器发送的请求，处理请求，并将处理后的响应结果返回给服务器；

### APPlication(应用程序)
> Application（应用程序）必须是一个可调用的对象（函数，或者是实现了__call__方法的类），接收两个参数，environ（WSGI的环境信息）和start_response（发送HTTP响应请求的函数），应用程序最后需要返回一个iterable，包含单个或者多个bytestring。

```python
def make_app(environ, start_response):
    headers = [("Content-type", "text/html")]
    status = "200 OK"

    start_response(status, headers)
    return [b'<h1>Hello, World</h1>']
```
备注：
- environ变量是包含了环境信息的字典；
- start_response也是一个可调用对象，设置响应请求的状态码和响应头；
- 参数名称不一定要求是environ,start_response,要求服务器传入的是位置参数而非关键字参数；


### Server（服务器）
> Server（服务器）负责解析HTTP请求，并且将请求发送给应用程序处理。Python中有内置的wsgiref模块，可以直接生成一个WSGI服务器（仅供开发测试）。

```python
from wsgiref.simple_server import make_server

with make_server("", 8000, make_app) as httpd:
    print("Server on port 8000......")
    httpd.serve_forever()
```
备注：
- 创建一个WSGI服务器，监听8000端口，指定make_app函数处理请求；
- serve_forever轮询等待请求，直到shutdown()请求；

### 模拟Get/Post请求解析
> 上述简单的模拟Get请求到WSGI服务器，然后返回一个HTML的过程，下面模拟解析Get请求参数，解析Post的json参数

**GET请求解析：**
```
# -*- coding: utf-8 -*-

from wsgiref.simple_server import make_server
from urllib.parse import parse_qs


def application(environ, start_response):
    # 判断是否请求方式是否为GET
    headers = [("Content-Type", "text/html")]
    method = environ['REQUEST_METHOD']
    if method != "GET":
        status = "405 Method Not Allowed"
        start_response(status, headers)
        html = b"<h1>405 Method Not Allowed</h1>"
        return [html]

    # 判断请求路径是否合法
    path = environ['PATH_INFO']
    if path not in ["/hello", "/"]:
        status = "404 Not Found"
        start_response(status, headers)
        html = b"<h1>404</h1>"
        return [html]

    status = "200 OK"
    start_response(status, headers)

    d = parse_qs(environ['QUERY_STRING'])
    name = d.get("name", [])
    if name:
        name = name[0]
        html = b"<h1> Hello, %s , Welcome to my website.</h1>" % name.encode("utf8")
    else:
        html = b"<h1> Hello, World.</h1>"

    return [html]


with make_server("", 8000, application) as httpd:
    print("Server on 8000 Port......")
    httpd.serve_forever()
```
备注：
- 检查environ字典中的REQUEST_METHOD，判断请求方式，如果请求方式不为GET，返回405状态页面；
- 检查environ字典中的PATH_INFO，判断请求路径是否合法，当路径不在预设的列表中，则返回404状态页面；
- 通过parse_qs解析environ字典中的QUER_STRING字符串，判断能否获取对应的请求参数name；

**Post请求解析：**
```python
# -*- coding: utf-8 -*-
from wsgiref.simple_server import make_server
from cgi import parse_qs
from faker import Faker
import json

def application(environ, start_response):
    f = Faker()
    wsgi_input = environ["wsgi.input"]
    
    try:
        content_length = int(environ.get("CONTENT_LENGTH", 0))
    except (ValueError):
        content_length = 0

    request_body = wsgi_input.read(content_length)
    request_json = json.loads(request_body.decode("utf8"))

    
    status = "200 OK"
    headers = [("Content-Type", "application/json")]
    start_response(status, headers)

    name = request_json.get("name", "")
    user = {"name": name,  "address": f.address(), "email": f.email() }
    text = json.dumps(user)
    return [text.encode("utf8")] 
    

with make_server("", 8000, application) as httpd:
    print("Server on port 8000....")
    httpd.serve_forever()
```
备注：
- 模拟POST请求提交json数据，获取提交的json数据需要通过environ字典中的wsgi.input文件，而读取该文件则首先需要获取文件的长度CONTENT_LENGTH;
- 将读取到请求数据，通过json解码成字典，再获取到对应key值，这里通过faker伪造数据模拟通过name查询数据库的过程；
- 最后将得到的信息组成字典，通过json编码成字符串，返回给前端；
- 这里没有对请求方式，请求路径，请求数据是否合法进行校验，单纯的测试POST请求流程；

**总结**
> 其实在上面的示例能感受到，其实一个Web应用，就是通过编写的WSGI处理函数去针对每个HTTP请求进行响应，但是后期随着你要处理
的URL越来越多，这个处理函数代码会越来越庞大，更加难以维护。所以在WSGI接口的基础上，将这些路由选择，请求方式判断等代码抽象，让Web框架去做，开发者只需要专注于业务逻辑代码，流行的Python Web框架Flask，Django就是这样。

## Flask框架
> 这里简单看看Flask框架写一个Web App

```python
# -*- coding: utf-8 -*-
from flask import Flask, request, jsonify
from faker import Faker

app = Flask(__name__)


@app.route("/", methods=["GET"])
def index():
    name = request.args.get("name", "")

    if name:
        return f'<h1>Hello {name}, Welcom to my Website.'
    else:
        return '<h1>Hello,World</h1>'


@app.route("/hello", methods=["POST"])
def hello():
    data = request.json
    name = data.get("name", "")

    if not name:
        response = {
            "ret_code": 500,
            "ret_info": "name 不能为空。"
        }
        return jsonify(response)
    else:
        f = Faker()
        response = {
            "name": name,
            "email": f.email(),
            "address": f.address()
        }
        return jsonify(response)


if __name__ == "__main__":
    app.run("0.0.0.0", port=5000, debug=True)
```
备注：
- 这里处理对应两个URL，分别对应上述WSGI接口解析GET/POST请求；
- 这里面Flask框架通过使用装饰器，将URL和函数关联起来，这样的处理方式既简洁又方便，这样只用关注处理函数中代码逻辑即可；
- 后期可以分析Flask实现WSGI接口的源码，这里按下不表；

## 参考
WSGI规范（PEP3333）
> https://www.python.org/dev/peps/pep-3333/

wsgiref模块官方文档：
> https://docs.python.org/zh-cn/3/library/wsgiref.html?highlight=wsgiref#module-wsgiref

WSGI教程：
> http://wsgi.tutorial.codepoint.net/application-interface
