# coding: utf-8
"""
    :date: 2024-01-09
    :author: linshukai
    :description: About fastapi server
"""

from fastapi import FastAPI, WebSocket, Request, Form, WebSocketDisconnect
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import uvicorn
import asyncio

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


class UserForm(BaseModel):
    username: str


# @app.get("/index", response_class=HTMLResponse)
@app.get("/index")
def index(request: Request):
    template_response = templates.TemplateResponse(request=request, name="index.html")
    return template_response


@app.post("/chat", response_class=HTMLResponse)
def post_chat(request: Request, username: str = Form()):
    template_response = templates.TemplateResponse(
        request=request,
        name="chat.html",
        context={"username": username},
    )
    template_response.set_cookie(key="username", value=username)
    return template_response


@app.get("/chat")
def get_chat(request: Request):
    cookies = request.cookies
    print(cookies, type(cookies), cookies.get("username"))
    if not cookies.get("username"):
        return RedirectResponse(url="index")

    username = cookies.get("username")
    return templates.TemplateResponse(
        request=request, name="chat.html", context={"username": username}
    )


class ConnectionManager:
    def __init__(self):
        self.connection = {}

    async def connect(self, client_id: str, websocket: WebSocket):
        await websocket.accept()

        self.connection[client_id] = websocket

    async def disconnect(self, client_id: str, msg: str):
        self.connection.pop(client_id)
        await self.broadcast(client_id, msg)

    async def broadcast(self, client_id: str, msg: str):
        for client, websocket in self.connection.items():
            if client != client_id:
                await websocket.send_text(msg)

    async def send_personal_text(self, client_id, msg: str):
        await self.connection[client_id].send_text(msg)


manager = ConnectionManager()


@app.websocket("/ws/{client_id}")
async def handle_websocket(websocket: WebSocket, client_id: str):
    await manager.connect(client_id, websocket)

    try:
        while True:
            msg = await websocket.receive_text()
            await manager.broadcast(client_id, f"{client_id}: {msg}")
            print(f"Received {client_id}: {msg}")
            await manager.send_personal_text(client_id, f"You: {msg}")

    except WebSocketDisconnect:
        msg = f"System Manager: {client_id} left th chat."
        await manager.disconnect(client_id, msg)


async def server_main():
    config = uvicorn.Config(
        app="server:app", host="0.0.0.0", port=80, ws="websockets", log_level="info"
    )
    server = uvicorn.Server(config)
    await server.serve()


# async def main():
# await asyncio.gather(server_main(), http_server_main())


if __name__ == "__main__":
    asyncio.run(server_main())
