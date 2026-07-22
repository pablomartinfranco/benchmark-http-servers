from typing import cast
from wsgiref.types import WSGIApplication

from a2wsgi import ASGIMiddleware
from a2wsgi.asgi_typing import ASGIApp
from main import app

application = cast(WSGIApplication, ASGIMiddleware(cast(ASGIApp, app)))
