import os
from pathlib import Path

HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", "8000"))
WORKERS = int(os.getenv("WORKERS", "1"))


async def app(scope, receive, send):  # type: ignore[no-untyped-def]
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
    os.execvp(
        "granian",
        [
            "granian",
            f"{module_name}:app",
            "--interface",
            "asgi",
            "--host",
            HOST,
            "--port",
            str(PORT),
            "--workers",
            str(WORKERS),
        ],
    )
