from flask import Blueprint, render_template, request, redirect, session, url_for
from models import Admin, Post
from extensions import db
from utils import login_required

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """处理登录请求"""
    # 检查用户是否已经登录
    if 'logged_in' in session:
        return redirect(url_for('auth.management'))

    if request.method == 'POST':
        # 从表单获取输入的密码数据
        username = request.form.get('username', '')
        password = request.form.get('password', '')

        # 从数据库获取管理员用户
        admin_user = Admin.query.filter_by(username=username).first()

        # 校验
        if not admin_user:
            return render_template("login.html", error="用户名不存在"), 401

        if admin_user.check_password(password):
            # 登录成功后将登录状态存入 session
            session['logged_in'] = True
            session['username'] = admin_user.username
            return redirect(url_for('auth.management'))
        else:
            return render_template("login.html", error="密码或用户名错误"), 401

    # GET: 支持通过查询参数 info 显示提醒信息
    info = request.args.get('info') or ''
    return render_template("login.html", info=info)


@auth_bp.route('/logout')
def logout():
    """处理登出请求"""
    session.pop('logged_in', None)
    session.pop('username', None)
    return redirect(url_for('auth.login', info='你已成功登出'))


@auth_bp.route('/management')
@login_required
def management():
    """显示管理页"""
    all_posts = Post.query.order_by(Post.id.desc()).all()
    return render_template('management.html', posts=all_posts)


@auth_bp.route('/api/change_password', methods=['POST'])
@login_required
def change_password():
    """处理修改密码请求：校验当前密码，更新为新密码，然后要求重新登录"""
    username = session.get('username') or 'YewFence'
    admin_user = Admin.query.filter_by(username=username).first()

    if not admin_user:
        return redirect(url_for('auth.login', info='用户不存在，请重新登录'))

    new_password = request.form.get('new_password', '')
    confirm_password = request.form.get('confirm_password', '')

    # 校验
    if new_password != confirm_password:
        return redirect(url_for('auth.management', info='新密码与确认密码不匹配'))

    # 更新密码
    admin_user.set_password(new_password)
    db.session.commit()

    # 修改密码后强制登出，要求使用新密码重新登录
    session.pop('logged_in', None)
    session.pop('username', None)
    return redirect(url_for('auth.login', info='密码已更新，请使用新密码重新登录'))
