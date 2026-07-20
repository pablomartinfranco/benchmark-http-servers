import os

from blacksheep import Application
from blacksheep.messages import Response


HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", "8000"))


app = Application()


@app.router.get("/")
async def home():
    return Response(200, [(b"content-type", b"text/plain")], b"ok")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host=HOST, port=PORT, loop="auto", access_log=False)
