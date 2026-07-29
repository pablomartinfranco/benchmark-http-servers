import asyncio
from typing import Any

from shared.utils import blocking_io, fibonacci, gen_items, hash


async def async_blocking_io(id: int | None = None) -> None:
    await asyncio.to_thread(blocking_io, id)


async def async_fibonacci(n: int, id: int | None = None) -> tuple[int, int]:
    return await asyncio.to_thread(fibonacci, n, id)


async def async_gen_items(n: int = 100, id: int | None = None) -> list[dict[str, Any]]:
    return await asyncio.to_thread(gen_items, n, id)


async def async_hash(data: bytes, id: int | None = None) -> tuple[str, int]:
    return await asyncio.to_thread(hash, data, id)
