import os
import pprint
import sys

sys.path.insert(0, os.path.dirname(__file__))


def application(environ, start_response):  # type: ignore[no-untyped-def]
    body = pprint.pformat(dict(environ))  # type: ignore[no-untyped-call]
    message = "It works!\n"
    version = f"Python {sys.version.split()[0]}\n"
    response = "\n".join([body, message, version]).encode()
    content_length = str(len(response))
    start_response("200 OK", [("Content-Type", "text/plain"), ("Content-Length", content_length)])
    return [response]
