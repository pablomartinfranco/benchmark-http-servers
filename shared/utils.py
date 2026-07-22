import hashlib
import time
from collections.abc import Callable
from functools import wraps
from typing import Any


def benchmark(func: Callable[..., Any]) -> Callable[..., Any]:

    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:

        start = time.perf_counter()

        try:
            return func(*args, **kwargs)

        finally:
            elapsed = time.perf_counter() - start
            print(f"\n{func.__name__}: {elapsed:.6f}s")

    return wrapper


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
