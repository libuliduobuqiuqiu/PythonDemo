# coding: utf-8
"""
    :date: 2023-12-25
    :author: linshukai
    :description: About Asgi Server
"""
from handle_http_req import handle_http
import asyncio
import uvicorn


async def app(scope, receive, send):
    assert scope["type"] == "http"
    await handle_http(scope, receive, send)


async def main():
    config = uvicorn.Config("asgi_app:app", port=80, log_level="info")
    server = uvicorn.Server(config=config)
    await server.serve()


if __name__ == "__main__":
    asyncio.run(main())
