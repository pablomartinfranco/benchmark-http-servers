#!/usr/bin/env bash
set -e

cd "$(dirname "$0")"

git fetch origin
git reset --hard origin/main

source ~/virtualenv/opt/stonks.0a.com.ar/stonks-api-python/3.11/bin/activate

pip install --upgrade pip
pip list --format=freeze | grep -vE '^(pip|setuptools|wheel)==' | cut -d= -f1 | xargs -r pip uninstall -y
pip install -e .

mkdir -p tmp
touch tmp/restart.txt

# Enter to the virtual environment.
# To enter to virtual environment, run the command: 
# source /home/alphalab/virtualenv/opt/stonks.0a.com.ar/stonks-api-python/3.11/bin/activate && cd /home/alphalab/opt/stonks.0a.com.ar/stonks-api-python
