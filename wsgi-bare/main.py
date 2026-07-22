from collections.abc import Iterable
from wsgiref.types import StartResponse, WSGIEnvironment


def application(environ: WSGIEnvironment, start_response: StartResponse) -> Iterable[bytes]:
    body = b"OK"
    start_response(
        "200 OK",
        [
            ("Content-Type", "text/plain"),
            ("Content-Length", str(len(body))),
        ],
    )
    return [body]
