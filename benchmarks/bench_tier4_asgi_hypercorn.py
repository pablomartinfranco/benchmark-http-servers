import asyncio
import os

from hypercorn.asyncio import serve
from hypercorn.config import Config


HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", "8000"))


async def app(scope, receive, send):
    if scope["type"] != "http":
        return
    await send(
        {
            "type": "http.response.start",
            "status": 200,
            "headers": [(b"content-type", b"text/plain"), (b"content-length", b"2")],
        }
    )
    await send({"type": "http.response.body", "body": b"ok"})


async def main() -> None:
    config = Config()
    config.bind = [f"{HOST}:{PORT}"]
    config.use_reloader = False
    config.accesslog = None
    await serve(app, config)


if __name__ == "__main__":
    asyncio.run(main())
