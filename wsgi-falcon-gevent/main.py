# ruff: noqa: E402
from gevent import monkey

monkey.patch_all()

import threading

import falcon
import gevent
import requests
from falcon import Request, Response
from gevent import config, get_hub
from gevent.greenlet import Greenlet

from shared.utils import benchmark, benchmark_scope, blocking_io, fibonacci, gen_items, hash


class Plain:
    @benchmark(name="plain_outer")
    def on_get(self, req: Request, resp: Response) -> None:
        resp.media = {"status": "ok"}


class Json_1:
    @benchmark(name="json_1_outer")
    def on_get(self, req: Request, resp: Response) -> None:

        items_1 = gen_items(100, id=1)
        items_2 = gen_items(100, id=2)
        items_3 = gen_items(100, id=3)
        items_4 = gen_items(100, id=4)
        items_5 = gen_items(100, id=5)

        resp.media = {"items": list(items_1 + items_2 + items_3 + items_4 + items_5)}


class Json_2:
    @benchmark(name="json_2_outer")
    def on_get(self, req: Request, resp: Response) -> None:

        jobs: list[Greenlet[..., None]] = [
            gevent.spawn(gen_items, n=100, id=1),
            gevent.spawn(gen_items, n=100, id=2),
            gevent.spawn(gen_items, n=100, id=3),
            gevent.spawn(gen_items, n=100, id=4),
            gevent.spawn(gen_items, n=100, id=5),
        ]

        gevent.joinall(jobs)

        resp.media = {"items": [job.get() for job in jobs]}


class Cpu_1:
    @benchmark(name="cpu_1_outer")
    def on_get(self, req: Request, resp: Response) -> None:

        with benchmark_scope("cpu_1_inner") as result:
            fibonacci(30, id=1)
            fibonacci(30, id=2)
            fibonacci(30, id=3)
            fibonacci(30, id=4)
            fibonacci(30, id=5)

        resp.media = {
            "status": "ok",
            **result.to_dict(),
        }


class Cpu_2:
    @benchmark(name="cpu_2_outer")
    def on_get(self, req: Request, resp: Response) -> None:

        with benchmark_scope("cpu_2_inner") as result:
            jobs: list[Greenlet[..., int]] = [
                gevent.spawn(fibonacci, n=30, id=1),
                gevent.spawn(fibonacci, n=30, id=2),
                gevent.spawn(fibonacci, n=30, id=3),
                gevent.spawn(fibonacci, n=30, id=4),
                gevent.spawn(fibonacci, n=30, id=5),
            ]

            gevent.joinall(jobs)

        resp.media = {
            "status": "ok",
            **result.to_dict(),
        }


class IO_1:
    @benchmark(name="io_1_outer")
    def on_get(self, req: Request, resp: Response) -> None:

        with benchmark_scope("io_1_inner") as result:
            blocking_io(id=1)
            blocking_io(id=2)
            blocking_io(id=3)
            blocking_io(id=4)
            blocking_io(id=5)

        resp.media = {
            "status": "ok",
            **result.to_dict(),
        }


class IO_2:
    @benchmark(name="io_2_outer")
    def on_get(self, req: Request, resp: Response) -> None:

        with benchmark_scope("io_2_inner") as result:
            jobs: list[Greenlet[..., None]] = [
                gevent.spawn(blocking_io, id=1),
                gevent.spawn(blocking_io, id=2),
                gevent.spawn(blocking_io, id=3),
                gevent.spawn(blocking_io, id=4),
                gevent.spawn(blocking_io, id=5),
            ]

            gevent.joinall(jobs)

        resp.media = {
            "status": "ok",
            **result.to_dict(),
        }


class HTTP_1:
    @benchmark(name="http_1_outer")
    def on_get(self, req: Request, resp: Response) -> None:

        resp_1 = requests.get("https://httpbin.org/delay/1")
        resp_2 = requests.get("https://httpbin.org/delay/1")
        resp_3 = requests.get("https://httpbin.org/delay/1")
        resp_4 = requests.get("https://httpbin.org/delay/1")
        resp_5 = requests.get("https://httpbin.org/delay/1")

        responses = [resp_1, resp_2, resp_3, resp_4, resp_5]

        resp.media = {"responses": [resp.status_code for resp in responses]}


class HTTP_2:
    @benchmark(name="http_2_outer")
    def on_get(self, req: Request, resp: Response) -> None:

        jobs: list[Greenlet[..., requests.Response]] = [
            gevent.spawn(requests.get, "https://httpbin.org/delay/1"),
            gevent.spawn(requests.get, "https://httpbin.org/delay/1"),
            gevent.spawn(requests.get, "https://httpbin.org/delay/1"),
            gevent.spawn(requests.get, "https://httpbin.org/delay/1"),
            gevent.spawn(requests.get, "https://httpbin.org/delay/1"),
        ]

        gevent.joinall(jobs)

        resp.media = {"responses": [job.get().status_code for job in jobs]}


class HTTPCall:
    @benchmark(name="http_call_outer")
    def on_get(self, req: Request, resp: Response) -> None:

        r = requests.get("https://httpbin.org/get", timeout=10)

        is_json = r.headers.get("content-type", "").startswith("application/json")

        # resp.media = r.json()
        resp.media = {
            "status": r.status_code,
            "content_type": r.headers.get("content-type"),
            "body": r.json() if is_json else r.text,
        }


class Echo:
    @benchmark(name="echo_outer")
    def on_post(self, req: Request, resp: Response) -> None:

        data = req.media

        resp.media = {"received": data}


class Hash_1:
    @benchmark(name="hash_1_outer")
    def on_get(self, req: Request, resp: Response) -> None:

        data = b"x" * 10_000_000

        dig_1 = hash(data, id=1)
        dig_2 = hash(data, id=2)
        dig_3 = hash(data, id=3)
        dig_4 = hash(data, id=4)
        dig_5 = hash(data, id=5)

        resp.media = {"sha256": [dig_1, dig_2, dig_3, dig_4, dig_5]}


class Hash_2:
    @benchmark(name="hash_2_outer")
    def on_get(self, req: Request, resp: Response) -> None:

        data = b"x" * 10_000_000

        jobs: list[Greenlet[..., None]] = [
            gevent.spawn(hash, data, id=1),
            gevent.spawn(hash, data, id=2),
            gevent.spawn(hash, data, id=3),
            gevent.spawn(hash, data, id=4),
            gevent.spawn(hash, data, id=5),
        ]

        gevent.joinall(jobs)

        resp.media = {"sha256": [job.get() for job in jobs]}


class GeventInfo:
    def on_get(self, req: Request, resp: Response) -> None:

        hub = get_hub()
        current = gevent.getcurrent()

        resp.media = {
            "gevent": {
                "version": gevent.__version__,
                "hub": {
                    "type": type(hub).__name__,
                    "loop": {
                        "type": type(hub.loop).__name__,
                        "default": hub.loop.default,
                    },
                },
                "current": {
                    "type": type(current).__name__,
                    "repr": repr(current),
                    "is_main": current is gevent.get_hub().parent,
                },
                "config": {
                    "monitor_thread": config.monitor_thread,
                },
            },
            "monkey_patch": {
                "socket": monkey.is_module_patched("socket"),
                "ssl": monkey.is_module_patched("ssl"),
                "threading": monkey.is_module_patched("threading"),
                "select": monkey.is_module_patched("select"),
                "time": monkey.is_module_patched("time"),
                "subprocess": monkey.is_module_patched("subprocess"),
            },
            "python": {
                "thread": {
                    "name": threading.current_thread().name,
                    "ident": threading.current_thread().ident,
                }
            },
        }


class GeventYield:
    def on_get(self, req: Request, resp: Response) -> None:

        events: list[str] = []

        def worker(id: int) -> None:
            events.append(f"{id}-start")
            gevent.sleep(0)
            events.append(f"{id}-end")

        jobs: list[Greenlet[..., None]] = [
            gevent.spawn(worker, 1),
            gevent.spawn(worker, 2),
            gevent.spawn(worker, 3),
        ]

        gevent.joinall(jobs)

        resp.media = {
            "events": events,
            "greenlets": len(jobs),
        }


app = falcon.App()


app.add_route("/plain", Plain())
app.add_route("/json-1", Json_1())
app.add_route("/json-2", Json_2())
app.add_route("/cpu-1", Cpu_1())
app.add_route("/cpu-2", Cpu_2())
app.add_route("/io-1", IO_1())
app.add_route("/io-2", IO_2())
app.add_route("/http-1", HTTP_1())
app.add_route("/http-2", HTTP_2())
app.add_route("/http-call", HTTPCall())
app.add_route("/echo", Echo())
app.add_route("/hash-1", Hash_1())
app.add_route("/hash-2", Hash_2())
app.add_route("/gevent-info", GeventInfo())
app.add_route("/gevent-yield", GeventYield())
