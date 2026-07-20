import os

import uvicorn
from fastapi import FastAPI
from fastapi.responses import PlainTextResponse


HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", "8000"))


app = FastAPI()


@app.get("/", response_class=PlainTextResponse)
async def home() -> str:
    return "ok"


if __name__ == "__main__":
    uvicorn.run(app, host=HOST, port=PORT, loop="uvloop", access_log=False)
