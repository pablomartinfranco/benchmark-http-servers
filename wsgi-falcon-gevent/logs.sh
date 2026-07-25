#!/usr/bin/env bash
set -euo pipefail

tail -F ~/web/0a/wsgi-falcon-gevent.0a.com.ar/stderr.log

# tail -F \
#     "$SCRIPT_DIR/web/0a/wsgi-falcon-gevent.0a.com.ar/stderr.log" \
#     "$SCRIPT_DIR/web/0a/wsgi-falcon-gevent.0a.com.ar/stdout.log"