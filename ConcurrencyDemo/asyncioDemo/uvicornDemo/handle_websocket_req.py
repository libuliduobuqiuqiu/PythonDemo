# coding: utf-8
"""
    :date: 2023-12-29
    :author: linshukai
    :description: Asgi Server to handle websocket request
"""


def handle_websocket(scope, receive, send):
    assert scope["type"] == "websocket"
