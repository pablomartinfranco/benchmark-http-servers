import os

from gunicorn.app.base import BaseApplication


HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", "8000"))
WORKERS = int(os.getenv("WORKERS", "1"))


def app(environ, start_response):
    body = b"ok"
    start_response("200 OK", [("Content-Type", "text/plain"), ("Content-Length", str(len(body)))])
    return [body]


class GunicornApplication(BaseApplication):
    def __init__(self, application, options=None):
        self.application = application
        self.options = options or {}
        super().__init__()

    def load_config(self):
        for key, value in self.options.items():
            if key in self.cfg.settings and value is not None:
                self.cfg.set(key.lower(), value)

    def load(self):
        return self.application


if __name__ == "__main__":
    GunicornApplication(
        app,
        {
            "bind": f"{HOST}:{PORT}",
            "workers": WORKERS,
            "worker_class": "gevent",
            "accesslog": None,
            "errorlog": "-",
        },
    ).run()
