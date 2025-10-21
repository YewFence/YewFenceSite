from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy  # 导入ORM库 SQLAlchemy
import os # 导入 os 库来帮助我们构建路径

# 获取当前文件 (app.py) 所在的文件夹的绝对路径
basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)

# 2. 配置数据库
# 告诉 SQLAlchemy 我们的数据库在哪里
# 我们使用 SQLite，数据库文件将命名为 'data.db'，存放在项目根目录
app.config['SQLALCHEMY_DATABASE_URI'] = \
    'sqlite:///' + os.path.join(basedir, 'data.db')
# 关闭一个不必要的追踪功能
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# 3. 初始化 SQLAlchemy 实例
# 把我们的 app 实例传给 SQLAlchemy，完成“绑定”
db = SQLAlchemy(app)

# 定义路由 (Routing)
@app.route('/')
def show_index_page():
    """ 显示首页 """
    return render_template('index.html')

@app.route('/contact')
def show_contact_page():
    """ 显示联系页 """
    return render_template('contact.html')

@app.route('/interests')
def show_interests_page():
    """ 显示兴趣页 """
    return render_template('interests.html')

@app.route('/about')
def show_about_page():
    """ 显示关于页 """
    return render_template('about.html')

@app.route('/blogs')
def show_blogs_page():
    """ 显示博客页 """
    return render_template('blogs_summary.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        pw = request.form.get("password", "").strip()
        # TODO: 这里替换为你的鉴权逻辑，比如对接数据库或哈希校验
        if pw == "ok":
            return redirect("/management")  # 或 url_for('management')
        else:
            return render_template("login.html", error="密码错误"), 401
    return render_template("login.html")

@app.route('/management')
def management():
    """ 显示管理页 """
    return render_template('management.html')