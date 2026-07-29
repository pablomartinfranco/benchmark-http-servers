#!/usr/bin/env bash
set -euo pipefail
# Exit immediately if a command exits with a non-zero status.

# set -euxo pipefail
# Exit immediately if a command exits with a non-zero status,
# print commands and their arguments as they are executed, 
# treat unset variables as an error when substituting,
# and prevent errors in a pipeline from being masked.

cd "$(dirname "$0")"

PYTHON_VERSION="3.11"

APP_DIR="$(basename "$PWD")"

VENV="$HOME/virtualenv/web/0a/$APP_DIR/$PYTHON_VERSION"

rm -rf "$VENV/lib/python$PYTHON_VERSION/site-packages"

source "$VENV/bin/activate"

python -m ensurepip --upgrade

# python -m pip install --upgrade pip

# python -m pip list --format=freeze \
#   | grep -vE '^(pip|setuptools|wheel)==' || true \
#   | cut -d= -f1 \
#   | xargs -r python -m pip uninstall -y

python -m pip install --upgrade -r requirements.txt

mkdir -p tmp

touch tmp/restart.txt

echo "Deployment completed for $APP_DIR"

# Enter to the virtual environment.
# To enter to virtual environment, run the command: 
# source ~/virtualenv/web/0a/wsgi.0a.com.ar/3.11/bin/activate && cd ~/web/0a/wsgi.0a.com.ar