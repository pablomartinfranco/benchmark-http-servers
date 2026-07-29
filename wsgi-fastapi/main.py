# def application(environ, start_response):  # type: ignore
#     start_response("200 OK", [("Content-Type", "text/plain")])
#     return [b"Hello"]


from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    return {"ok": True}


# from __future__ import annotations

# import asyncio
# import threading
# from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
# from contextlib import AsyncExitStack, asynccontextmanager
# from dataclasses import dataclass
# from typing import Annotated, Any

# import httpx
# import requests
# from fastapi import Depends, FastAPI, Request

# from shared.async_utils import async_blocking_io, async_fibonacci, async_gen_items, async_hash
# from shared.utils import benchmark, benchmark_scope, blocking_io, fibonacci, gen_items, hash


# @dataclass(frozen=True, slots=True)
# class AppContainer:
#     httpx_client: httpx.AsyncClient
#     requests_client: requests.Session
#     thread_pool: ThreadPoolExecutor
#     process_pool: ProcessPoolExecutor


# def get_container(request: Request) -> AppContainer:
#     return request.app.state.container


# Container = Annotated[AppContainer, Depends(get_container)]


# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     print("Starting lifespan")

#     async with AsyncExitStack() as stack:
#         # async resources
#         timeout = httpx.Timeout(connect=5.0, read=10.0, write=10.0, pool=5.0)
#         httpx_client = await stack.enter_async_context(
#             httpx.AsyncClient(timeout=timeout, http2=True)
#         )
#         # sync resources
#         requests_client = requests.Session()
#         stack.callback(requests_client.close)
#         thread_pool = ThreadPoolExecutor(max_workers=5)
#         stack.callback(thread_pool.shutdown, wait=True)
#         process_pool = ProcessPoolExecutor(max_workers=5)
#         stack.callback(process_pool.shutdown, wait=True)
#         # application container
#         app.state.container = AppContainer(
#             httpx_client=httpx_client,
#             requests_client=requests_client,
#             thread_pool=thread_pool,
#             process_pool=process_pool,
#         )
#         # yield control to the application
#         yield


# app = FastAPI(lifespan=lifespan)


# # ---------------------------------------------------------------------------
# # Plain
# # ---------------------------------------------------------------------------


# @app.get("/plain")
# @benchmark(name="plain_outer")
# async def plain() -> dict[str, Any]:
#     with benchmark_scope("plain_inner") as result:
#         values = {"data": "ok"}
#     return {
#         **values,
#         **result.to_dict(),
#     }


# # ---------------------------------------------------------------------------
# # JSON (serial)
# # ---------------------------------------------------------------------------


# @app.get("/json-1")
# @benchmark(name="json_1_outer")
# async def json_1() -> dict[str, Any]:
#     with benchmark_scope("json_1_inner") as result:
#         items_1 = gen_items(100, id=1)
#         items_2 = gen_items(100, id=2)
#         items_3 = gen_items(100, id=3)
#         items_4 = gen_items(100, id=4)
#         items_5 = gen_items(100, id=5)

#     return {
#         "data": [items_1, items_2, items_3, items_4, items_5],
#         **result.to_dict(),
#     }


# # ---------------------------------------------------------------------------
# # JSON  (async, concurrent, parallel)
# # ---------------------------------------------------------------------------


# @app.get("/json-2")
# @benchmark(name="json_2_outer")
# async def json_2() -> dict[str, Any]:

#     with benchmark_scope("json_2_inner") as result:
#         values = [
#             await async_gen_items(100, 1),
#             await async_gen_items(100, 2),
#             await async_gen_items(100, 3),
#             await async_gen_items(100, 4),
#             await async_gen_items(100, 5),
#         ]

#     return {
#         "data": values,
#         **result.to_dict(),
#     }


# @app.get("/json-3")
# @benchmark(name="json_3_outer")
# async def json_3() -> dict[str, Any]:

#     with benchmark_scope("json_3_inner") as result:
#         values = await asyncio.gather(
#             async_gen_items(100, 1),
#             async_gen_items(100, 2),
#             async_gen_items(100, 3),
#             async_gen_items(100, 4),
#             async_gen_items(100, 5),
#             return_exceptions=True,
#         )

#     return {
#         "data": values,
#         **result.to_dict(),
#     }


# @app.get("/json-4")
# @benchmark(name="json_4_outer")
# async def json_4() -> dict[str, Any]:

#     with benchmark_scope("json_4_inner") as result:
#         async with asyncio.TaskGroup() as tg:
#             tasks = [
#                 tg.create_task(async_gen_items(100, 1)),
#                 tg.create_task(async_gen_items(100, 2)),
#                 tg.create_task(async_gen_items(100, 3)),
#                 tg.create_task(async_gen_items(100, 4)),
#                 tg.create_task(async_gen_items(100, 5)),
#             ]

#     return {
#         "data": [t.result() for t in tasks],
#         **result.to_dict(),
#     }


# @app.get("/json-5")
# @benchmark(name="json_5_outer")
# async def json_5() -> dict[str, Any]:

#     with benchmark_scope("json_5_inner") as result:
#         values = await asyncio.gather(
#             asyncio.to_thread(gen_items, 100, 1),
#             asyncio.to_thread(gen_items, 100, 2),
#             asyncio.to_thread(gen_items, 100, 3),
#             asyncio.to_thread(gen_items, 100, 4),
#             asyncio.to_thread(gen_items, 100, 5),
#             return_exceptions=True,
#         )

#     return {
#         "data": values,
#         **result.to_dict(),
#     }


# @app.get("/json-6")
# @benchmark(name="json_6_outer")
# async def json_6(container: Container) -> dict[str, Any]:

#     loop = asyncio.get_running_loop()

#     with benchmark_scope("json_6_inner") as result:
#         values = await asyncio.gather(
#             loop.run_in_executor(container.thread_pool, gen_items, 100, 1),
#             loop.run_in_executor(container.thread_pool, gen_items, 100, 2),
#             loop.run_in_executor(container.thread_pool, gen_items, 100, 3),
#             loop.run_in_executor(container.thread_pool, gen_items, 100, 4),
#             loop.run_in_executor(container.thread_pool, gen_items, 100, 5),
#             return_exceptions=True,
#         )

#     return {
#         "data": values,
#         **result.to_dict(),
#     }


# @app.get("/json-7")
# @benchmark(name="json_7_outer")
# async def json_7(container: Container) -> dict[str, Any]:

#     loop = asyncio.get_running_loop()

#     with benchmark_scope("json_7_inner") as result:
#         values = await asyncio.gather(
#             loop.run_in_executor(container.process_pool, gen_items, 100, 1),
#             loop.run_in_executor(container.process_pool, gen_items, 100, 2),
#             loop.run_in_executor(container.process_pool, gen_items, 100, 3),
#             loop.run_in_executor(container.process_pool, gen_items, 100, 4),
#             loop.run_in_executor(container.process_pool, gen_items, 100, 5),
#             return_exceptions=True,
#         )

#     return {
#         "data": values,
#         **result.to_dict(),
#     }


# # ---------------------------------------------------------------------------
# # CPU (serial)
# # ---------------------------------------------------------------------------


# @app.get("/cpu-1")
# @benchmark(name="cpu_1_outer")
# async def cpu_1() -> dict[str, Any]:

#     with benchmark_scope("cpu_1_inner") as result:
#         fib_1 = fibonacci(31, id=1)
#         fib_2 = fibonacci(31, id=2)
#         fib_3 = fibonacci(31, id=3)
#         fib_4 = fibonacci(31, id=4)
#         fib_5 = fibonacci(31, id=5)

#     return {
#         "data": [fib_1, fib_2, fib_3, fib_4, fib_5],
#         **result.to_dict(),
#     }


# # ---------------------------------------------------------------------------
# # CPU (async, concurrent, parallel)
# # ---------------------------------------------------------------------------


# @app.get("/cpu-2")
# @benchmark(name="cpu_2_outer")
# async def cpu_2() -> dict[str, Any]:

#     with benchmark_scope("cpu_2_inner") as result:
#         values = [
#             await async_fibonacci(31, 1),
#             await async_fibonacci(31, 2),
#             await async_fibonacci(31, 3),
#             await async_fibonacci(31, 4),
#             await async_fibonacci(31, 5),
#         ]

#     return {
#         "data": values,
#         **result.to_dict(),
#     }


# @app.get("/cpu-3")
# @benchmark(name="cpu_3_outer")
# async def cpu_3() -> dict[str, Any]:

#     with benchmark_scope("cpu_3_inner") as result:
#         values = await asyncio.gather(
#             async_fibonacci(31, 1),
#             async_fibonacci(31, 2),
#             async_fibonacci(31, 3),
#             async_fibonacci(31, 4),
#             async_fibonacci(31, 5),
#             return_exceptions=True,
#         )

#     return {
#         "data": values,
#         **result.to_dict(),
#     }


# @app.get("/cpu-4")
# @benchmark(name="cpu_4_outer")
# async def cpu_4() -> dict[str, Any]:

#     with benchmark_scope("cpu_4_inner") as result:
#         async with asyncio.TaskGroup() as tg:
#             tasks = [
#                 tg.create_task(async_fibonacci(31, 1)),
#                 tg.create_task(async_fibonacci(31, 2)),
#                 tg.create_task(async_fibonacci(31, 3)),
#                 tg.create_task(async_fibonacci(31, 4)),
#                 tg.create_task(async_fibonacci(31, 5)),
#             ]

#     return {
#         "data": [t.result() for t in tasks],
#         **result.to_dict(),
#     }


# @app.get("/cpu-5")
# @benchmark(name="cpu_5_outer")
# async def cpu_5() -> dict[str, Any]:

#     with benchmark_scope("cpu_5_inner") as result:
#         values = await asyncio.gather(
#             asyncio.to_thread(fibonacci, 31),
#             asyncio.to_thread(fibonacci, 31),
#             asyncio.to_thread(fibonacci, 31),
#             asyncio.to_thread(fibonacci, 31),
#             asyncio.to_thread(fibonacci, 31),
#             return_exceptions=True,
#         )

#     return {
#         "data": values,
#         **result.to_dict(),
#     }


# @app.get("/cpu-6")
# @benchmark(name="cpu_6_outer")
# async def cpu_6(container: Container) -> dict[str, Any]:

#     loop = asyncio.get_running_loop()

#     with benchmark_scope("cpu_6_inner") as result:
#         values = await asyncio.gather(
#             loop.run_in_executor(container.thread_pool, fibonacci, 31),
#             loop.run_in_executor(container.thread_pool, fibonacci, 31),
#             loop.run_in_executor(container.thread_pool, fibonacci, 31),
#             loop.run_in_executor(container.thread_pool, fibonacci, 31),
#             loop.run_in_executor(container.thread_pool, fibonacci, 31),
#             return_exceptions=True,
#         )

#     return {
#         "data": values,
#         **result.to_dict(),
#     }


# @app.get("/cpu-7")
# @benchmark(name="cpu_7_outer")
# async def cpu_7(container: Container) -> dict[str, Any]:

#     loop = asyncio.get_running_loop()

#     with benchmark_scope("cpu_7_inner") as result:
#         values = await asyncio.gather(
#             loop.run_in_executor(container.process_pool, fibonacci, 31),
#             loop.run_in_executor(container.process_pool, fibonacci, 31),
#             loop.run_in_executor(container.process_pool, fibonacci, 31),
#             loop.run_in_executor(container.process_pool, fibonacci, 31),
#             loop.run_in_executor(container.process_pool, fibonacci, 31),
#             return_exceptions=True,
#         )

#     return {
#         "data": values,
#         **result.to_dict(),
#     }


# # ---------------------------------------------------------------------------
# # IO (serial)
# # ---------------------------------------------------------------------------


# @app.get("/io-1")
# @benchmark(name="io_1_outer")
# async def io_1() -> dict[str, Any]:

#     with benchmark_scope("io_1_inner") as result:
#         io_1 = blocking_io(id=1)
#         io_2 = blocking_io(id=2)
#         io_3 = blocking_io(id=3)
#         io_4 = blocking_io(id=4)
#         io_5 = blocking_io(id=5)

#     return {
#         "data": [io_1, io_2, io_3, io_4, io_5],
#         **result.to_dict(),
#     }


# # ---------------------------------------------------------------------------
# # IO  (async, concurrent, parallel)
# # ---------------------------------------------------------------------------


# @app.get("/io-2")
# @benchmark(name="io_2_outer")
# async def io_2() -> dict[str, Any]:

#     with benchmark_scope("io_2_inner") as result:
#         values = [
#             await async_blocking_io(1),
#             await async_blocking_io(2),
#             await async_blocking_io(3),
#             await async_blocking_io(4),
#             await async_blocking_io(5),
#         ]

#     return {
#         "data": values,
#         **result.to_dict(),
#     }


# @app.get("/io-3")
# @benchmark(name="io_3_outer")
# async def io_3() -> dict[str, Any]:

#     with benchmark_scope("io_3_inner") as result:
#         values = await asyncio.gather(
#             async_blocking_io(1),
#             async_blocking_io(2),
#             async_blocking_io(3),
#             async_blocking_io(4),
#             async_blocking_io(5),
#             return_exceptions=True,
#         )

#     return {
#         "data": values,
#         **result.to_dict(),
#     }


# @app.get("/io-4")
# @benchmark(name="io_4_outer")
# async def io_4() -> dict[str, Any]:

#     with benchmark_scope("io_4_inner") as result:
#         async with asyncio.TaskGroup() as tg:
#             tasks = [
#                 tg.create_task(async_blocking_io(1)),
#                 tg.create_task(async_blocking_io(2)),
#                 tg.create_task(async_blocking_io(3)),
#                 tg.create_task(async_blocking_io(4)),
#                 tg.create_task(async_blocking_io(5)),
#             ]

#     return {
#         "data": [t.result() for t in tasks],
#         **result.to_dict(),
#     }


# @app.get("/io-5")
# @benchmark(name="io_5_outer")
# async def io_5() -> dict[str, Any]:

#     with benchmark_scope("io_5_inner") as result:
#         values = await asyncio.gather(
#             asyncio.to_thread(blocking_io, 1),
#             asyncio.to_thread(blocking_io, 2),
#             asyncio.to_thread(blocking_io, 3),
#             asyncio.to_thread(blocking_io, 4),
#             asyncio.to_thread(blocking_io, 5),
#             return_exceptions=True,
#         )

#     return {
#         "data": values,
#         **result.to_dict(),
#     }


# @app.get("/io-6")
# @benchmark(name="io_6_outer")
# async def io_6(container: Container) -> dict[str, Any]:

#     loop = asyncio.get_running_loop()

#     with benchmark_scope("io_6_inner") as result:
#         values = await asyncio.gather(
#             loop.run_in_executor(container.thread_pool, blocking_io, 1),
#             loop.run_in_executor(container.thread_pool, blocking_io, 2),
#             loop.run_in_executor(container.thread_pool, blocking_io, 3),
#             loop.run_in_executor(container.thread_pool, blocking_io, 4),
#             loop.run_in_executor(container.thread_pool, blocking_io, 5),
#             return_exceptions=True,
#         )

#     return {
#         "data": values,
#         **result.to_dict(),
#     }


# @app.get("/io-7")
# @benchmark(name="io_7_outer")
# async def io_7(container: Container) -> dict[str, Any]:

#     loop = asyncio.get_running_loop()

#     with benchmark_scope("io_7_inner") as result:
#         values = await asyncio.gather(
#             loop.run_in_executor(container.process_pool, blocking_io, 1),
#             loop.run_in_executor(container.process_pool, blocking_io, 2),
#             loop.run_in_executor(container.process_pool, blocking_io, 3),
#             loop.run_in_executor(container.process_pool, blocking_io, 4),
#             loop.run_in_executor(container.process_pool, blocking_io, 5),
#             return_exceptions=True,
#         )

#     return {
#         "data": values,
#         **result.to_dict(),
#     }


# # ---------------------------------------------------------------------------
# # HTTP (serial)
# # ---------------------------------------------------------------------------


# @app.get("/http-1")
# @benchmark(name="http_1_outer")
# async def http_1() -> dict[str, Any]:

#     with benchmark_scope("http_1_inner") as result:
#         responses = [
#             requests.get("https://httpbin.org/delay/1"),
#             requests.get("https://httpbin.org/delay/1"),
#             requests.get("https://httpbin.org/delay/1"),
#             requests.get("https://httpbin.org/delay/1"),
#             requests.get("https://httpbin.org/delay/1"),
#         ]

#     return {
#         "data": [r.status_code for r in responses],
#         **result.to_dict(),
#     }


# # ---------------------------------------------------------------------------
# # HTTP (async, concurrent, parallel)
# # ---------------------------------------------------------------------------


# @app.get("/http-2")
# @benchmark(name="http_2_outer")
# async def http_2(container: Container) -> dict[str, Any]:

#     with benchmark_scope("http_2_inner") as result:
#         responses = [
#             await container.httpx_client.get("https://httpbin.org/delay/1"),
#             await container.httpx_client.get("https://httpbin.org/delay/1"),
#             await container.httpx_client.get("https://httpbin.org/delay/1"),
#             await container.httpx_client.get("https://httpbin.org/delay/1"),
#             await container.httpx_client.get("https://httpbin.org/delay/1"),
#         ]

#     return {
#         "data": [r.status_code for r in responses],
#         **result.to_dict(),
#     }


# @app.get("/http-2b")
# @benchmark(name="http_2b_outer")
# async def http_2b() -> dict[str, Any]:

#     with benchmark_scope("http_2b_inner") as result:
#         async with httpx.AsyncClient(timeout=10) as client:
#             responses = [
#                 await client.get("https://httpbin.org/delay/1"),
#                 await client.get("https://httpbin.org/delay/1"),
#                 await client.get("https://httpbin.org/delay/1"),
#                 await client.get("https://httpbin.org/delay/1"),
#                 await client.get("https://httpbin.org/delay/1"),
#             ]

#     return {
#         "data": [r.status_code for r in responses],
#         **result.to_dict(),
#     }


# @app.get("/http-3")
# @benchmark(name="http_3_outer")
# async def http_3(container: Container) -> dict[str, Any]:

#     with benchmark_scope("http_3_inner") as result:
#         responses = await asyncio.gather(
#             container.httpx_client.get("https://httpbin.org/delay/1"),
#             container.httpx_client.get("https://httpbin.org/delay/1"),
#             container.httpx_client.get("https://httpbin.org/delay/1"),
#             container.httpx_client.get("https://httpbin.org/delay/1"),
#             container.httpx_client.get("https://httpbin.org/delay/1"),
#             return_exceptions=True,
#         )

#     return {
#         "data": [r.status_code for r in responses if isinstance(r, httpx.Response)],
#         **result.to_dict(),
#     }


# @app.get("/http-4")
# @benchmark(name="http_4_outer")
# async def http_4(container: Container) -> dict[str, Any]:

#     with benchmark_scope("http_4_inner") as result:
#         async with asyncio.TaskGroup() as tg:
#             tasks = [
#                 tg.create_task(container.httpx_client.get("https://httpbin.org/delay/1")),
#                 tg.create_task(container.httpx_client.get("https://httpbin.org/delay/1")),
#                 tg.create_task(container.httpx_client.get("https://httpbin.org/delay/1")),
#                 tg.create_task(container.httpx_client.get("https://httpbin.org/delay/1")),
#                 tg.create_task(container.httpx_client.get("https://httpbin.org/delay/1")),
#             ]

#     return {
#         "data": [t.result().status_code for t in tasks],
#         **result.to_dict(),
#     }


# @app.get("/http-5")
# @benchmark(name="http_5_outer")
# async def http_5(container: Container) -> dict[str, Any]:

#     with benchmark_scope("http_5_inner") as result:
#         responses = await asyncio.gather(
#             asyncio.to_thread(container.httpx_client.get, "https://httpbin.org/delay/1"),
#             asyncio.to_thread(container.httpx_client.get, "https://httpbin.org/delay/1"),
#             asyncio.to_thread(container.httpx_client.get, "https://httpbin.org/delay/1"),
#             asyncio.to_thread(container.httpx_client.get, "https://httpbin.org/delay/1"),
#             asyncio.to_thread(container.httpx_client.get, "https://httpbin.org/delay/1"),
#             return_exceptions=True,
#         )

#     return {
#         "data": [r.status_code for r in responses if isinstance(r, httpx.Response)],
#         **result.to_dict(),
#     }


# @app.get("/http-5b")
# @benchmark(name="http_5b_outer")
# async def http_5b(container: Container) -> dict[str, Any]:

#     with benchmark_scope("http_5b_inner") as result:
#         responses = await asyncio.gather(
#             asyncio.to_thread(container.requests_client.get, "https://httpbin.org/delay/1"),
#             asyncio.to_thread(container.requests_client.get, "https://httpbin.org/delay/1"),
#             asyncio.to_thread(container.requests_client.get, "https://httpbin.org/delay/1"),
#             asyncio.to_thread(container.requests_client.get, "https://httpbin.org/delay/1"),
#             asyncio.to_thread(container.requests_client.get, "https://httpbin.org/delay/1"),
#             return_exceptions=True,
#         )

#     return {
#         "data": [r.status_code for r in responses if isinstance(r, httpx.Response)],
#         **result.to_dict(),
#     }


# @app.get("/http-6")
# @benchmark(name="http_6_outer")
# async def http_6(container: Container) -> dict[str, Any]:

#     client = container.httpx_client
#     thread_pool = container.thread_pool
#     loop = asyncio.get_running_loop()

#     with benchmark_scope("http_6_inner") as result:
#         responses = await asyncio.gather(
#             loop.run_in_executor(thread_pool, client.get, "https://httpbin.org/delay/1"),
#             loop.run_in_executor(thread_pool, client.get, "https://httpbin.org/delay/1"),
#             loop.run_in_executor(thread_pool, client.get, "https://httpbin.org/delay/1"),
#             loop.run_in_executor(thread_pool, client.get, "https://httpbin.org/delay/1"),
#             loop.run_in_executor(thread_pool, client.get, "https://httpbin.org/delay/1"),
#             return_exceptions=True,
#         )

#     return {
#         "data": [r.status_code for r in responses if isinstance(r, httpx.Response)],
#         **result.to_dict(),
#     }


# @app.get("/http-6b")
# @benchmark(name="http_6b_outer")
# async def http_6b(container: Container) -> dict[str, Any]:

#     client = container.requests_client
#     thread_pool = container.thread_pool
#     loop = asyncio.get_running_loop()

#     with benchmark_scope("http_6b_inner") as result:
#         responses = await asyncio.gather(
#             loop.run_in_executor(thread_pool, client.get, "https://httpbin.org/delay/1"),
#             loop.run_in_executor(thread_pool, client.get, "https://httpbin.org/delay/1"),
#             loop.run_in_executor(thread_pool, client.get, "https://httpbin.org/delay/1"),
#             loop.run_in_executor(thread_pool, client.get, "https://httpbin.org/delay/1"),
#             loop.run_in_executor(thread_pool, client.get, "https://httpbin.org/delay/1"),
#             return_exceptions=True,
#         )

#     return {
#         "data": [r.status_code for r in responses if isinstance(r, httpx.Response)],
#         **result.to_dict(),
#     }


# @app.get("/http-7")
# @benchmark(name="http_7_outer")
# async def http_7(container: Container) -> dict[str, Any]:

#     client = container.httpx_client
#     process_pool = container.process_pool
#     loop = asyncio.get_running_loop()

#     with benchmark_scope("http_7_inner") as result:
#         responses = await asyncio.gather(
#             loop.run_in_executor(process_pool, client.get, "https://httpbin.org/delay/1"),
#             loop.run_in_executor(process_pool, client.get, "https://httpbin.org/delay/1"),
#             loop.run_in_executor(process_pool, client.get, "https://httpbin.org/delay/1"),
#             loop.run_in_executor(process_pool, client.get, "https://httpbin.org/delay/1"),
#             loop.run_in_executor(process_pool, client.get, "https://httpbin.org/delay/1"),
#             return_exceptions=True,
#         )

#     return {
#         "data": [r.status_code for r in responses if isinstance(r, httpx.Response)],
#         **result.to_dict(),
#     }


# @app.get("/http-7b")
# @benchmark(name="http_7b_outer")
# async def http_7b(container: Container) -> dict[str, Any]:

#     client = container.requests_client
#     process_pool = container.process_pool
#     loop = asyncio.get_running_loop()

#     with benchmark_scope("http_7b_inner") as result:
#         responses = await asyncio.gather(
#             loop.run_in_executor(process_pool, client.get, "https://httpbin.org/delay/1"),
#             loop.run_in_executor(process_pool, client.get, "https://httpbin.org/delay/1"),
#             loop.run_in_executor(process_pool, client.get, "https://httpbin.org/delay/1"),
#             loop.run_in_executor(process_pool, client.get, "https://httpbin.org/delay/1"),
#             loop.run_in_executor(process_pool, client.get, "https://httpbin.org/delay/1"),
#             return_exceptions=True,
#         )

#     return {
#         "data": [r.status_code for r in responses if isinstance(r, httpx.Response)],
#         **result.to_dict(),
#     }


# # ---------------------------------------------------------------------------
# # HTTP Call
# # ---------------------------------------------------------------------------


# @app.get("/http-call-1")
# @benchmark(name="http_call_1_outer")
# async def http_call_1(container: Container) -> dict[str, Any]:

#     with benchmark_scope("http_call_1_inner") as result:
#         response = container.requests_client.get("https://httpbin.org/get")

#         is_json = response.headers.get("content-type", "").startswith("application/json")

#     return {
#         "status": response.status_code,
#         "content_type": response.headers.get("content-type"),
#         "body": response.json() if is_json else response.text,
#         **result.to_dict(),
#     }


# @app.get("/http-call-2")
# @benchmark(name="http_call_2_outer")
# async def http_call_2(container: Container) -> dict[str, Any]:

#     with benchmark_scope("http_call_2_inner") as result:
#         response = await container.httpx_client.get("https://httpbin.org/get")

#         is_json = response.headers.get("content-type", "").startswith("application/json")

#     return {
#         "status": response.status_code,
#         "content_type": response.headers.get("content-type"),
#         "body": response.json() if is_json else response.text,
#         **result.to_dict(),
#     }


# # ---------------------------------------------------------------------------
# # Echo
# # ---------------------------------------------------------------------------


# @app.post("/echo")
# @benchmark(name="echo_outer")
# async def echo(request: Request) -> dict[str, Any]:

#     with benchmark_scope("echo_inner") as result:
#         data = await request.json()

#     return {
#         "data": data,
#         **result.to_dict(),
#     }


# # ---------------------------------------------------------------------------
# # Hash (serial)
# # ---------------------------------------------------------------------------


# @app.get("/hash-1")
# @benchmark(name="hash_1_outer")
# async def hash_1() -> dict[str, Any]:

#     with benchmark_scope("hash_1_inner") as result:
#         data = b"x" * 10_000_000
#         values = [
#             hash(data, id=1),
#             hash(data, id=2),
#             hash(data, id=3),
#             hash(data, id=4),
#             hash(data, id=5),
#         ]

#     return {
#         "sha256": values,
#         **result.to_dict(),
#     }


# # ---------------------------------------------------------------------------
# # Hash (async, concurrent, parallel)
# # ---------------------------------------------------------------------------


# @app.get("/hash-2")
# @benchmark(name="hash_2_outer")
# async def hash_2() -> dict[str, Any]:

#     data = b"x" * 10_000_000

#     with benchmark_scope("hash_2_inner") as result:
#         values = [
#             await async_hash(data, 1),
#             await async_hash(data, 2),
#             await async_hash(data, 3),
#             await async_hash(data, 4),
#             await async_hash(data, 5),
#         ]

#     return {
#         "sha256": values,
#         **result.to_dict(),
#     }


# @app.get("/hash-3")
# @benchmark(name="hash_3_outer")
# async def hash_3() -> dict[str, Any]:

#     data = b"x" * 10_000_000

#     with benchmark_scope("hash_3_inner") as result:
#         values = await asyncio.gather(
#             async_hash(data, 1),
#             async_hash(data, 2),
#             async_hash(data, 3),
#             async_hash(data, 4),
#             async_hash(data, 5),
#             return_exceptions=True,
#         )

#     return {
#         "sha256": values,
#         **result.to_dict(),
#     }


# @app.get("/hash-4")
# @benchmark(name="hash_4_outer")
# async def hash_4() -> dict[str, Any]:

#     data = b"x" * 10_000_000

#     with benchmark_scope("hash_4_inner") as result:
#         async with asyncio.TaskGroup() as tg:
#             tasks = [
#                 tg.create_task(async_hash(data, 1)),
#                 tg.create_task(async_hash(data, 2)),
#                 tg.create_task(async_hash(data, 3)),
#                 tg.create_task(async_hash(data, 4)),
#                 tg.create_task(async_hash(data, 5)),
#             ]

#     return {
#         "sha256": [t.result() for t in tasks],
#         **result.to_dict(),
#     }


# @app.get("/hash-5")
# @benchmark(name="hash_5_outer")
# async def hash_5() -> dict[str, Any]:

#     data = b"x" * 10_000_000

#     with benchmark_scope("hash_5_inner") as result:
#         values = await asyncio.gather(
#             asyncio.to_thread(hash, data, 1),
#             asyncio.to_thread(hash, data, 2),
#             asyncio.to_thread(hash, data, 3),
#             asyncio.to_thread(hash, data, 4),
#             asyncio.to_thread(hash, data, 5),
#             return_exceptions=True,
#         )

#     return {
#         "sha256": values,
#         **result.to_dict(),
#     }


# @app.get("/hash-6")
# @benchmark(name="hash_6_outer")
# async def hash_6(container: Container) -> dict[str, Any]:

#     loop = asyncio.get_running_loop()

#     data = b"x" * 10_000_000

#     with benchmark_scope("hash_6_inner") as result:
#         values = await asyncio.gather(
#             loop.run_in_executor(container.thread_pool, hash, data, 1),
#             loop.run_in_executor(container.thread_pool, hash, data, 2),
#             loop.run_in_executor(container.thread_pool, hash, data, 3),
#             loop.run_in_executor(container.thread_pool, hash, data, 4),
#             loop.run_in_executor(container.thread_pool, hash, data, 5),
#             return_exceptions=True,
#         )

#     return {
#         "sha256": values,
#         **result.to_dict(),
#     }


# @app.get("/hash-7")
# @benchmark(name="hash_7_outer")
# async def hash_7(container: Container) -> dict[str, Any]:

#     loop = asyncio.get_running_loop()

#     data = b"x" * 10_000_000

#     with benchmark_scope("hash_7_inner") as result:
#         values = await asyncio.gather(
#             loop.run_in_executor(container.process_pool, hash, data, 1),
#             loop.run_in_executor(container.process_pool, hash, data, 2),
#             loop.run_in_executor(container.process_pool, hash, data, 3),
#             loop.run_in_executor(container.process_pool, hash, data, 4),
#             loop.run_in_executor(container.process_pool, hash, data, 5),
#             return_exceptions=True,
#         )

#     return {
#         "sha256": values,
#         **result.to_dict(),
#     }


# # ---------------------------------------------------------------------------
# # AsyncIO Info
# # ---------------------------------------------------------------------------


# @app.get("/asyncio-info")
# async def asyncio_info() -> dict[str, Any]:

#     loop = asyncio.get_running_loop()
#     current = asyncio.current_task()

#     return {
#         "asyncio": {
#             "loop": {
#                 "type": type(loop).__name__,
#                 "repr": repr(loop),
#                 "is_running": loop.is_running(),
#                 "is_closed": loop.is_closed(),
#             },
#             "task": {
#                 "type": type(current).__name__ if current else None,
#                 "repr": repr(current),
#                 "name": current.get_name() if current else None,
#                 "done": current.done() if current else None,
#             },
#         },
#         "python": {
#             "thread": {
#                 "name": threading.current_thread().name,
#                 "ident": threading.current_thread().ident,
#             },
#         },
#     }


# # ---------------------------------------------------------------------------
# # AsyncIO Yield
# # ---------------------------------------------------------------------------


# @app.get("/asyncio-yield")
# @benchmark(name="asyncio_yield_outer")
# async def asyncio_yield() -> dict[str, Any]:

#     with benchmark_scope("asyncio_yield_inner") as result:
#         events: list[str] = []

#         async def worker(id: int) -> None:
#             events.append(f"{id}-start")
#             await asyncio.sleep(0)
#             events.append(f"{id}-end")

#         async with asyncio.TaskGroup() as tg:
#             tg.create_task(worker(1))
#             tg.create_task(worker(2))
#             tg.create_task(worker(3))

#     return {
#         "events": events,
#         "tasks": 3,
#         **result.to_dict(),
#     }
