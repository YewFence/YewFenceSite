from flask import Blueprint, request, session, jsonify
from models import Admin, Post
from extensions import db
from utils import login_required

auth_bp = Blueprint('auth', __name__, url_prefix='/api')


@auth_bp.route('/auth/login', methods=['POST'])
def login():
    """处理登录请求，返回 JSON"""
    # 检查用户是否已经登录
    if 'logged_in' in session:
        return jsonify({'success': True, 'message': '已经登录'}), 200

    # 从表单获取输入的密码数据
    username = request.form.get('username', '')
    password = request.form.get('password', '')

    # 从数据库获取管理员用户
    admin_user = Admin.query.filter_by(username=username).first()

    # 校验
    if not admin_user:
        return jsonify({'success': False, 'error': '用户名不存在'}), 401

    if admin_user.check_password(password):
        # 登录成功后将登录状态存入 session
        session['logged_in'] = True
        session['username'] = admin_user.username
        return jsonify({'success': True, 'message': '登录成功', 'username': admin_user.username}), 200
    else:
        return jsonify({'success': False, 'error': '密码或用户名错误'}), 401


@auth_bp.route('/auth/logout', methods=['GET', 'POST'])
def logout():
    """处理登出请求，返回 JSON"""
    session.pop('logged_in', None)
    session.pop('username', None)
    return jsonify({'success': True, 'message': '已成功登出'}), 200


@auth_bp.route('/management/posts', methods=['GET'])
@login_required
def get_management_posts():
    """获取管理页面的文章列表数据，返回 JSON"""
    all_posts = Post.query.order_by(Post.id.desc()).all()
    posts_data = []
    for post in all_posts:
        posts_data.append({
            'id': post.id,
            'title': post.title,
            'author_name': post.author_name,
            'date_posted': post.date_posted.strftime('%Y-%m-%d') if post.date_posted else None,
            'brief_summary': post.brief_summary or '',
            'status': post.status,
            'note': post.note or ''
        })
    return jsonify({'posts': posts_data}), 200


@auth_bp.route('/auth/change_password', methods=['POST'])
@login_required
def change_password():
    """处理修改密码请求，返回 JSON"""
    username = session.get('username') or 'YewFence'
    admin_user = Admin.query.filter_by(username=username).first()

    if not admin_user:
        return jsonify({'success': False, 'error': '用户不存在，请重新登录'}), 401

    new_password = request.form.get('new_password', '')
    confirm_password = request.form.get('confirm_password', '')

    # 校验
    if new_password != confirm_password:
        return jsonify({'success': False, 'error': '新密码与确认密码不匹配'}), 400

    # 更新密码
    admin_user.set_password(new_password)
    db.session.commit()

    # 修改密码后强制登出，要求使用新密码重新登录
    session.pop('logged_in', None)
    session.pop('username', None)
    return jsonify({'success': True, 'message': '密码已更新，请使用新密码重新登录'}), 200

# 文章预览路由
@auth_bp.route('/blog/<int:post_id>/preview', methods=['GET'])
@login_required
def post_preview(post_id: int):
    post = Post.query.get_or_404(post_id)
    # 不需要检查是否隐藏状态，因为已登录用户可以预览所有文章
    # 优化：使用缓存的 HTML，如果没有则重新渲染
    if post.rendered_html:
        post_html_from_md_body = post.rendered_html
    else:
        # 首次访问或缓存失效，重新渲染并保存
        post_html_from_md_body = post.render_content()
        from extensions import db
        db.session.commit()

    post_data = {
        'id': post.id,
        'title': post.title,
        'author_name': post.author_name,
        'date_posted': post.date_posted.strftime('%Y-%m-%d') if post.date_posted else None,
        'brief_summary': post.brief_summary or '',
        'status': post.status,
        'content': post_html_from_md_body
    }

    return jsonify({'post': post_data})