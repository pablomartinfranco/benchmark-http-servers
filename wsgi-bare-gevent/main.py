from collections.abc import Iterable
from wsgiref.types import StartResponse, WSGIEnvironment

# ruff: noqa: E402
from gevent import monkey

monkey.patch_all()

import json
import time

import gevent
import requests
from gevent import get_hub
from gevent.greenlet import Greenlet
from gevent.pool import Pool
from requests import Response


def worker(n: int) -> None:
    print(f"{n} start")
    time.sleep(1)
    print(f"{n} end")


def application(environ: WSGIEnvironment, start_response: StartResponse) -> Iterable[bytes]:

    print("Hub:", get_hub())
    print("Greenlet:", gevent.getcurrent())

    start = time.perf_counter()
    jobs_1: list[Greenlet[..., None]] = [
        gevent.spawn(worker, 1),
        gevent.spawn(worker, 2),
        gevent.spawn(worker, 3),
    ]
    gevent.joinall(jobs_1)
    print(time.perf_counter() - start)

    jobs_2: list[Greenlet[..., Response]] = [
        gevent.spawn(requests.get, "https://example.com"),
        gevent.spawn(requests.get, "https://example.org"),
    ]
    gevent.joinall(jobs_2)

    pool = Pool(20)
    urls: list[str] = ["https://httpbin.org/get", "https://httpbin.org/get"]
    jobs_3 = [pool.spawn(requests.get, url) for url in urls]
    gevent.joinall(jobs_3)

    body = json.dumps({"hello": "world"}).encode()
    start_response(
        "200 OK",
        [
            ("Content-Type", "application/json"),
            ("Content-Length", str(len(body))),
        ],
    )
    return [body]
