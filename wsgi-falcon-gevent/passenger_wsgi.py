# ruff: noqa: E402
import sys

sys.stdout = sys.stderr

from wsgiref.types import WSGIApplication

from main import app

application: WSGIApplication = app
