import os
from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import PlainTextResponse

HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", "8000"))
WORKERS = int(os.getenv("WORKERS", "1"))


app = FastAPI()


@app.get("/", response_class=PlainTextResponse)
async def home() -> str:
    return "ok"


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
