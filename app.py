from flask import Flask

# 1. 创建一个 Flask 应用实例
app = Flask(__name__)

# 2. 定义一个路由 (Routing)
# 告诉 Flask：如果有人访问网站的根路径 ("/")
@app.route('/')
def hello_world():
    # 3. 运行这个视图函数 (View Function)
    # 并返回 "Hello, World!"
    return 'Hello, World!'

@app.route('/about')
def about():
    return 'This is the about page.'