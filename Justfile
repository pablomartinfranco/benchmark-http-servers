# Load .env automatically
set dotenv-load := true
set export := true

# Windows
set shell := ["powershell.exe", "-NoLogo", "-NoProfile", "-Command"]

# Linux/macOS
# set shell := ["sh", "-cu"]

# Config
app  := env_var_or_default("APP", "main:app")
host := env_var_or_default("HOST", "127.0.0.1")
port := env_var_or_default("PORT", "8000")

default:
    @just --list

# Dependencies
install:
    uv sync

update:
    uv lock --upgrade
    uv sync

# Run app
dev:
    uv run uvicorn {{app}} --app-dir src --reload --host {{host}} --port {{port}}

start:
    uv run uvicorn {{app}} --app-dir src --host {{host}} --port {{port}}
    # uv run uvicorn {{app}} --app-dir src --host 0.0.0.0 --port {{port}} # localhost:8000,

# Testing
test:
    uv run pytest

# Code quality
lint:
    uv run ruff check .

format:
    uv run ruff format .

check:
    just lint
    just test

locust:
    uv run locust -f locustfile.py --headless -u 100 -r 10 --run-time 1m

molotov:
    uv run molotov molotovfile.py --workers 100 --duration 60
    # uv run molotov benchmark.py

# Python shell
shell:
    uv run python

# Cleanup
clean:
    Remove-Item -Recurse -Force -ErrorAction SilentlyContinue .pytest_cache, .ruff_cache
    Get-ChildItem -Recurse -Directory -Filter __pycache__ | Remove-Item -Recurse -Force