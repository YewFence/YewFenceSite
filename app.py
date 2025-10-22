from flask import Flask, render_template, request, redirect, session, url_for
from flask_sqlalchemy import SQLAlchemy  # 导入ORM库 SQLAlchemy
import os # 导入 os 库来帮助我们构建路径
from datetime import datetime # 我们需要 datetime记录默认的发布时间
from werkzeug.security import generate_password_hash, check_password_hash # 导入哈希工具，校验密码

# -----------------------------------------------
# 功能函数配置
# -----------------------------------------------

# Markdown 渲染函数
try:
    from markdown import markdown as _md_render
    def render_md(text: str) -> str:
        return _md_render(
            text or "",
            extensions=['extra', 'codehilite', 'fenced_code', 'toc']
        )
except Exception:
    def render_md(text: str) -> str:
        return f"<pre>{(text or '').replace('<','&lt;').replace('>','&gt;')}</pre>"

# -----------------------------------------------
# 应用和数据库配置
# -----------------------------------------------

basedir = os.path.abspath(os.path.dirname(__file__))
# 1. 创建 Flask 应用实例
app = Flask(__name__)

app.config['SECRET_KEY'] = 'nawowenni_shenmecaishiyigefuzadezifuchuan' # 随便写一个复杂的字符串
# 2. 配置数据库
# 使用 SQLite，数据库文件将命名为 'data.db'，存放在项目根目录
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.db')
# 关闭一个不必要的追踪功能
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# 3. 初始化 SQLAlchemy 实例
# 把我们的 app 实例传给 SQLAlchemy
db = SQLAlchemy(app)

# -----------------------------------------------
# 模型定义
# -----------------------------------------------

# Admin 模型，存储登录信息，暂时不需要多用户管理
class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    # 存储hash值
    password_hash = db.Column(db.String(128), nullable=False)

    def set_password(self, password):
        """ 设置密码，存储哈希值到db """
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """ 检查密码是否正确 """
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        """ 返回字符串表示 """
        return f'<Admin {self.username}>'

# 文章模型
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True) # 主键
    title = db.Column(db.String(120), nullable=False)
    author_name = db.Column(db.String(80), default='YewFence') # 默认作者是YewFence 
    brief_summary = db.Column(db.Text) 
    content = db.Column(db.Text, nullable=False) 
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow) 
    status = db.Column(db.String(30), nullable=False, default='draft')

    def __repr__(self):
        """ 返回字符串表示 """
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

@app.route('/blog')
def show_blog_page():
    """ 显示博客页 """
    all_posts = Post.query.order_by(Post.date_posted.desc()).all()
    # 2. 把查询到的数据 (all_posts) 传递给模板
    return render_template('blog_index.html', posts=all_posts)

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
        if admin_user and admin_user.check_password(password):
            # 4. 登录成功后将登录状态存入 session
            session['logged_in'] = True
            session['username'] = admin_user.username
            # 5. 重定向到管理页面
            return redirect(url_for('management'))
        else:
            # 登录失败
            return render_template("login.html", error="密码错误"), 401
    # GET: 支持通过查询参数 info 显示提醒信息
    info = request.args.get('info')
    if info:
        return render_template("login.html", info=info)
    return render_template("login.html")

@app.route('/post_detail/<int:post_id>')
def post_detail(post_id):
    """ 显示文章详情页 """
    post = Post.query.get_or_404(post_id)
    # 将 Markdown 内容转换为 HTML
    post_html = render_md(post.content)
    return render_template("single_post.html", post=post, post_html=post_html)

@app.route('/logout')
def logout():
    """ 处理登出请求 """
    # 清除 session
    session.pop('logged_in', None)
    session.pop('username', None)
    # 重定向到登录页，加上提示信息
    return redirect(url_for('login', info='你已成功登出'))

@app.route('/management')
def management():
    """ 显示管理页 """
    # 检查是否登录
    if 'logged_in' not in session:
        # 未登录：带提示信息跳转到登录页
        return redirect(url_for('login', info='请先登录后再访问管理页'))
    # 已登录：显示管理页
    return render_template('management.html')