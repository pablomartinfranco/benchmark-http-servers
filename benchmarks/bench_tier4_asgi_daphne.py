import os
from pathlib import Path

from daphne.cli import CommandLineInterface


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


if __name__ == "__main__":
    module_name = Path(__file__).stem
    CommandLineInterface().run([
        "-b",
        HOST,
        "-p",
        str(PORT),
        f"{module_name}:app",
    ])
