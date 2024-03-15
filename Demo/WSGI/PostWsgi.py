# -*- coding: utf-8 -*-
from wsgiref.simple_server import make_server
from urllib.parse import parse_qs
from faker import Faker
import json


def application(environ, start_response):
    f = Faker()
    headers = [("Content-Type", "application/json")]

    wsgi_input = environ["wsgi.input"]
    try:
        content_length = int(environ.get("CONTENT_LENGTH", 0))
    except (ValueError):
        content_length = 0

    request_body = wsgi_input.read(content_length)
    request_json = json.loads(request_body.decode("utf8"))

    status = "200 OK"
    start_response(status, headers)

    name = request_json.get("name", "")
    user = {"name": name, "address": f.address(), "email": f.email()}
    text = json.dumps(user)
    return [text.encode("utf8")]


with make_server("", 8000, application) as httpd:
    print("Server on port 8000....")
    httpd.serve_forever()