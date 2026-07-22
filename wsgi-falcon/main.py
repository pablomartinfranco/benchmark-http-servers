import falcon
from falcon import Request, Response


class HealthResource:
    def on_get(self, req: Request, resp: Response):
        resp.media = {
            "server": "falcon",
            "runtime": "passenger",
        }


app = falcon.App()

app.add_route("/", HealthResource())
