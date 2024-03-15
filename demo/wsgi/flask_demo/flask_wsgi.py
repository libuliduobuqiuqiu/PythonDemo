# -*- coding: utf-8 -*-
from flask import Flask, request, jsonify
from faker import Faker

app = Flask(__name__)


@app.route("/", methods=["GET"])
def index():
    name = request.args.get("name", "")

    if name:
        return f'<h1>Hello {name}, Welcom to my Website.'
    else:
        return '<h1>Hello,World</h1>'


@app.route("/hello", methods=["POST"])
def hello():
    data = request.json
    name = data.get("name", "")

    if not name:
        response = {
            "ret_code": 500,
            "ret_info": "name 不能为空。"
        }
        return jsonify(response)
    else:
        f = Faker()
        response = {
            "name": name,
            "email": f.email(),
            "address": f.address()
        }
        return jsonify(response)


if __name__ == "__main__":
    app.run("0.0.0.0", port=5000, debug=True)
