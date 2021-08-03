# -*- coding: utf-8 -*-
from wsgiref.simple_server import make_server


def make_app(environ, start_response):
    headers = [("Content-type", "text/html")]
    status = "200 OK"

    start_response(status, headers)
    return (b'<h1>Hello, World</h1>',)


with make_server("", 8000, make_app) as httpd:
    print("Server on port 8000......")
    httpd.serve_forever()