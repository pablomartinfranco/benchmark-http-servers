# ruff: noqa: E402
from typing import Any

from gevent import monkey

monkey.patch_all()

import threading
import time
from dataclasses import asdict, is_dataclass

import falcon
import gevent
import orjson
import requests
from falcon import Request, Response
from falcon.media import JSONHandler
from gevent import config, get_hub
from gevent.greenlet import Greenlet

from shared.utils import benchmark, blocking_io, fibonacci, gen_items, hash


class Plain:
    @benchmark(name="plain")
    def on_get(self, req: Request, resp: Response) -> None:
        resp.media = {
            "status": "ok",
        }


class Json_1:
    @benchmark(name="blocking_json")
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
    @benchmark(name="non_blocking_json")
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
    @benchmark(name="blocking_cpu")
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
    @benchmark(name="non_blocking_cpu")
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
    @benchmark(name="blocking_io")
    def on_get(self, req: Request, resp: Response) -> None:

        # start = time.perf_counter()

        blocking_io(id=1)
        blocking_io(id=2)
        blocking_io(id=3)
        blocking_io(id=4)
        blocking_io(id=5)

        # elapsed = time.perf_counter() - start

        resp.media = {
            # "elapsed": f"{elapsed:.6f}s",
            "benchmark": resp.context.benchmark,
        }


class IO_2:
    @benchmark(name="non_blocking_io")
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
    @benchmark(name="blocking_http")
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
    @benchmark(name="non_blocking_http")
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
    @benchmark(name="http_call")
    def on_get(self, req: Request, resp: Response) -> None:

        start = time.perf_counter()

        r = requests.get("https://httpbin.org/get", timeout=10)

        elapsed = time.perf_counter() - start

        is_json = r.headers.get("content-type", "").startswith("application/json")

        # resp.media = r.json()
        resp.media = {
            "status": r.status_code,
            "content_type": r.headers.get("content-type"),
            "body": r.json() if is_json else r.text,
            "elapsed": f"{elapsed:.6f}s",
        }


class Echo:
    @benchmark(name="post_echo")
    def on_post(self, req: Request, resp: Response) -> None:

        start = time.perf_counter()

        data = req.media

        elapsed = time.perf_counter() - start

        resp.media = {
            "received": data,
            "elapsed": f"{elapsed:.6f}s",
        }


class Hash_1:
    @benchmark(name="blocking_hash")
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
    @benchmark(name="non_blocking_hash")
    def on_get(self, req: Request, resp: Response) -> None:

        start = time.perf_counter()

        data = b"x" * 10_000_000

        jobs: list[Greenlet[..., None]] = [
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


def json_default(obj: Any) -> Any:
    if is_dataclass(obj):
        return asdict(obj)  # type: ignore[no-any-return]

    if hasattr(obj, "model_dump"):
        return obj.model_dump()

    if hasattr(obj, "__dict__"):
        return vars(obj)  # type: ignore[no-any-return]

    raise TypeError(f"{type(obj).__name__} is not JSON serializable")


def json_dumps(obj: Any) -> bytes:
    return orjson.dumps(obj, default=json_default)


json_handler = JSONHandler(dumps=json_dumps)


app = falcon.App(  # type: ignore[arg-type]
    media_handlers={"application/json": json_handler}
)

# app = falcon.App()


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
