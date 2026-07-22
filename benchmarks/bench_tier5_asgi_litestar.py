import os

import uvicorn
from litestar import Litestar, get

HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", "8000"))


@get("/")
async def home() -> str:
    return "ok"


app = Litestar(route_handlers=[home])


if __name__ == "__main__":
    uvicorn.run(app, host=HOST, port=PORT, loop="uvloop", access_log=False)
