# coding: utf-8
"""
    :date: 2023-12-25
    :author: linshukai
    :description: About Asgi Server
"""
from handle_http_req import handle_http
from handle_websocket_req import handle_websocket
import asyncio
import uvicorn


async def app(scope, receive, send):
    if scope["type"] == "http":
        await handle_http(scope, receive, send)
    elif scope["type"] == "websocket":
        await handle_websocket(scope, receive, send)


async def main():
    config = uvicorn.Config("asgi_app:app", port=80, ws="websockets", log_level="info")
    server = uvicorn.Server(config=config)
    await server.serve()


if __name__ == "__main__":
    asyncio.run(main())
