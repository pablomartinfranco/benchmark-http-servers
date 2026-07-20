# benchmark-http-servers

Single-file HTTP benchmark servers grouped by benchmark name.

## Files

- `/home/runner/work/benchmark-http-servers/benchmark-http-servers/benchmarks/bench_tier1_stdlib_httpserver.py`
- `/home/runner/work/benchmark-http-servers/benchmark-http-servers/benchmarks/bench_tier1_stdlib_threadinghttpserver.py`
- `/home/runner/work/benchmark-http-servers/benchmark-http-servers/benchmarks/bench_tier1_stdlib_asyncio_default.py`
- `/home/runner/work/benchmark-http-servers/benchmark-http-servers/benchmarks/bench_tier1_stdlib_asyncio_uvloop.py`
- `/home/runner/work/benchmark-http-servers/benchmark-http-servers/benchmarks/bench_tier2_wsgi_waitress.py`
- `/home/runner/work/benchmark-http-servers/benchmark-http-servers/benchmarks/bench_tier2_wsgi_gunicorn_sync.py`
- `/home/runner/work/benchmark-http-servers/benchmark-http-servers/benchmarks/bench_tier2_wsgi_gunicorn_gthread.py`
- `/home/runner/work/benchmark-http-servers/benchmark-http-servers/benchmarks/bench_tier2_wsgi_gunicorn_gevent.py`
- `/home/runner/work/benchmark-http-servers/benchmark-http-servers/benchmarks/bench_tier3_aiohttp_with_aiohttp_parser.py`
- `/home/runner/work/benchmark-http-servers/benchmark-http-servers/benchmarks/bench_tier3_sanic_with_httptools_parser.py`
- `/home/runner/work/benchmark-http-servers/benchmark-http-servers/benchmarks/bench_tier3_blacksheep_with_httptools_parser.py`
- `/home/runner/work/benchmark-http-servers/benchmark-http-servers/benchmarks/bench_tier3_falcon_asgi_with_httptools_parser.py`
- `/home/runner/work/benchmark-http-servers/benchmark-http-servers/benchmarks/bench_tier4_asgi_uvicorn_default.py`
- `/home/runner/work/benchmark-http-servers/benchmark-http-servers/benchmarks/bench_tier4_asgi_uvicorn_uvloop.py`
- `/home/runner/work/benchmark-http-servers/benchmark-http-servers/benchmarks/bench_tier4_asgi_hypercorn.py`
- `/home/runner/work/benchmark-http-servers/benchmark-http-servers/benchmarks/bench_tier4_asgi_daphne.py`
- `/home/runner/work/benchmark-http-servers/benchmark-http-servers/benchmarks/bench_tier5_asgi_bare_app.py`
- `/home/runner/work/benchmark-http-servers/benchmark-http-servers/benchmarks/bench_tier5_asgi_starlette.py`
- `/home/runner/work/benchmark-http-servers/benchmark-http-servers/benchmarks/bench_tier5_asgi_fastapi.py`
- `/home/runner/work/benchmark-http-servers/benchmark-http-servers/benchmarks/bench_tier5_asgi_litestar.py`
- `/home/runner/work/benchmark-http-servers/benchmark-http-servers/benchmarks/bench_tier5_asgi_quart.py`
- `/home/runner/work/benchmark-http-servers/benchmark-http-servers/benchmarks/bench_tier6_granian_default.py`
- `/home/runner/work/benchmark-http-servers/benchmark-http-servers/benchmarks/bench_tier6_granian_fastapi.py`
- `/home/runner/work/benchmark-http-servers/benchmark-http-servers/benchmarks/bench_tier6_granian_bare_asgi.py`

## Run

```bash
python /home/runner/work/benchmark-http-servers/benchmark-http-servers/benchmarks/<file>.py
```

Environment variables:

- `HOST` (default `0.0.0.0`)
- `PORT` (default `8000`)
- `WORKERS` (used by Gunicorn/Granian examples, default `1`)
- `THREADS` (used by Gunicorn gthread example, default `8`)