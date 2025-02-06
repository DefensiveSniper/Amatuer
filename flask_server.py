import os
import psutil
import time
import signal
from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

# 监听 SIGTERM 信号，优雅关闭 Flask 服务器
def shutdown_server(signum, frame):
    print("Shutting down Flask server...")
    os._exit(0)

signal.signal(signal.SIGTERM, shutdown_server)
signal.signal(signal.SIGINT, shutdown_server)

# 监视 Electron 是否退出
PARENT_PID = os.getppid()

def monitor_parent():
    while True:
        if not psutil.pid_exists(PARENT_PID):
            print("Electron 已退出，关闭 Flask 服务器")
            os._exit(0)
        time.sleep(5)

if __name__ == '__main__':
    from threading import Thread
    monitor_thread = Thread(target=monitor_parent, daemon=True)
    monitor_thread.start()

    app.run(port=6969)
