# ruff: noqa: E402
import sys

sys.stdout = sys.stderr

from falcon.asgi import App, Request, Response
from main_asgi import app

application: App[Request, Response] = app
