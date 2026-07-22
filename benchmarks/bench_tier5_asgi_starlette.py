import os

import uvicorn
from starlette.applications import Starlette
from starlette.responses import PlainTextResponse
from starlette.routing import Route

HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", "8000"))


async def home(_):
    return PlainTextResponse("ok")


app = Starlette(routes=[Route("/", home)])  # type: ignore[no-untyped-call]


if __name__ == "__main__":
    uvicorn.run(app, host=HOST, port=PORT, loop="uvloop", access_log=False)
