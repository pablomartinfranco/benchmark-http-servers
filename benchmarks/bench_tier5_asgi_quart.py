import os

import uvicorn
from quart import Quart

HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", "8000"))


app = Quart(__name__)


@app.get("/")
async def home() -> str:
    return "ok"


if __name__ == "__main__":
    uvicorn.run(app, host=HOST, port=PORT, loop="uvloop", access_log=False)
