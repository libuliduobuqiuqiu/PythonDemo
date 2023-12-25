# coding: utf-8
"""
    :date: 2023-12-25
    :author: linshukai
    :description: About Asgi Server
"""
import asyncio
import uvicorn


async def hello_world():
    print("hello")
    await asyncio.sleep(2)
    print("world")

async def hello_task():
    await asyncio.gather(hello_world())


async def app(scope, receive, send):
    assert scope['type'] == 'http'
    print(scope)

    await send({
        "type": "http.response.start",
        "status": 200,
        "headers": [
            [b"content-type", b"text/plain"]
        ]
    })

    await hello_task()

    await send({
        "type": "http.response.body",
        "body": b"hello,world"
    })

if __name__ == "__main__":
    config = uvicorn.Config('asgi_server:app', port=7878, log_level="info")
    server = uvicorn.Server(config=config)
    server.run()
    
