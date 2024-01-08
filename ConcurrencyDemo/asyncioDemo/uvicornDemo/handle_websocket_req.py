# coding: utf-8
"""
    :date: 2023-12-29
    :author: linshukai
    :description: Asgi Server to handle websocket request
"""


async def handle_websocket(scope, receive, send):
    assert scope["type"] == "websocket"
    print(scope)

    msg = await receive()

    await send({"type": "websocket.accept", "headers": []})

    receive_msg = await receive()
    data = receive_msg["bytes"]

    while data:
        await send(
            {
                "type": "websocket.send",
                "bytes": f"Server Got: {str(data)}".encode("utf-8"),
            }
        )
        receive_msg = await receive()
        data = receive_msg["bytes"]

    await send({"type": "websocket.close", "headers": []})
