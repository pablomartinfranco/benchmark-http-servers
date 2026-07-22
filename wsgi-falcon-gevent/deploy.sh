#!/usr/bin/env bash
set -e

cd "$(dirname "$0")"

source ~/virtualenv/web/0a/wsgi-falcon-gevent.0a.com.ar/3.11/bin/activate

pip install --upgrade pip
pip list --format=freeze | grep -vE '^(pip|setuptools|wheel)==' | cut -d= -f1 | xargs -r pip uninstall -y
pip install -r requirements.txt

mkdir -p tmp
touch tmp/restart.txt

# Enter to the virtual environment.
# To enter to virtual environment, run the command: 
# source ~/virtualenv/web/0a/wsgi-falcon-gevent.0a.com.ar/3.11/bin/activate && cd ~/web/0a/wsgi-falcon-gevent.0a.com.ar
