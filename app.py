from flask import Flask, render_template, request, redirect, session, url_for, jsonify, make_response, Response, json
from flask_sqlalchemy import SQLAlchemy  # 导入ORM库 SQLAlchemy
from flask_migrate import Migrate  # 导入数据库迁移工具
import os # 导入 os 库来帮助我们构建路径
from datetime import datetime # 我们需要 datetime记录默认的发布时间
from werkzeug.security import generate_password_hash, check_password_hash # 导入哈希工具，校验密码
from urllib.parse import quote
import re

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
# 初始化数据库迁移工具
migrate = Migrate(app, db)

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
    note = db.Column(db.Text, nullable=True)

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
    return render_template('interest.html')

@app.route('/about')
def show_about_page():
    """ 显示关于页 """
    return render_template('about.html')

@app.route('/blog')
def show_blog_page():
    """ 显示博客页 """
    all_posts = Post.query.order_by(Post.date_posted.desc()).all()
    # 1. 过滤掉状态为 'hidden' 的文章
    if session.get('logged_in'):
        visible_posts = all_posts  # 已登录用户可见所有文章
    else:
        visible_posts = [post for post in all_posts if post.status != 'hidden']
    # 2. 把查询到的数据传递给模板
    return render_template('blog_index.html', posts=visible_posts, login_status=session.get('logged_in'))

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

def find_title_in_content(content: str, target: str = 'title') -> str | None:
    """提取 Markdown 首个标题，或返回移除首个标题后的正文。

    支持两类标题：
    - ATX: 以一个或多个 # 开头的行（例如: # Title）
    - Setext: 标题行下一行全为 '=' 或 '-'（例如: Title\n=====）

    参数:
      content: 原始 Markdown 文本
      target: 'title' 返回标题文本；'post' 返回移除首个标题后的正文

    返回:
      - 当 target='title'：返回首个标题文本，未找到则返回 None
      - 当 target='post' ：返回移除首个标题后的正文；未找到标题则返回原内容
    """
    if content is None:
        return None if target == 'title' else ''

    lines = content.splitlines()
    n = len(lines)

    def atx_title(s: str) -> str | None:
        s1 = s.strip()
        if s1.startswith('#'):
            txt = s1.lstrip('#').strip()
            # 去掉行尾可选的关闭井号序列（例如 "# Title ####"）
            txt = re.sub(r"\s#+\s*$", "", txt).strip()
            return txt or None
        return None

    def is_all(ch: str, s: str) -> bool:
        return bool(s) and all(c == ch for c in s)

    for i in range(n):
        raw = lines[i]
        # 先识别 ATX 标题
        t = atx_title(raw)
        if t:
            if target == 'title':
                return t
            # target == 'post': 删除该行
            return "\n".join(lines[:i] + lines[i+1:])

        # 再尝试识别 Setext 标题（下一行全为 '=' 或 '-'）
        if i + 1 < n:
            title_line = raw.strip()
            underline = lines[i + 1].strip()
            if title_line and (is_all('=', underline) or is_all('-', underline)):
                if target == 'title':
                    return title_line
                # target == 'post': 删除标题行与下划线行
                return "\n".join(lines[:i] + lines[i+2:])

    # 未找到任何标题
    return None if target == 'title' else content

def strip_md_title_if_matches(content: str, db_title: str) -> str:
    """若 MD 首个标题与数据库标题相同（忽略大小写与前后空白），则返回去掉该标题后的正文，否则返回原内容。"""
    raw = content or ''
    md_title = find_title_in_content(raw, target='title')
    norm = lambda s: (s or '').strip().lower()
    if norm(md_title) == norm(db_title):
        return find_title_in_content(raw, target='post') or ''
    return raw

@app.route('/post_detail/<int:post_id>')
def post_detail(post_id):
    """ 显示文章详情页 """
    post = Post.query.get_or_404(post_id)
    post_content = strip_md_title_if_matches(post.content or '', post.title)
    # 将 Markdown 内容转换为 HTML
    post_html_from_md_body = render_md(post_content or '')
    site_title = "Post | " + post.title
    return render_template("single_post.html",
                            post=post,
                            post_html_from_md_body=post_html_from_md_body,
                            title=site_title)

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
    # 已登录：显示管理页,渲染所有博客
    all_posts = Post.query.order_by(Post.id.desc()).all()
    return render_template('management.html', posts=all_posts)

@app.route('/api/change_password', methods=['POST'])
def change_password():
    """处理修改密码请求：校验当前密码，更新为新密码，然后要求重新登录"""
    # 必须登录
    if 'logged_in' not in session:
        return redirect(url_for('login', info='请先登录后再修改密码'))

    username = session.get('username') or 'YewFence'
    admin_user = Admin.query.filter_by(username=username).first()
    if not admin_user:
        # 安全起见，找不到用户则回登录
        return redirect(url_for('login', info='用户不存在，请重新登录'))

    new_password = request.form.get('new_password', '')
    confirm_password = request.form.get('confirm_password', '')

    # 校验
    if new_password != confirm_password:
        return redirect(url_for('management', info='新密码与确认密码不匹配'))

    # 更新密码
    admin_user.set_password(new_password)
    db.session.commit()

    # 修改密码后强制登出，要求使用新密码重新登录
    session.pop('logged_in', None)
    session.pop('username', None)
    return redirect(url_for('login', info='密码已更新，请使用新密码重新登录'))

# -------------------------
# 博客更新与导出 API
# -------------------------

def _parse_date_yyyy_mm_dd(s: str):
    try:
        if not s:
            return None
        # 接收 input[type=date] 的值：YYYY-MM-DD
        return datetime.strptime(s, '%Y-%m-%d')
    except Exception:
        return None

# 统一的 Post 序列化函数
def _post_to_dict(p: Post) -> dict:
    return {
        'id': p.id,
        'title': p.title,
        'author_name': p.author_name,
        'date_posted': p.date_posted.strftime('%Y-%m-%d') if p.date_posted else None,
        'brief_summary': p.brief_summary or '',
        'note': p.note or '',
        'status': p.status,
        'content': p.content or ''
    }

@app.route('/api/posts/export_json', methods=['GET'])
def api_posts_export_json():
    if 'logged_in' not in session:
        return jsonify({ 'error': 'unauthorized' }), 401
    rows = Post.query.order_by(Post.id.desc()).all()
    payload = []
    for p in rows:
        payload.append({
            'id': p.id,
            'title': p.title,
            'author_name': p.author_name,
            'date_posted': p.date_posted.strftime('%Y-%m-%d') if p.date_posted else None,
            'brief_summary': p.brief_summary or '',
            'status': p.status,
            'note': p.note or ''
        })
    resp = make_response(jsonify(payload))
    # 提示浏览器下载为文件（可选）
    resp.headers['Content-Disposition'] = 'attachment; filename=blogs.json'
    return resp

# 以标题为文件名下载该文章的 Markdown 源文档
def _safe_filename(title: str) -> str:
    base = (title or 'post').strip()
    # 替换 Windows 不允许的字符 \\/:*?"<>|
    base = ''.join('_' if c in '\\/:*?"<>|' else c for c in base)
    # 去掉结尾的句点或空格（Windows 不允许）
    base = base.rstrip(' .') or 'post'
    # 控制长度
    if len(base) > 120:
        base = base[:120]
    return base

@app.route('/api/posts/<int:post_id>/md', methods=['GET', 'POST', 'PUT'])
def api_post_download_md(post_id: int):
    # 仅登录的管理页用户可操作
    if 'logged_in' not in session:
        return redirect(url_for('login', info='请先登录后再下载'))
    # 获取文章
    post = Post.query.get_or_404(post_id)

    if request.method in ('POST', 'PUT'):
        # 更新 Markdown 内容
        try:
            content = request.get_data(as_text=True) or ''
            post.content = content
            db.session.commit()
            return jsonify({'ok': True, 'id': post.id}), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({'ok': False, 'error': str(e)}), 500

    # GET 下载 Markdown
    content = post.content or ''
    filename_base = _safe_filename(post.title)
    filename_utf8 = quote(f"{filename_base}.md")
    resp = app.response_class(response=content, mimetype='text/markdown; charset=utf-8')
    # 提供 UTF-8 文件名
    resp.headers['Content-Disposition'] = f"attachment; filename*=UTF-8''{filename_utf8}"
    return resp

@app.route('/management/posts/<int:post_id>/preview', methods=['GET'])
def post_md_preview(post_id: int):
    # 仅登录的管理页用户可预览
    if 'logged_in' not in session:
        return redirect(url_for('login', info='请先登录后再预览'))

    post = Post.query.get_or_404(post_id)
    # 预览也应用同样的去标题逻辑
    md = strip_md_title_if_matches(post.content or '', post.title)
    post_html_from_md_body = render_md(md)
    site_title = "PostReview | " + post.title
    return render_template("single_post.html",
                            post=post,
                            post_html_from_md_body=post_html_from_md_body,
                            title=site_title)

# -------------------------
# 管理页表单提交CRUD
# -------------------------

@app.route('/management/posts/new', methods=['POST'])
def management_post_create():
    if 'logged_in' not in session:
        return redirect(url_for('login', info='请先登录后再进行操作'))

    form = request.form
    allowed_status = {'published', 'hidden'}
    try:
        p = Post()
        p.title = (form.get('title') or '').strip()
        p.author_name = (form.get('author') or '').strip() or 'YewFence'
        dv = _parse_date_yyyy_mm_dd(form.get('date') or '')
        p.date_posted = dv or datetime.utcnow()
        p.brief_summary = form.get('summary')
        p.note = form.get('note')
        st = (form.get('status') or '').strip().lower()
        p.status = st if st in allowed_status else 'hidden'
        # content 确认有一个有效的提示信息
        if 'content' in form:
            p.content = form.get('content') or ''
        else:
            p.content = '博客内容待补充...'
        # 若未填写标题，则尝试从 Markdown 内容首个一级标题推断；仍无则回退为“无标题”
        if not p.title:
            p.title = find_title_in_content(p.content or '') or '无标题'
        db.session.add(p)
        db.session.commit()
        return redirect(url_for('management'))
    except Exception:
        db.session.rollback()
        return redirect(url_for('management'))


@app.route('/management/posts/<int:post_id>/edit', methods=['POST'])
def management_post_edit(post_id: int):
    if 'logged_in' not in session:
        return redirect(url_for('login', info='请先登录后再进行操作'))

    post = Post.query.get_or_404(post_id)
    form = request.form
    allowed_status = {'published', 'hidden'}
    try:
        title = (form.get('title') or '').strip()
        author = (form.get('author') or '').strip()
        date_s = form.get('date') or ''
        if title:
            post.title = title
        if author:
            post.author_name = author
        dv = _parse_date_yyyy_mm_dd(date_s)
        if dv:
            post.date_posted = dv
        post.brief_summary = form.get('summary')
        post.note = form.get('note')
        st = (form.get('status') or '').strip().lower()
        if st in allowed_status:
            post.status = st
        # 若表单包含 content 字段，则更新（允许空字符串覆盖）
        if 'content' in form:
            post.content = form.get('content') or ''

        db.session.commit()
        return redirect(url_for('management') + f"#post-{post.id}")
    except Exception:
        db.session.rollback()
        return redirect(url_for('management') + f"#post-{post.id}")
    
@app.route('/api/posts/<int:post_id>/delete', methods=['GET'])
def api_post_delete(post_id: int):
    if 'logged_in' not in session:
        return redirect(url_for('login', info='请先登录后再进行操作'))

    post = Post.query.get_or_404(post_id)
    try:
        db.session.delete(post)
        db.session.commit()
        # todo: 信息提示
        return redirect(url_for('management'))
    except Exception:
        db.session.rollback()
        return redirect(url_for('management') + f"#post-{post.id}")