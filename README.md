# benchmark-http-servers

Single-file HTTP benchmark servers grouped by benchmark name.

## Run

```bash
python /home/runner/work/benchmark-http-servers/benchmark-http-servers/benchmarks/<file>.py
```

Environment variables:

- `HOST` (default `0.0.0.0`)
- `PORT` (default `8000`)
- `WORKERS` (used by Gunicorn/Granian examples, default `1`)
- `THREADS` (used by Gunicorn gthread example, default `8`)

# Benchmark Configurations

This document summarizes the execution model of every benchmark configuration.

| Benchmark | Runtime | HTTP Parser | Concurrency Model | Scheduling | I/O | Best For | Notes |
|-----------|----------|-------------|-------------------|------------|--------------|----------|------|
| **bench-tier1-stdlib-httpserver** | stdlib | Python | Single-thread | Sequential | ❌ Blocking | CPU-bound (single client), testing | Processes one request at a time. Simplest possible HTTP server. |
| **bench-tier1-stdlib-threadinghttpserver** | stdlib | Python | Thread per request | OS kernel threads | ❌ Blocking | Mixed, low/moderate concurrency | Every connection gets its own OS thread. Simple but expensive at high concurrency. |
| **bench-tier1-stdlib-asyncio-default** | asyncio | Manual | Async coroutines | asyncio event loop | ✅ Non-blocking | I/O-bound | Single-thread cooperative multitasking using `async/await`. |
| **bench-tier1-stdlib-asyncio-uvloop** | asyncio + uvloop | Manual | Async coroutines | libuv event loop | ✅ Non-blocking | I/O-bound | Same architecture as above but replaces asyncio scheduler with libuv for lower overhead. |

---

## Tier 2 — WSGI Servers

| Benchmark | Runtime | HTTP Parser | Concurrency Model | Scheduling | Blocking I/O | Best For | Notes |
|-----------|----------|-------------|-------------------|------------|--------------|----------|------|
| **bench-tier2-wsgi-waitress** | Waitress | Python | Thread pool | OS kernel threads | ❌ Blocking | Mixed workloads | Production WSGI server. Cross-platform (Windows friendly). |
| **bench-tier2-wsgi-gunicorn-sync** | Gunicorn | Python | Multiple worker processes | OS process scheduler | ❌ Blocking | CPU-bound | Classic prefork model. One request per worker process. Linux standard deployment. |
| **bench-tier2-wsgi-gunicorn-gthread** | Gunicorn | Python | Processes + thread pools | OS scheduler | ❌ Blocking | Mixed workloads | Multiple processes each serving requests using worker threads. |
| **bench-tier2-wsgi-gunicorn-gevent** | Gunicorn + gevent | Python | Processes + greenlets | Cooperative (greenlet scheduler) | ✅ Non-blocking* | I/O-bound | Monkey-patches blocking sockets into cooperative operations. Excellent for many idle connections. |

> *Uses cooperative non-blocking networking via gevent monkey patching.

---

## Tier 3 — Async Frameworks

| Benchmark | Runtime | HTTP Parser | Concurrency Model | Scheduling | Blocking I/O | Best For | Notes |
|-----------|----------|-------------|-------------------|------------|--------------|----------|------|
| **bench-tier3-aiohttp-with-aiohttp-parser** | aiohttp | aiohttp C parser | Async coroutines | asyncio / uvloop | ✅ Non-blocking | I/O-bound | Mature asyncio-native HTTP framework. |
| **bench-tier3-sanic-with-httptools-parser** | Sanic | httptools (llhttp) | Async coroutines | asyncio / uvloop | ✅ Non-blocking | I/O-bound | Optimized for low latency and high throughput. |
| **bench-tier3-blacksheep-with-httptools-parser** | BlackSheep | httptools | Async coroutines | asyncio / uvloop | ✅ Non-blocking | I/O-bound | Minimal overhead ASGI framework. |
| **bench-tier3-falcon-asgi-with-httptools-parser** | Falcon ASGI | httptools | Async coroutines | asyncio / uvloop | ✅ Non-blocking | I/O-bound | Lightweight ASGI implementation focused on performance. |

---

## Tier 4 — ASGI Servers

| Benchmark | Runtime | HTTP Parser | Concurrency Model | Scheduling | Blocking I/O | Best For | Notes |
|-----------|----------|-------------|-------------------|------------|--------------|----------|------|
| **bench-tier4-asgi-uvicorn-default** | Uvicorn | httptools | Async coroutines | asyncio | ✅ Non-blocking | I/O-bound | Most common ASGI deployment. |
| **bench-tier4-asgi-uvicorn-uvloop** | Uvicorn | httptools | Async coroutines | uvloop (libuv) | ✅ Non-blocking | I/O-bound | Faster scheduler with lower event-loop overhead. |
| **bench-tier4-asgi-hypercorn** | Hypercorn | h11 / httptools | Async coroutines | asyncio / Trio / uvloop | ✅ Non-blocking | I/O-bound | Supports multiple async runtimes including Trio. |
| **bench-tier4-asgi-daphne** | Daphne | Twisted HTTP | Async callbacks | Twisted Reactor | ✅ Non-blocking | I/O-bound | Reference ASGI server used by Django Channels. |

---

## Tier 5 — ASGI Applications

(Assumes Uvicorn + uvloop)

| Benchmark | Framework | Protocol | Scheduling | Blocking I/O | Best For | Notes |
|-----------|-----------|----------|------------|--------------|----------|------|
| **bench-tier5-asgi-bare-app** | Bare ASGI | ASGI | Event loop | ✅ Non-blocking | I/O-bound | Measures raw ASGI overhead. |
| **bench-tier5-asgi-starlette** | Starlette | ASGI | Event loop | ✅ Non-blocking | I/O-bound | Lightweight ASGI toolkit. |
| **bench-tier5-asgi-fastapi** | FastAPI | ASGI | Event loop | ✅ Non-blocking | I/O-bound | Adds dependency injection and Pydantic validation. |
| **bench-tier5-asgi-litestar** | Litestar | ASGI | Event loop | ✅ Non-blocking | I/O-bound | Performance-oriented ASGI framework. |
| **bench-tier5-asgi-quart** | Quart | ASGI | Event loop | ✅ Non-blocking | I/O-bound | Async-compatible Flask implementation. |

---

## Tier 6 — Granian

| Benchmark | Runtime | HTTP Parser | Concurrency Model | Scheduling | Blocking I/O | Best For | Notes |
|-----------|----------|-------------|-------------------|------------|--------------|----------|------|
| **bench-tier6-granian-default** | Granian | Rust (hyper) | Native worker threads | Rust runtime | ✅ Non-blocking | I/O-bound | Networking handled entirely in Rust before entering Python. |
| **bench-tier6-granian-fastapi** | Granian + FastAPI | Rust | Native worker threads | Rust runtime | ✅ Non-blocking | I/O-bound | FastAPI application running behind Rust HTTP stack. |
| **bench-tier6-granian-bare-asgi** | Granian + Bare ASGI | Rust | Native worker threads | Rust runtime | ✅ Non-blocking | I/O-bound | Lowest-overhead Granian benchmark. |

---

# Concurrency Models

| Model | Description |
|--------|-------------|
| **Sequential** | One request processed at a time. |
| **Thread per request** | Every connection owns one kernel thread. |
| **Thread pool** | Fixed number of worker threads process requests. |
| **Multi-process** | Multiple independent Python worker processes. |
| **Process + thread pool** | Worker processes containing thread pools. |
| **Greenlets** | User-space coroutines scheduled cooperatively by gevent. |
| **Async coroutines** | `async/await` tasks running on an event loop. |
| **Native Rust workers** | Networking and scheduling implemented in Rust. |

---

# Scheduling Techniques

| Scheduler | Description |
|-----------|-------------|
| **Sequential** | No scheduler; one request runs until completion. |
| **Kernel threads** | Operating system schedules threads across CPU cores. |
| **Kernel processes** | Operating system schedules independent worker processes. |
| **asyncio Event Loop** | Cooperative scheduler driven by `await`. |
| **uvloop (libuv)** | High-performance replacement for asyncio's default event loop. |
| **Greenlet Scheduler** | gevent switches greenlets during patched blocking operations. |
| **Twisted Reactor** | Callback/event-driven scheduler used by Twisted. |
| **Rust Runtime** | Native scheduler implemented in Rust (Granian). |

---

# HTTP Parsers

| Parser | Language | Used By |
|---------|----------|----------|
| stdlib parser | Python | HTTPServer, ThreadingHTTPServer |
| Manual parser | Python | Custom asyncio benchmarks |
| aiohttp parser | C | aiohttp |
| httptools (llhttp) | C | Uvicorn, Sanic, BlackSheep, Falcon |
| h11 | Python | Hypercorn (optional) |
| Twisted HTTP | Python | Daphne |
| hyper | Rust | Granian |

---

# Choosing the Right Model

| Workload | Recommended Model |
|----------|-------------------|
| CPU-bound | Multi-process (Gunicorn Sync) |
| Mixed CPU + blocking I/O | Gunicorn GThread, Waitress |
| High network concurrency | asyncio / Uvicorn / Sanic / aiohttp |
| Thousands of idle connections | gevent |
| Maximum ASGI performance | Uvicorn + uvloop |
| Lowest Python networking overhead | Granian |
| Baseline comparisons | stdlib HTTPServer / ThreadingHTTPServer |

---

# If only choosing 12 configurations

```bash
bench-stdlib-httpserver (python http parser) # single thread
bench-stdlib-threadinghttpserver (python http parser) # kernel thread / request
bench-stdlib-asyncio-default (manual http parser) # event loop
bench-stdlib-asyncio-uvloop (manual http parser) # event loop

bench-wsgi-waitress (thread pool) # windows friendly
bench-wsgi-gunicorn-sync (multi process) # linux standard
bench-wsgi-gunicorn-gthread (processes + thread pools) # mixed workloads
bench-wsgi-gunicorn-gevent (processes + greenlets) # cooperative i/o

bench-asyncio-aiohttp-default
bench-asyncio-sanic-httptools-uvloop

bench-asgi-bare-uvicorn-uvloop
bench-asgi-fastapi-uvicorn-uvloop
```

---

Examples: **"respond to HTTP requests using CPython 3.11"**, the simplest possible servers built into the standard library.

```python
from http.server import BaseHTTPRequestHandler, HTTPServer

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-Type", "text/plain")
        self.end_headers()
        self.wfile.write(b"Hello, world!")

HTTPServer(("0.0.0.0", 8000), Handler).serve_forever()
```

Run it:

```bash
python server.py
```

Test it:

```bash
curl http://localhost:8000/
```

Response:

```
Hello, world!
```

---

If you just need a quick static file server, CPython already includes one:

```bash
python -m http.server 8000
```

---

If you want to respond to different paths:

```python
from http.server import BaseHTTPRequestHandler, HTTPServer

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/":
            body = b"Home"
        elif self.path == "/hello":
            body = b"Hello!"
        else:
            self.send_error(404)
            return

        self.send_response(200)
        self.send_header("Content-Type", "text/plain")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

HTTPServer(("localhost", 8000), Handler).serve_forever()
```

This uses only the Python 3.11 standard library—no third-party packages required.

If instead you meant **respond to raw TCP requests**, **HTTPS**, or **REST APIs (e.g., JSON endpoints)**, the simplest solution is slightly different.



No. The code as written is **synchronous**.

`HTTPServer` processes **one request at a time**. If one request takes 5 seconds, every other client waits until it's finished.

### Option 1: Threading (simplest)

If you just want to handle multiple clients concurrently, replace `HTTPServer` with `ThreadingHTTPServer`:

```python
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Hello")

ThreadingHTTPServer(("localhost", 8000), Handler).serve_forever()
```

Each request runs in its own thread.

---

### Option 2: asyncio

The standard `http.server` module is **not** based on `asyncio`, so you cannot write:

```python
async def do_GET(self):
    ...
```

and have it work.

If you want true async I/O, you'd typically use an asyncio-based framework like:

* `aiohttp`
* `FastAPI` (via `uvicorn`)
* `Quart`

Example with `aiohttp`:

```python
from aiohttp import web

async def hello(request):
    return web.Response(text="Hello!")

app = web.Application()
app.router.add_get("/", hello)

web.run_app(app, port=8000)
```

---

### Option 3: Write your own asyncio server (standard library only)

Python's standard library includes `asyncio.start_server()`, so you can implement an HTTP server yourself:

```python
import asyncio

async def handle(reader, writer):
    await reader.read(1024)

    response = (
        "HTTP/1.1 200 OK\r\n"
        "Content-Type: text/plain\r\n"
        "Content-Length: 5\r\n"
        "\r\n"
        "Hello"
    )

    writer.write(response.encode())
    await writer.drain()
    writer.close()
    await writer.wait_closed()

async def main():
    server = await asyncio.start_server(handle, "0.0.0.0", 8000)
    async with server:
        await server.serve_forever()

asyncio.run(main())
```

This is fully asynchronous and uses only the Python 3.11 standard library.

### Conclusions

* **Simple HTTP server:** `ThreadingHTTPServer`
* **High-concurrency async server:** `aiohttp` or `FastAPI`
* **No dependencies and true async:** `asyncio.start_server()` with your own minimal HTTP parsing.





