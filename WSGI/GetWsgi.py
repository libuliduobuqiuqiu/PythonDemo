# -*- coding: utf-8 -*-

from wsgiref.simple_server import make_server
from cgi import parse_qs, escape


def application(environ, start_response):
    d = parse_qs(environ['QUERY_STRING'])
    path = environ['PATH_INFO']
    name = d.get("name", [])

    headers = [("Content-Type", "text/html")]

    if path not in ["/hello", "/"]:
        status = "404 Not Found"
        html = b"<h1>404</h1>"
        return [html]

    status = "200 OK"
    start_response(status, headers)
    if name:
        name = name[0]
        html = b"<h1> Hello, %s , Welcome to my website.</h1>" % name.encode("utf8")
    else:
        html = b"<h1> Hello, World.</h1>"

    return [html]


with make_server("", 8000, application) as httpd:
    print("Server on 8000 Port......")
    httpd.serve_forever()
