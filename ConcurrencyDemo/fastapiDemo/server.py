# coding: utf-8
"""
    :date: 2024-01-09
    :author: linshukai
    :description: About fastapi server
"""

from fastapi import FastAPI, WebSocket
from http_server import http_server_main
import uvicorn
import asyncio

app = FastAPI()


@app.websocket("/")
async def handle_websocket(websocket: WebSocket):
    await websocket.accept()

    while True:
        msg = await websocket.receive_text()
        print(f"Received client: {msg}")
        await websocket.send_text(f"Message text was {msg}")


async def server_main():
    config = uvicorn.Config(
        app="server:app", host="127.0.0.1", port=80, ws="websockets", log_level="info"
    )
    server = uvicorn.Server(config)
    await server.serve()


async def main():
    await asyncio.gather(server_main(), http_server_main())


if __name__ == "__main__":
    asyncio.run(main())
