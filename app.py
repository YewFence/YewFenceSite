from flask import Flask, render_template, request, redirect, session, url_for
from flask_sqlalchemy import SQLAlchemy  # 导入ORM库 SQLAlchemy
import os # 导入 os 库来帮助我们构建路径
from datetime import datetime # 我们需要 datetime
from werkzeug.security import generate_password_hash, check_password_hash # 1. 导入哈希工具

# -----------------------------------------------
# 应用和数据库配置
# -----------------------------------------------

basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config['SECRET_KEY'] = 'nawowenni_shenmecaishiyigefuzadezifuchuan' # 随便写一个复杂的字符串

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

# -----------------------------------------------
# 模型定义
# -----------------------------------------------

# Admin 模型 (用于存储登录信息)
class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    # 我们不存密码原文，只存哈希值！哈希值通常很长。
    password_hash = db.Column(db.String(128), nullable=False)

    # (可选) 我们可以在模型里定义一个“设置密码”的方法
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    # (可选) 再定义一个“检查密码”的方法
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<Admin {self.username}>'

# 文章模型
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True) # 主键
    
    # 对应 json 'title'
    title = db.Column(db.String(120), nullable=False)
    
    # --- 新增 ---
    # 对应 json 'author'
    author_name = db.Column(db.String(80), default='YewFence') # 你可以把'YourName'改成你的名字
    
    # 对应 json 'brief_summary'
    brief_summary = db.Column(db.Text) # 用 Text 更保险，summary 可能会长
    
    # 对应 .md 文件的内容
    content = db.Column(db.Text, nullable=False) 
    
    # 对应 json 'date'
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow) 
    
    # 对应 json 'status' (e.g., 'hidden', 'published')
    status = db.Column(db.String(30), nullable=False, default='draft')

    def __repr__(self):
        return f'<Post {self.title}>'
    
# -----------------------------------------------
# 路由配置
# -----------------------------------------------

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
# 检查用户是否已经登录了
    if 'logged_in' in session:
        return redirect(url_for('management')) # 如果已登录，直接跳到管理页

    if request.method == 'POST':
        # 1. 从表单获取输入的密码数据
        password = request.form.get('password', '')
        # 2. 从数据库获取管理员用户
        admin_user = Admin.query.filter_by(username='YewFence').first()
        # 3. 校验
        # 检查：(1) 用户存在吗？ (2) 密码正确吗？
        if admin_user and admin_user.check_password(password):
            # 登录成功！
            # 4. 存入 session，记住他
            session['logged_in'] = True
            session['username'] = admin_user.username
            # 5. 重定向到管理页面
            return redirect(url_for('management')) # 我们稍后创建这个路由
        else:
            # 登录失败
            return render_template("login.html", error="密码错误"), 401
    # GET: 支持通过查询参数 info 显示提醒信息
    info = request.args.get('info')
    if info:
        return render_template("login.html", info=info)
    return render_template("login.html")

@app.route('/logout')
def logout():
    """ 处理登出请求 """
    # 清除 session
    session.pop('logged_in', None)
    session.pop('username', None)
    # 重定向到登录页，带提示信息
    return redirect(url_for('login', info='你已成功登出'))

@app.route('/management')
def management():
    """ 显示管理页 """
    # 检查是否登录
    if 'logged_in' not in session:
        # 未登录：带提示信息跳转到登录页
        return redirect(url_for('login', info='请先登录后再访问管理页'))

    # 渲染你的 management.html 页面
    return render_template('management.html')