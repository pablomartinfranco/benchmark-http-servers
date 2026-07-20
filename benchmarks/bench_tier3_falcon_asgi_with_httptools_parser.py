import os

import falcon.asgi


HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", "8000"))


class HelloResource:
    async def on_get(self, req, resp):
        resp.text = "ok"


app = falcon.asgi.App()
app.add_route("/", HelloResource())


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host=HOST, port=PORT, loop="auto", access_log=False)
