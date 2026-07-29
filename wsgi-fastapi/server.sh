source ~/virtualenv/web/0a/wsgi-fastapi.0a.com.ar/3.11/bin/activate && cd ~/web/0a/wsgi-fastapi.0a.com.ar

python -m pip install --upgrade -r requirements.txt

python -m uvicorn main:app --host 0.0.0.0 --port 8001

nohup python -m uvicorn main:app --host 127.0.0.1 --port 8001 &

nohup python -m uvicorn main:app --host 127.0.0.1 --port 8001 > uvicorn.log 2>&1 &

# Check if it's running
# ps -ef | grep uvicorn
# pgrep -af uvicorn

# Stop it: 1st Find the process ID, 2nd Kill the process ID
# pgrep -af uvicorn
# 12345 uvicorn main:app --host 127.0.0.1 --port 8001
# kill 12345
# kill -9 12345