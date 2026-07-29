#####
## If only WSGI is supported, use the WSGI application
import os
import sys

# Add your application directory to the system path
sys.path.insert(0, os.path.dirname(__file__))

# Import your FastAPI instance (assuming your main script is main.py and app instance is named app)
# Import the ASGI-to-WSGI middleware
from a2wsgi import ASGIMiddleware
from main import app  # Import the FastAPI app instance

# Wrap the FastAPI app to make it WSGI-compliant
application = ASGIMiddleware(app)  # type: ignore


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
