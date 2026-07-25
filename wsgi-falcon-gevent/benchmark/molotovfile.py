import os

from molotov import scenario  # type: ignore

BASE_URL = os.getenv("BASE_URL", "https://wsgi-falcon-gevent.0a.com.ar")

ENDPOINTS = [
    "/plain",
    # "/json-1",
    # "/json-2",
    # "/cpu-1",
    # "/cpu-2",
    # "/io-1",
    # "/io-2",
    # "/http-1",
    # "/http-2",
    # "/http-call",
    # "/hash-1",
    # "/hash-2",
]


@scenario()
async def benchmark(session):  # type: ignore
    for endpoint in ENDPOINTS:
        async with session.get(f"{BASE_URL}{endpoint}") as resp:  # type: ignore
            assert resp.status == 200  # type: ignore
            await resp.read()  # type: ignore
