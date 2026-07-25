# PROJECT TREE

```text
.
├── auto-cpanel
│   └── passenger_wsgi.py
├── shared
│   └── utils.py
├── wsgi-bare
│   ├── deploy.sh
│   ├── main.py
│   └── passenger_wsgi.py
├── wsgi-bare-gevent
│   ├── deploy.sh
│   ├── main.py
│   └── passenger_wsgi.py
├── wsgi-falcon
│   ├── deploy.sh
│   ├── main.py
│   └── passenger_wsgi.py
├── wsgi-falcon-gevent
│   ├── deploy.sh
│   ├── logs.sh
│   ├── main.py
│   ├── passenger_wsgi.py
│   └── requirements.txt
├── wsgi-fastapi
│   ├── deploy.sh
│   ├── main.py
│   └── passenger_wsgi.py
├── wsgi-flask
│   ├── deploy.sh
│   ├── main.py
│   └── passenger_wsgi.py
├── wsgi-flask-gevent
│   ├── deploy.sh
│   ├── main.py
│   └── passenger_wsgi.py
├── deploy.sh
├── Justfile
└── pyproject.toml
```

# PYTHON FILE CONTENTS


# FILE: auto-cpanel\passenger_wsgi.py

```python
import os
import pprint
import sys

sys.path.insert(0, os.path.dirname(__file__))


def application(environ, start_response):  # type: ignore[no-untyped-def]
    body = pprint.pformat(dict(environ))  # type: ignore[no-untyped-call]
    message = "It works!\n"
    version = f"Python {sys.version.split()[0]}\n"
    response = "\n".join([body, message, version]).encode()
    content_length = str(len(response))
    start_response("200 OK", [("Content-Type", "text/plain"), ("Content-Length", content_length)])
    return [response]

```


# FILE: deploy.sh

```python
#!/usr/bin/env bash
set -e

cd "$(dirname "$0")"

git fetch origin
git reset --hard origin/main

source ~/virtualenv/opt/stonks.0a.com.ar/stonks-api-python/3.11/bin/activate

pip install --upgrade pip
pip list --format=freeze | grep -vE '^(pip|setuptools|wheel)==' | cut -d= -f1 | xargs -r pip uninstall -y
pip install -e .

mkdir -p tmp
touch tmp/restart.txt

# Enter to the virtual environment.
# To enter to virtual environment, run the command: 
# source /home/alphalab/virtualenv/opt/stonks.0a.com.ar/stonks-api-python/3.11/bin/activate && cd /home/alphalab/opt/stonks.0a.com.ar/stonks-api-python

```


# FILE: pyproject.toml

```python
[project]
name = "stonks-api-python"
version = "0.1.0"
description = "Add your description here"
readme = "README.md"
requires-python = ">=3.11"
dependencies = [
    "attrs>=26.1.0",
    "httpx>=0.28.1",
    "pydantic>=2.10.6",
    "a2wsgi>=1.10.10",
    "fastapi[all]>=0.124.4",
    "uvicorn[standard]>=0.33.0",
    'uvloop>=0.21.0; platform_system != "Windows"',
    "gunicorn>=26.0.0",
    "aiohttp>=3.14.1",
    "blacksheep>=2.6.3",
    "falcon>=4.3.1",
    "sanic[all]>=25.12.1",
    "daphne>=4.2.2",
    "hypercorn>=0.18.0",
    "litestar[pydantic,standard]>=2.24.0",
    "quart>=0.20.0",
    "gevent>=26.5.0",
    "requests>=2.34.2",
    "psutil>=7.2.2",
    "orjson>=3.11.9",
]

[dependency-groups]
dev = [
    "mypy>=1.14.1",
    "pytest>=8.3.5",
    "pytest-asyncio>=0.24.0",
    "rich>=14.3.4",
    "ruff>=0.15.11",
    "typer>=0.20.1",
]

[project.optional-dependencies]
opt = [
]

[tool.pytest.ini_options]
asyncio_mode = "auto"
pythonpath = ["src"]

[tool.ruff]
line-length = 100
target-version = "py311"

[tool.ruff.lint]
select = ["E", "F", "I", "UP", "B", "SIM"]
ignore = ["E501", "B008"]  # optional (line length handled elsewhere)

[tool.ruff.format]
quote-style = "double"
indent-style = "space"

[tool.mypy]
python_version = "3.11"
strict = true
plugins = ["pydantic.mypy"]

mypy_path = "src"
explicit_package_bases = true
warn_unused_ignores = true
warn_return_any = true

# disallow_untyped_defs = true
# check_untyped_defs = true
# no_implicit_optional = true

[[tool.mypy.overrides]]
module = ["jose.*", "passlib.*"]
ignore_missing_imports = true

```


# FILE: shared\utils.py

```python
from __future__ import annotations

import hashlib
import os
import time
import tracemalloc
from collections.abc import Callable, Generator
from contextlib import contextmanager
from dataclasses import asdict, dataclass
from functools import wraps
from typing import Any

import psutil

# Initialize once when the application starts.
# Do not start/stop tracemalloc on every request.
tracemalloc.start()


@dataclass(slots=True)
class BenchmarkResult:
    elapsed: float = 0.0
    cpu_time: float = 0.0
    memory: int = 0
    voluntary_switches: int = 0
    involuntary_switches: int = 0

    def to_dict(self):
        return asdict(self)


@contextmanager
def benchmark_scope(name: str) -> Generator[BenchmarkResult, None, None]:

    process = psutil.Process(os.getpid())
    # print(f"\nos pid={os.getpid()} psutil pid={process.pid}", flush=True)

    start_wall = time.perf_counter_ns()
    start_cpu = time.process_time_ns()

    start_memory, _ = tracemalloc.get_traced_memory()
    start_context = process.num_ctx_switches()

    result = BenchmarkResult()

    try:
        yield result

    finally:
        end_wall = time.perf_counter_ns()
        end_cpu = time.process_time_ns()
        end_memory, _ = tracemalloc.get_traced_memory()
        end_context = process.num_ctx_switches()

        result.elapsed = (end_wall - start_wall) / 1_000_000_000
        result.cpu_time = (end_cpu - start_cpu) / 1_000_000_000
        result.memory = end_memory - start_memory

        # print(f"\nbefore end: os={os.getpid()} psutil={process.pid}", flush=True)
        result.voluntary_switches = end_context.voluntary - start_context.voluntary
        result.involuntary_switches = end_context.involuntary - start_context.involuntary

        print(
            f"\n{name}:\n"
            f"  wall={result.elapsed:.6f}s\n"
            f"  cpu ={result.cpu_time:.6f}s\n"
            f"  mem ={result.memory / 1024:.2f}KB\n"
            f"  ctx ={result.voluntary_switches} voluntary "
            f"{result.involuntary_switches} involuntary",
            flush=True,
        )


def benchmark(
    func: Callable[..., Any] | None = None, *, name: str | None = None
) -> Callable[..., Any]:

    def decorator(target: Callable[..., Any]) -> Callable[..., Any]:

        @wraps(target)
        def wrapper(*args: Any, **kwargs: Any) -> Any:

            with benchmark_scope(name or target.__name__):
                return target(*args, **kwargs)

        return wrapper

    if func is not None:
        return decorator(func)

    return decorator


def blocking_io(id: int | None = None) -> None:
    time.sleep(1)
    _ = id and print(f"\nid = {id}")


def fibonacci(n: int, id: int | None = None) -> int:
    def fibo(n: int) -> int:
        return n if n <= 1 else fibonacci(n - 1, id=None) + fibonacci(n - 2, id=None)

    fib = fibo(n)
    _ = id and print(f"\nid = {id}")
    return fib


def gen_items(n: int = 1000, id: int | None = None) -> list[dict[str, Any]]:
    items: list[dict[str, Any]] = [
        {
            "id": f"{id}-{i}" if id is not None else f"{i}",
            "name": f"user-{i}",
            "active": True,
        }
        for i in range(n)
    ]
    _ = id and print(f"\nid = {id}")
    return items


def hash(data: bytes, id: int | None = None) -> str:

    result = hashlib.sha256(data).hexdigest()
    _ = id and print(f"\nid = {id}")
    return result

```


# FILE: wsgi-bare\deploy.sh

```python
#!/usr/bin/env bash
set -e

cd "$(dirname "$0")"

git fetch origin
git reset --hard origin/main

source ~/virtualenv/opt/stonks.0a.com.ar/stonks-api-python/3.11/bin/activate

pip install --upgrade pip
pip list --format=freeze | grep -vE '^(pip|setuptools|wheel)==' | cut -d= -f1 | xargs -r pip uninstall -y
pip install -e .

mkdir -p tmp
touch tmp/restart.txt

# Enter to the virtual environment.
# To enter to virtual environment, run the command: 
# source /home/alphalab/virtualenv/opt/stonks.0a.com.ar/stonks-api-python/3.11/bin/activate && cd /home/alphalab/opt/stonks.0a.com.ar/stonks-api-python

```


# FILE: wsgi-bare\main.py

```python
from collections.abc import Iterable
from wsgiref.types import StartResponse, WSGIEnvironment


def application(environ: WSGIEnvironment, start_response: StartResponse) -> Iterable[bytes]:
    body = b"OK"
    start_response(
        "200 OK",
        [
            ("Content-Type", "text/plain"),
            ("Content-Length", str(len(body))),
        ],
    )
    return [body]

```


# FILE: wsgi-bare\passenger_wsgi.py

```python
from wsgiref.types import WSGIApplication

from main import application

application: WSGIApplication = application

```


# FILE: wsgi-bare-gevent\deploy.sh

```python
#!/usr/bin/env bash
set -e

cd "$(dirname "$0")"

git fetch origin
git reset --hard origin/main

source ~/virtualenv/opt/stonks.0a.com.ar/stonks-api-python/3.11/bin/activate

pip install --upgrade pip
pip list --format=freeze | grep -vE '^(pip|setuptools|wheel)==' | cut -d= -f1 | xargs -r pip uninstall -y
pip install -e .

mkdir -p tmp
touch tmp/restart.txt

# Enter to the virtual environment.
# To enter to virtual environment, run the command: 
# source /home/alphalab/virtualenv/opt/stonks.0a.com.ar/stonks-api-python/3.11/bin/activate && cd /home/alphalab/opt/stonks.0a.com.ar/stonks-api-python

```


# FILE: wsgi-bare-gevent\main.py

```python
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

```


# FILE: wsgi-bare-gevent\passenger_wsgi.py

```python
from wsgiref.types import WSGIApplication

from main import application

application: WSGIApplication = application

```


# FILE: wsgi-falcon\deploy.sh

```python
#!/usr/bin/env bash
set -e

cd "$(dirname "$0")"

git fetch origin
git reset --hard origin/main

source ~/virtualenv/opt/stonks.0a.com.ar/stonks-api-python/3.11/bin/activate

pip install --upgrade pip
pip list --format=freeze | grep -vE '^(pip|setuptools|wheel)==' | cut -d= -f1 | xargs -r pip uninstall -y
pip install -e .

mkdir -p tmp
touch tmp/restart.txt

# Enter to the virtual environment.
# To enter to virtual environment, run the command: 
# source /home/alphalab/virtualenv/opt/stonks.0a.com.ar/stonks-api-python/3.11/bin/activate && cd /home/alphalab/opt/stonks.0a.com.ar/stonks-api-python

```


# FILE: wsgi-falcon\main.py

```python
import falcon
from falcon import Request, Response


class HealthResource:
    def on_get(self, req: Request, resp: Response):
        resp.media = {
            "server": "falcon",
            "runtime": "passenger",
        }


app = falcon.App()

app.add_route("/", HealthResource())

```


# FILE: wsgi-falcon\passenger_wsgi.py

```python
from wsgiref.types import WSGIApplication

from main import app

application: WSGIApplication = app

```


# FILE: wsgi-falcon-gevent\deploy.sh

```python
#!/usr/bin/env bash
set -e

cd "$(dirname "$0")"

source ~/virtualenv/web/0a/wsgi-falcon-gevent.0a.com.ar/3.11/bin/activate

pip install --upgrade pip
pip list --format=freeze | grep -vE '^(pip|setuptools|wheel)==' | cut -d= -f1 | xargs -r pip uninstall -y
pip install -r requirements.txt

mkdir -p tmp
touch tmp/restart.txt

# Enter to the virtual environment.
# To enter to virtual environment, run the command: 
# source ~/virtualenv/web/0a/wsgi-falcon-gevent.0a.com.ar/3.11/bin/activate && cd ~/web/0a/wsgi-falcon-gevent.0a.com.ar

```


# FILE: wsgi-falcon-gevent\logs.sh

```python
#!/usr/bin/env bash
set -euo pipefail

tail -F ~/web/0a/wsgi-falcon-gevent.0a.com.ar/stderr.log

# tail -F \
#     "$SCRIPT_DIR/web/0a/wsgi-falcon-gevent.0a.com.ar/stderr.log" \
#     "$SCRIPT_DIR/web/0a/wsgi-falcon-gevent.0a.com.ar/stdout.log"
```


# FILE: wsgi-falcon-gevent\main.py

```python
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
        with benchmark_scope("cpu_1_inner") as result:
            ...
        resp.media = {
            "data": "ok",
            **result.to_dict(),
        }


class Json_1:
    @benchmark(name="json_1_outer")
    def on_get(self, req: Request, resp: Response) -> None:
        with benchmark_scope("cpu_1_inner") as result:
            items_1 = gen_items(100, id=1)
            items_2 = gen_items(100, id=2)
            items_3 = gen_items(100, id=3)
            items_4 = gen_items(100, id=4)
            items_5 = gen_items(100, id=5)

        resp.media = {
            "data": list(items_1 + items_2 + items_3 + items_4 + items_5),
            **result.to_dict(),
        }


class Json_2:
    @benchmark(name="json_2_outer")
    def on_get(self, req: Request, resp: Response) -> None:

        with benchmark_scope("cpu_1_inner") as result:
            jobs: list[Greenlet[..., None]] = [
                gevent.spawn(gen_items, n=100, id=1),
                gevent.spawn(gen_items, n=100, id=2),
                gevent.spawn(gen_items, n=100, id=3),
                gevent.spawn(gen_items, n=100, id=4),
                gevent.spawn(gen_items, n=100, id=5),
            ]
            gevent.joinall(jobs)

        resp.media = {
            "data": [job.get() for job in jobs],
            **result.to_dict(),
        }


class Cpu_1:
    @benchmark(name="cpu_1_outer")
    def on_get(self, req: Request, resp: Response) -> None:

        with benchmark_scope("cpu_1_inner") as result:
            fibonacci(31, id=1)
            fibonacci(31, id=2)
            fibonacci(31, id=3)
            fibonacci(31, id=4)
            fibonacci(31, id=5)

        resp.media = {
            "data": "ok",
            **result.to_dict(),
        }


class Cpu_2:
    @benchmark(name="cpu_2_outer")
    def on_get(self, req: Request, resp: Response) -> None:

        with benchmark_scope("cpu_2_inner") as result:
            jobs: list[Greenlet[..., int]] = [
                gevent.spawn(fibonacci, n=31, id=1),
                gevent.spawn(fibonacci, n=31, id=2),
                gevent.spawn(fibonacci, n=31, id=3),
                gevent.spawn(fibonacci, n=31, id=4),
                gevent.spawn(fibonacci, n=31, id=5),
            ]
            gevent.joinall(jobs)

        resp.media = {
            "data": "ok",
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
            "data": "ok",
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
            "data": "ok",
            **result.to_dict(),
        }


class HTTP_1:
    @benchmark(name="http_1_outer")
    def on_get(self, req: Request, resp: Response) -> None:

        with benchmark_scope("http_1_inner") as result:
            resp_1 = requests.get("https://httpbin.org/delay/1")
            resp_2 = requests.get("https://httpbin.org/delay/1")
            resp_3 = requests.get("https://httpbin.org/delay/1")
            resp_4 = requests.get("https://httpbin.org/delay/1")
            resp_5 = requests.get("https://httpbin.org/delay/1")
            responses = [resp_1, resp_2, resp_3, resp_4, resp_5]

        resp.media = {
            "data": [resp.status_code for resp in responses],
            **result.to_dict(),
        }


class HTTP_2:
    @benchmark(name="http_2_outer")
    def on_get(self, req: Request, resp: Response) -> None:

        with benchmark_scope("http_2_inner") as result:
            jobs: list[Greenlet[..., requests.Response]] = [
                gevent.spawn(requests.get, "https://httpbin.org/delay/1"),
                gevent.spawn(requests.get, "https://httpbin.org/delay/1"),
                gevent.spawn(requests.get, "https://httpbin.org/delay/1"),
                gevent.spawn(requests.get, "https://httpbin.org/delay/1"),
                gevent.spawn(requests.get, "https://httpbin.org/delay/1"),
            ]
            gevent.joinall(jobs)

        resp.media = {
            "data": [job.get().status_code for job in jobs],
            **result.to_dict(),
        }


class HTTPCall:
    @benchmark(name="http_call_outer")
    def on_get(self, req: Request, resp: Response) -> None:

        with benchmark_scope("http_call_inner") as result:
            r = requests.get("https://httpbin.org/get", timeout=10)

            is_json = r.headers.get("content-type", "").startswith("application/json")

        # resp.media = r.json()
        resp.media = {
            "status": r.status_code,
            "content_type": r.headers.get("content-type"),
            "body": r.json() if is_json else r.text,
            **result.to_dict(),
        }


class Echo:
    @benchmark(name="echo_outer")
    def on_post(self, req: Request, resp: Response) -> None:

        with benchmark_scope("echo_inner") as result:
            data = req.media

        resp.media = {
            "data": data,
            **result.to_dict(),
        }


class Hash_1:
    @benchmark(name="hash_1_outer")
    def on_get(self, req: Request, resp: Response) -> None:

        with benchmark_scope("hash_1_inner") as result:
            data = b"x" * 10_000_000
            dig_1 = hash(data, id=1)
            dig_2 = hash(data, id=2)
            dig_3 = hash(data, id=3)
            dig_4 = hash(data, id=4)
            dig_5 = hash(data, id=5)

        resp.media = {
            "sha256": [dig_1, dig_2, dig_3, dig_4, dig_5],
            **result.to_dict(),
        }


class Hash_2:
    @benchmark(name="hash_2_outer")
    def on_get(self, req: Request, resp: Response) -> None:

        with benchmark_scope("hash_2_inner") as result:
            data = b"x" * 10_000_000
            jobs: list[Greenlet[..., None]] = [
                gevent.spawn(hash, data, id=1),
                gevent.spawn(hash, data, id=2),
                gevent.spawn(hash, data, id=3),
                gevent.spawn(hash, data, id=4),
                gevent.spawn(hash, data, id=5),
            ]
            gevent.joinall(jobs)

        resp.media = {
            "sha256": [job.get() for job in jobs],
            **result.to_dict(),
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
    @benchmark(name="gevent_yield_outer")
    def on_get(self, req: Request, resp: Response) -> None:

        with benchmark_scope("gevent_yield_inner") as result:
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
            **result.to_dict(),
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

```


# FILE: wsgi-falcon-gevent\passenger_wsgi.py

```python
# ruff: noqa: E402
import sys

sys.stdout = sys.stderr

from wsgiref.types import WSGIApplication

from main import app

application: WSGIApplication = app

```


# FILE: wsgi-falcon-gevent\requirements.txt

```python
falcon
gevent
requests
psutil
orjson
```


# FILE: wsgi-fastapi\deploy.sh

```python
#!/usr/bin/env bash
set -e

cd "$(dirname "$0")"

git fetch origin
git reset --hard origin/main

source ~/virtualenv/opt/stonks.0a.com.ar/stonks-api-python/3.11/bin/activate

pip install --upgrade pip
pip list --format=freeze | grep -vE '^(pip|setuptools|wheel)==' | cut -d= -f1 | xargs -r pip uninstall -y
pip install -e .

mkdir -p tmp
touch tmp/restart.txt

# Enter to the virtual environment.
# To enter to virtual environment, run the command: 
# source /home/alphalab/virtualenv/opt/stonks.0a.com.ar/stonks-api-python/3.11/bin/activate && cd /home/alphalab/opt/stonks.0a.com.ar/stonks-api-python

```


# FILE: wsgi-fastapi\main.py

```python
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def index():
    return {
        "server": "fastapi",
        "adapter": "a2wsgi",
    }

```


# FILE: wsgi-fastapi\passenger_wsgi.py

```python
from typing import cast
from wsgiref.types import WSGIApplication

from a2wsgi import ASGIMiddleware
from a2wsgi.asgi_typing import ASGIApp
from main import app

application = cast(WSGIApplication, ASGIMiddleware(cast(ASGIApp, app)))

```


# FILE: wsgi-flask\deploy.sh

```python
#!/usr/bin/env bash
set -e

cd "$(dirname "$0")"

git fetch origin
git reset --hard origin/main

source ~/virtualenv/opt/stonks.0a.com.ar/stonks-api-python/3.11/bin/activate

pip install --upgrade pip
pip list --format=freeze | grep -vE '^(pip|setuptools|wheel)==' | cut -d= -f1 | xargs -r pip uninstall -y
pip install -e .

mkdir -p tmp
touch tmp/restart.txt

# Enter to the virtual environment.
# To enter to virtual environment, run the command: 
# source /home/alphalab/virtualenv/opt/stonks.0a.com.ar/stonks-api-python/3.11/bin/activate && cd /home/alphalab/opt/stonks.0a.com.ar/stonks-api-python

```


# FILE: wsgi-flask\main.py

```python
from flask import Flask, jsonify

app = Flask(__name__)


@app.route("/")
def index():

    return jsonify(
        server="flask",
        runtime="passenger",
    )

```


# FILE: wsgi-flask\passenger_wsgi.py

```python
from wsgiref.types import WSGIApplication

from main import app

application: WSGIApplication = app

```


# FILE: wsgi-flask-gevent\deploy.sh

```python
#!/usr/bin/env bash
set -e

cd "$(dirname "$0")"

git fetch origin
git reset --hard origin/main

source ~/virtualenv/opt/stonks.0a.com.ar/stonks-api-python/3.11/bin/activate

pip install --upgrade pip
pip list --format=freeze | grep -vE '^(pip|setuptools|wheel)==' | cut -d= -f1 | xargs -r pip uninstall -y
pip install -e .

mkdir -p tmp
touch tmp/restart.txt

# Enter to the virtual environment.
# To enter to virtual environment, run the command: 
# source /home/alphalab/virtualenv/opt/stonks.0a.com.ar/stonks-api-python/3.11/bin/activate && cd /home/alphalab/opt/stonks.0a.com.ar/stonks-api-python

```


# FILE: wsgi-flask-gevent\main.py

```python
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

```


# FILE: wsgi-flask-gevent\passenger_wsgi.py

```python
from wsgiref.types import WSGIApplication

from main import app

application: WSGIApplication = app

```
