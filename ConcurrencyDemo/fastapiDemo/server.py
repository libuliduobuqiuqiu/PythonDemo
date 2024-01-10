# coding: utf-8
"""
    :date: 2024-01-09
    :author: linshukai
    :description: About fastapi server
"""

from re import L
from fastapi import FastAPI, WebSocket, Request, Form, Response
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from http_server import http_server_main
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
def chat(request: Request, username: str = Form()):
    template_response = templates.TemplateResponse(
        request=request,
        name="chat.html",
        context={"username": username},
    )
    template_response.set_cookie(key="username", value=username)
    return template_response


@app.get("/chat")
def chat(request: Request):
    cookies = request.cookies
    print(cookies, type(cookies), cookies.get("username"))
    if not cookies.get("username"):
        return RedirectResponse(url="index")

    username = cookies.get("username")
    return templates.TemplateResponse(
        request=request, name="chat.html", context={"username": username}
    )


@app.websocket("/{client_id}")
async def handle_websocket(websocket: WebSocket, client_id: str):
    await websocket.accept()

    while True:
        msg = await websocket.receive_text()
        print(f"Received client{client_id}: {msg}")
        await websocket.send_text(f"Message text was {msg}")


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
