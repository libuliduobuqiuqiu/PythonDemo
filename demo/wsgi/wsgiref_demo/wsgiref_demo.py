# coding: utf-8
"""
    :date: 2023-12-6
    :author: linshukai
    :description: About Use Wsgiref create a WSGIServer
"""

from wsgiref.simple_server import make_server
import json


class MyApp:
    def __init__(self, app_name):
        self._app_name = app_name

    def __call__(self, environ, start_response):
        headers = [("Content-Type", "application/json")]

        if environ["REQUEST_METHOD"] == "GET":
            status = "200 OK"
            start_response(status, headers)
            resp = json.dumps({"error": 0, "msg": f"{self._app_name}: success"}).encode("utf8")
            return [resp]
        else:
            status = "404 NOT FOUND"
            start_response(status, headers)
            resp = json.dumps({"error": 404, "msg": f"{self._app_name}: error"}).encode("utf8")
            return [resp]


if __name__ == "__main__":
    with make_server("", 8000, MyApp("linshukai")) as app:
        app.serve_forever()
