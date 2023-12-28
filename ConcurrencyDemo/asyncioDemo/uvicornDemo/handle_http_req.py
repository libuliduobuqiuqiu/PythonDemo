# coding: utf-8
"""
    :date: 2023-12-28
    :author: linshukai
    :description: handle http request base on asgi protocol
"""


"""
    reference tutorial: https://www.cnblogs.com/hanabi-cnblogs/p/17792740.html
"""

from functools import partial
import asyncio
import json
import re

PERSON_INFO = {}
CAR_INFO = {}


def get_info(query_string, storage_data):
    name_info = re.search(r"name=(?P<name>\w+)", query_string)
    if name_info:
        name = name_info.groupdict()["name"]
        return storage_data.get(name, "")


def post_info(body, storage_data):
    data = json.loads(str(body))

    name = data.get("name")
    info = data.get("info")

    if not name or not info:
        return "name or info cannot be empty. "

    if name in storage_data:
        return "name is exist."

    storage_data[name] = info


async def handle_get(url, query_string, send):
    err_msg = {"code": 500, "error": ""}
    url_dict = {
        "person_info": partial(get_info, storage_data=PERSON_INFO),
        "car_info": partial(get_info, storage_data=CAR_INFO),
    }

    request_template = {
        "type": "http.request.start",
        "code": "",
        "headers": [[b"content-type", b"application/json"]],
    }

    if url in url_dict:
        fn = url_dict[url]
        result = fn(query_string)

        if result:
            request_template["code"] = 200
            await send(request_template)

            await send(
                {
                    "type": "http.request.body",
                    "body": json.dumps(
                        {"code": "200", "error": "", "data": result}
                    ).encode("utf-8"),
                }
            )
        else:
            request_template["code"] = 500
            await send(request_template)

            err_msg["error"] = "Query String Not Found"
            await send(
                {
                    "type": "http.request.body",
                    "body": json.dumps(err_msg).encode("utf-8"),
                }
            )
    else:
        request_template["code"] = 404
        await send(request_template)


async def handle_post(url, receive, send):
    error_msg = {"code": 500, "error": ""}
    url_dict = {
        "person_info": partial(post_info, storage_data=PERSON_INFO),
        "car_info": partial(post_info, storage_data=CAR_INFO),
    }
    request_template = {
        "type": "http.request.start",
        "code": "",
        "headers": [[b"content-type", b"application/json"]],
    }

    if url in url_dict:
        msg = await receive()
        body = msg.get("body", b"")
        result = url_dict[url](body)

        if result:
            request_template["code"] = "500"
            await send(request_template)

            error_msg["error"] = result
            error_body = json.dumps(error_msg).encode("utf-8")
            await send({"type": "http.request.body", "body": error_body})
        else:
            request_template["code"] = "200"
            await send(request_template)

            await send(
                {
                    "type": "http.request.body",
                    "body": json.dumps({"code": 200, "error": ""}).encode("utf-8"),
                }
            )

        return
    else:
        request_template["code"] = 404
        await send(request_template)


async def handle_http(scope, receive, send):
    print(scope)

    asgi_info = scope["asgi"]
    req_method = asgi_info["method"]
    req_path = asgi_info["path"]
    req_query_string = asgi_info["query_string"]

    if req_method == "GET":
        await handle_get(req_path, req_query_string, send)
        return
    elif req_method == "POST":
        await handle_post(req_path, receive, send)
        return
    else:
        await send(
            {
                "type": "http.request.start",
                "code": 404,
                "headers": [[b"content-type", b"text/plain"]],
            }
        )
        return
