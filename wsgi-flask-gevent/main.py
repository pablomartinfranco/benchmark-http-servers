# ruff: noqa: E402
from gevent import monkey

monkey.patch_all()

import requests
from flask import Flask, jsonify

app = Flask(__name__)


@app.route("/")
def index():

    r = requests.get("https://httpbin.org/get")

    return jsonify(
        server="flask",
        response=r.json(),
    )
