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

async def print_hello():
    task = asyncio.create_task(hello_world())
    await task



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

    # await print_hello()
    
    for chunk in [b'hello', b'', b'world']:
        await send({
            "type": "http.response.body",
            "body": chunk,
            "more_body": True
        })
        await asyncio.sleep(1)

    await send({
        "type": "http.response.body",
        "body": b"start"
    })

async def main():
    config = uvicorn.Config('asgi_server:app', port=80, log_level="info")
    server = uvicorn.Server(config=config)
    await server.serve()

if __name__ == "__main__":
    asyncio.run(main())
