# coding: utf-8
"""
    :date: 2023-12-29
    :author: linshuaki
    :description: About websockets demo
    :design: server -> websocket connections -> recv msg -> send message to all websockets
"""

import asyncio
from websockets.server import serve

connections = set()


# chat severice
async def echo(websocket):
    async for message in websocket:
        print(f"Received from ({websocket}): ", message)
        await websocket.send(message)


async def main():
    print("Public Chat Room:")
    async with serve(echo, "localhost", 80) as server:
        await server.wait_closed()


asyncio.run(main())
