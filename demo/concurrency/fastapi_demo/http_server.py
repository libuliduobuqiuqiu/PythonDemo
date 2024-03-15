# coding: utf-8
"""
    :date: 2024-01-09
    :author: linshukai
    :description: Fastapi framework handle http request
"""

from fastapi import FastAPI, WebSocket
from uvicorn import Config, Server


app = FastAPI()


@app.get("/")
async def hello_world():
    return {"code": 200, "msg": "hello,world"}


async def http_server_main():
    config = Config(app="http_server:app", host="127.0.0.1", port=81, log_level="info")
    server = Server(config)
    await server.serve()
