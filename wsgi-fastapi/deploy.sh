#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

APP_DIR="$(basename "$PWD")"
VENV="$HOME/virtualenv/web/0a/$APP_DIR/3.11"

source "$VENV/bin/activate"

python -m pip install --upgrade pip

python -m pip list --format=freeze \
  | grep -vE '^(pip|setuptools|wheel)==' \
  | cut -d= -f1 \
  | xargs -r python -m pip uninstall -y

python -m pip install -r requirements.txt

mkdir -p tmp
touch tmp/restart.txt

echo "Deployment completed for $APP_DIR"

# Enter to the virtual environment.
# To enter to virtual environment, run the command: 
# source ~/virtualenv/web/0a/wsgi.0a.com.ar/3.11/bin/activate && cd ~/web/0a/wsgi.0a.com.ar



# #!/usr/bin/env bash
# set -e

# cd "$(dirname "$0")"

# source ~/virtualenv/web/0a/wsgi-fastapi.0a.com.ar/3.11/bin/activate

# pip install --upgrade pip
# pip list --format=freeze | grep -vE '^(pip|setuptools|wheel)==' | cut -d= -f1 | xargs -r pip uninstall -y
# pip install -r requirements.txt

# mkdir -p tmp
# touch tmp/restart.txt

# # Enter to the virtual environment.
# # To enter to virtual environment, run the command: 
# # source ~/virtualenv/web/0a/wsgi-falcon-gevent.0a.com.ar/3.11/bin/activate && cd ~/web/0a/wsgi-falcon-gevent.0a.com.ar
