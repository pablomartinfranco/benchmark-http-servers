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

process = psutil.Process(os.getpid())

print(f"\nos pid={os.getpid()} psutil pid={process.pid}", flush=True)


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

        print(f"\nbefore end: os={os.getpid()} psutil={process.pid}", flush=True)
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
