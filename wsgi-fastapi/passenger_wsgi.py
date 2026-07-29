from a2wsgi import ASGIMiddleware
from starlette.applications import Starlette
from starlette.responses import PlainTextResponse
from starlette.routing import Route


async def homepage(request):  # type: ignore
    return PlainTextResponse("hello")


app = Starlette(routes=[Route("/", homepage)])  # type: ignore

application = ASGIMiddleware(app)  # type: ignore


# from fastapi import FastAPI

# app = FastAPI()


# @app.get("/")
# async def root():
#     return {"ok": True}


# def application(environ, start_response):  # type: ignore
#     start_response("200 OK", [("Content-Type", "text/plain")])
#     return [b"Hello"]


# def application(environ, start_response):  # type: ignore
#     start_response(
#         "200 OK",
#         [("Content-Type", "text/plain")],
#     )
#     return [b"Hello"]


# import sys

# from a2wsgi import ASGIMiddleware
# from main import app

# sys.stdout = sys.stderr

# application = ASGIMiddleware(app)  # type: ignore


# import sys
# from typing import cast
# from wsgiref.types import WSGIApplication

# from a2wsgi import ASGIMiddleware
# from a2wsgi.asgi_typing import ASGIApp
# from main import app

# sys.stdout = sys.stderr

# application = cast(WSGIApplication, ASGIMiddleware(cast(ASGIApp, app)))
