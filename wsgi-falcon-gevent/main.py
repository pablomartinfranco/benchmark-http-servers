# ruff: noqa: E402
from gevent import monkey

from shared.utils import benchmark, blocking_io, fibonacci, gen_items, hash

monkey.patch_all()

import time

import falcon
import gevent
import requests
from falcon import Request, Response
from gevent.greenlet import Greenlet


class Plain:
    @benchmark
    def on_get(self, req: Request, resp: Response) -> None:
        resp.media = {
            "status": "ok",
        }


class Json_1:
    @benchmark
    def on_get(self, req: Request, resp: Response) -> None:

        start = time.perf_counter()

        items_1 = gen_items(100, id=1)
        items_2 = gen_items(100, id=2)
        items_3 = gen_items(100, id=3)
        items_4 = gen_items(100, id=4)
        items_5 = gen_items(100, id=5)

        elapsed = time.perf_counter() - start

        resp.media = {
            "items": list(items_1 + items_2 + items_3 + items_4 + items_5),
            "elapsed": f"{elapsed:.6f}s",
        }


class Json_2:
    @benchmark
    def on_get(self, req: Request, resp: Response) -> None:

        start = time.perf_counter()

        jobs: list[Greenlet[..., None]] = [
            gevent.spawn(gen_items, n=100, id=1),
            gevent.spawn(gen_items, n=100, id=2),
            gevent.spawn(gen_items, n=100, id=3),
            gevent.spawn(gen_items, n=100, id=4),
            gevent.spawn(gen_items, n=100, id=5),
        ]

        gevent.joinall(jobs)

        elapsed = time.perf_counter() - start

        resp.media = {
            "items": [job.get() for job in jobs],
            "elapsed": f"{elapsed:.6f}s",
        }


class Cpu_1:
    @benchmark
    def on_get(self, req: Request, resp: Response) -> None:

        start = time.perf_counter()

        fibonacci(35, id=1)
        fibonacci(35, id=2)
        fibonacci(35, id=3)
        fibonacci(35, id=4)
        fibonacci(35, id=5)

        elapsed = time.perf_counter() - start

        resp.media = {
            "elapsed": f"{elapsed:.6f}s",
        }


class Cpu_2:
    @benchmark
    def on_get(self, req: Request, resp: Response) -> None:

        start = time.perf_counter()

        jobs: list[Greenlet[..., None]] = [
            gevent.spawn(fibonacci, n=35, id=1),
            gevent.spawn(fibonacci, n=35, id=2),
            gevent.spawn(fibonacci, n=35, id=3),
            gevent.spawn(fibonacci, n=35, id=4),
            gevent.spawn(fibonacci, n=35, id=5),
        ]

        gevent.joinall(jobs)

        elapsed = time.perf_counter() - start

        resp.media = {
            "elapsed": f"{elapsed:.6f}s",
        }


class IO_1:
    @benchmark
    def on_get(self, req: Request, resp: Response) -> None:

        start = time.perf_counter()

        blocking_io(id=1)
        blocking_io(id=2)
        blocking_io(id=3)
        blocking_io(id=4)
        blocking_io(id=5)

        elapsed = time.perf_counter() - start

        resp.media = {
            "elapsed": f"{elapsed:.6f}s",
        }


class IO_2:
    @benchmark
    def on_get(self, req: Request, resp: Response) -> None:

        start = time.perf_counter()

        jobs: list[Greenlet[..., None]] = [
            gevent.spawn(blocking_io, id=1),
            gevent.spawn(blocking_io, id=2),
            gevent.spawn(blocking_io, id=3),
            gevent.spawn(blocking_io, id=4),
            gevent.spawn(blocking_io, id=5),
        ]

        gevent.joinall(jobs)

        elapsed = time.perf_counter() - start

        resp.media = {
            "elapsed": f"{elapsed:.6f}s",
        }


class HTTP_1:
    @benchmark
    def on_get(self, req: Request, resp: Response) -> None:

        start = time.perf_counter()

        resp_1 = requests.get("https://httpbin.org/delay/1")
        resp_2 = requests.get("https://httpbin.org/delay/1")
        resp_3 = requests.get("https://httpbin.org/delay/1")
        resp_4 = requests.get("https://httpbin.org/delay/1")
        resp_5 = requests.get("https://httpbin.org/delay/1")

        responses = [resp_1, resp_2, resp_3, resp_4, resp_5]

        elapsed = time.perf_counter() - start

        resp.media = {
            "responses": [resp.status_code for resp in responses],
            "elapsed": f"{elapsed:.6f}s",
        }


class HTTP_2:
    @benchmark
    def on_get(self, req: Request, resp: Response) -> None:

        start = time.perf_counter()

        jobs: list[Greenlet[..., requests.Response]] = [
            gevent.spawn(requests.get, "https://httpbin.org/delay/1"),
            gevent.spawn(requests.get, "https://httpbin.org/delay/1"),
            gevent.spawn(requests.get, "https://httpbin.org/delay/1"),
            gevent.spawn(requests.get, "https://httpbin.org/delay/1"),
            gevent.spawn(requests.get, "https://httpbin.org/delay/1"),
        ]

        gevent.joinall(jobs)

        elapsed = time.perf_counter() - start

        resp.media = {
            "responses": [job.get().status_code for job in jobs],
            "elapsed": f"{elapsed:.6f}s",
        }


class HTTPCall:
    @benchmark
    def on_get(self, req: Request, resp: Response) -> None:

        start = time.perf_counter()

        r = requests.get("https://httpbin.org/get")

        elapsed = time.perf_counter() - start

        resp.media = r.json()
        resp.media["elapsed"] = f"{elapsed:.6f}s"


class Echo:
    @benchmark
    def on_post(self, req: Request, resp: Response) -> None:

        start = time.perf_counter()

        data = req.media

        elapsed = time.perf_counter() - start

        resp.media = {
            "received": data,
            "elapsed": f"{elapsed:.6f}s",
        }


class Hash_1:
    @benchmark
    def on_get(self, req: Request, resp: Response) -> None:

        start = time.perf_counter()

        data = b"x" * 10_000_000

        dig_1 = hash(data, id=1)
        dig_2 = hash(data, id=2)
        dig_3 = hash(data, id=3)
        dig_4 = hash(data, id=4)
        dig_5 = hash(data, id=5)

        elapsed = time.perf_counter() - start

        resp.media = {
            "sha256": [dig_1, dig_2, dig_3, dig_4, dig_5],
            "elapsed": f"{elapsed:.6f}s",
        }


class Hash_2:
    @benchmark
    def on_get(self, req: Request, resp: Response) -> None:

        start = time.perf_counter()

        data = b"x" * 10_000_000

        jobs: list[Greenlet[..., requests.Response]] = [
            gevent.spawn(hash, data, id=1),
            gevent.spawn(hash, data, id=2),
            gevent.spawn(hash, data, id=3),
            gevent.spawn(hash, data, id=4),
            gevent.spawn(hash, data, id=5),
        ]

        gevent.joinall(jobs)

        elapsed = time.perf_counter() - start

        resp.media = {
            "sha256": [job.get() for job in jobs],
            "elapsed": f"{elapsed:.6f}s",
        }


app = falcon.App()


app.add_route("/plain", Plain())
app.add_route("/json-1", Json_1())
app.add_route("/json-2", Json_2())
app.add_route("/cpu-1", Cpu_1())
app.add_route("/cpu-2", Cpu_2())
app.add_route("/io-1", IO_1())
app.add_route("/io-2", IO_2())
app.add_route("/io/http-1", HTTP_1())
app.add_route("/io/http-2", HTTP_2())
app.add_route("/io/http-call", HTTPCall())
app.add_route("/post/echo", Echo())
app.add_route("/hash-1", Hash_1())
app.add_route("/hash-2", Hash_2())
