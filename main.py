from flask import Flask, render_template

app = Flask(__name__)

# 你已有的其他路由
@app.route("/some_other_route")
def some_other_route():
    return "..."

@app.route("/")
def index():
    # 直接渲染 templates 文件夹中的 index.html
    return render_template("index.html")

if __name__ == '__main__':
    app.run(port=5000)
