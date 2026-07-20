import os

from waitress import serve


HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", "8000"))


def app(environ, start_response):
    body = b"ok"
    start_response("200 OK", [("Content-Type", "text/plain"), ("Content-Length", str(len(body)))])
    return [body]


if __name__ == "__main__":
    serve(app, host=HOST, port=PORT)
