import os
import socket
import time

host = os.environ.get('POSTGRES_HOST')
port = os.environ.get('POSTGRES_PORT', 5432)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
while True:
    try:
        s.connect((host, port))
        s.close()
        break
    except Exception:
        time.sleep(1)
