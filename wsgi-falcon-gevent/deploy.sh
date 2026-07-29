#!/usr/bin/env bash
set -e

cd "$(dirname "$0")"

source ~/virtualenv/web/0a/wsgi-falcon-gevent.0a.com.ar/3.11/bin/activate

python -m pip install --upgrade pip

python -m pip list --format=freeze | grep -vE '^(pip|setuptools|wheel)==' | cut -d= -f1 | xargs -r python -m pip uninstall -y

python -m pip install --upgrade -r requirements.txt

deactivate

mkdir -p tmp

touch tmp/restart.txt

# Enter to the virtual environment.
# To enter to virtual environment, run the command: 
# source ~/virtualenv/web/0a/wsgi-falcon-gevent.0a.com.ar/3.11/bin/activate && cd ~/web/0a/wsgi-falcon-gevent.0a.com.ar
