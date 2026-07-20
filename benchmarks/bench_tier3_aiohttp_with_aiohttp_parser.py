import os

from aiohttp import web


HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", "8000"))


async def handler(_: web.Request) -> web.Response:
    return web.Response(text="ok")


app = web.Application()
app.router.add_get("/", handler)


if __name__ == "__main__":
    web.run_app(app, host=HOST, port=PORT, access_log=None)
