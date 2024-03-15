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
    connections.add(websocket)
    async for message in websocket:
        print(f"Received from ({websocket}): ", message)
        await broadcast(websocket, message)
        # await websocket.send(message)


async def broadcast(websocket, msg):
    for client in connections:
        if client != websocket:
            print(client, websocket, "diff.")
            await client.send(msg)


async def main():
    print("Public Chat Room:")
    async with serve(echo, "localhost", 80, open_timeout=None) as server:
        await server.wait_closed()


if __name__ == "__main__":
    asyncio.run(main())
