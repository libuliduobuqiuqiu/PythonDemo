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
