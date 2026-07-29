from __future__ import annotations

import atexit
import hashlib
import logging
import os
import queue
import time
import tracemalloc
from collections.abc import Callable, Generator
from contextlib import contextmanager
from dataclasses import asdict, dataclass
from functools import cache, wraps
from logging.handlers import QueueHandler, QueueListener
from typing import Any

import psutil

log_queue: queue.SimpleQueue[logging.LogRecord] = queue.SimpleQueue()

file_handler = logging.FileHandler("bmark.log")

listener = QueueListener(log_queue, file_handler)
listener.start()

atexit.register(listener.stop)

logger = logging.getLogger("bmark")
logger.setLevel(logging.INFO)
logger.addHandler(QueueHandler(log_queue))

# Initialize once when the application starts.
# Do not start/stop tracemalloc on every request.
tracemalloc.start()


@dataclass(slots=True)
class BenchmarkResult:
    elapsed: float = 0.0
    cpu_time: float = 0.0
    memory: int = 0
    peak_memory: int = 0
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
    tracemalloc.reset_peak()

    start_context = process.num_ctx_switches()

    result = BenchmarkResult()

    try:
        yield result

    finally:
        end_wall = time.perf_counter_ns()
        end_cpu = time.process_time_ns()
        end_memory, peak_memory = tracemalloc.get_traced_memory()
        end_context = process.num_ctx_switches()

        result.elapsed = (end_wall - start_wall) / 1_000_000_000
        result.cpu_time = (end_cpu - start_cpu) / 1_000_000_000
        result.memory = end_memory - start_memory
        result.peak_memory = peak_memory - start_memory

        # print(f"\nbefore end: os={os.getpid()} psutil={process.pid}", flush=True)
        result.voluntary_switches = end_context.voluntary - start_context.voluntary
        result.involuntary_switches = end_context.involuntary - start_context.involuntary

        # print(
        #     f"\n{name}:\n"
        #     f"  wall={result.elapsed:.6f}s\n"
        #     f"  cpu ={result.cpu_time:.6f}s\n"
        #     f"  mem ={result.memory / 1024:.2f}KB\n"
        #     f"  ctx ={result.voluntary_switches} voluntary "
        #     f"{result.involuntary_switches} involuntary",
        #     flush=True,
        # )

        # logger.info(
        #     "%s wall=%.6f cpu=%.6f mem=%d ctx=%d/%d",
        #     name,
        #     result.elapsed,
        #     result.cpu_time,
        #     result.memory,
        #     result.voluntary_switches,
        #     result.involuntary_switches,
        # )

        logger.info(
            "%s wall=%.6fs cpu=%.6fs mem=%+.2fKiB max=%+.2fKiB ctx=%d/%d",
            name,
            result.elapsed,
            result.cpu_time,
            result.memory / 1024,
            result.peak_memory / 1024,
            result.voluntary_switches,
            result.involuntary_switches,
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


def flush_log_queue() -> None:
    while True:
        try:
            record = log_queue.get_nowait()
        except queue.Empty:
            break
        else:
            file_handler.handle(record)

    file_handler.flush()


def blocking_io(id: int | None = None) -> int:
    id = id if id is not None else int(time.time()) % 100000
    time.sleep(1)
    # _ = id and print(f"\nid = {id}")
    _ = id and logger.info(f"Blocking I/O completed for id={id}")
    return id


def fibonacci(n: int, id: int | None = None) -> tuple[int, int]:
    id = id if id is not None else int(time.time()) % 100000

    @cache
    def fibo(n: int) -> int:
        return n if n <= 1 else fibo(n - 1) + fibo(n - 2)

    fib = fibo(n)
    # _ = id and print(f"\nid = {id}")
    _ = id and logger.info(f"Fibonacci({n}) = {fib} for id={id}")
    return fib, id


def gen_items(n: int = 1000, id: int | None = None) -> list[dict[str, Any]]:
    id = id if id is not None else int(time.time()) % 100000
    items: list[dict[str, Any]] = [
        {
            "id": f"{id}-{i}",
            "name": f"user-{i}",
            "active": True,
        }
        for i in range(n)
    ]
    # _ = id and print(f"\nid = {id}")
    _ = id and logger.info(f"Generated {n} items for id={id}")
    return items


def hash(data: bytes, id: int | None = None) -> tuple[str, int]:
    id = id if id is not None else int(time.time()) % 100000

    result = hashlib.sha256(data).hexdigest()
    # _ = id and print(f"\nid = {id}")
    _ = id and logger.info(f"Hashed data of length {len(data)} for id={id}")
    return result, id
