import os

from sanic import Sanic
from sanic.response import text

HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", "8000"))


app = Sanic("bench_tier3_sanic_with_httptools_parser")


@app.get("/")
async def handler(_):
    return text("ok")


if __name__ == "__main__":
    app.run(host=HOST, port=PORT, access_log=False, single_process=True)  # type: ignore[no-untyped-call]
