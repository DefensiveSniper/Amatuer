import os
import json
import signal
import time
import psutil
from flask import Flask, request, jsonify, render_template, Response
from flask_cors import CORS
from openai import OpenAI

CONFIG_PATH = "config.json"

app = Flask(__name__)
CORS(app)  # 允许跨域请求

@app.route("/")
def index():
    return render_template("index.html")

# 读取配置
def load_config():
    if os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    return {
        "provider": "openai",
        "model": "gpt-4o",
        "apiKeys": { "openai": "", "deepseek": "" }  # 记录不同 provider 的 API Key
    }

# 全局配置
config = load_config()

# 初始化 OpenAI 客户端
def create_client():
    base_urls = {
        "openai": "https://api.openai.com/v1",
        "deepseek": "https://api.deepseek.com/v1"
    }

    provider = config["provider"]
    api_key = config["apiKeys"].get(provider, "")

    return OpenAI(api_key=api_key, base_url=base_urls[provider])

client = create_client()

# 获取配置
@app.route("/get_config", methods=["GET"])
def get_config():
    try:
        return jsonify(config), 200
    except Exception as e:
        return jsonify({"error": "Failed to load config", "details": str(e)}), 500

# 保存配置
@app.route("/save_config", methods=["POST"])
def save_config():
    try:
        data = request.json
        if not data:
            return jsonify({"error": "Invalid data"}), 400

        with open(CONFIG_PATH, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

        global config, client
        config = data
        client = create_client()  # 重新初始化 API 客户端

        return jsonify({"message": "Config saved successfully"}), 200

    except Exception as e:
        return jsonify({"error": "Failed to save config", "details": str(e)}), 500

# AI 聊天接口
@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        user_message = data.get("message", "")

        if not user_message:
            return jsonify({"error": "消息不能为空"}), 400

        def generate():
            response = client.chat.completions.create(
                model=config["model"],
                messages=[{"role": "user", "content": user_message}],
                stream=True
            )
            for chunk in response:
                if chunk.choices:
                    text = getattr(chunk.choices[0].delta, "content", "") or ""
                    yield text
                else:
                    yield "[Empty Response Chunk]"
        return Response(generate(), mimetype='text/plain')
    except Exception as e:
        print("Error in /chat:", str(e))
        return jsonify({"error": "服务器内部错误", "details": str(e)}), 500

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
