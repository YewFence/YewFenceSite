from flask import Blueprint, request, jsonify
from datetime import datetime
from models import Post
from extensions import db
from utils import login_required, find_title_in_content, parse_date_yyyy_mm_dd, safe_filename

crud_bp = Blueprint('crud', __name__, url_prefix='/api')

# CRUD 路由
@crud_bp.route('/posts/new', methods=['POST'])
@login_required
def create_post():
    """创建新文章"""
    form = request.form
    allowed_status = {'published', 'hidden'}

    try:
        p = Post()
        p.title = (form.get('title') or '').strip()
        p.author_name = (form.get('author') or '').strip() or 'YewFence'
        dv = parse_date_yyyy_mm_dd(form.get('date') or '')
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

        # 若未填写标题，则尝试从 Markdown 内容首个一级标题推断
        if not p.title:
            p.title = find_title_in_content(p.content or '') or '无标题'

        # 优化：创建文章时立即渲染 Markdown 并缓存
        p.render_content()

        db.session.add(p)
        db.session.commit()
        return jsonify({'success': True, 'message': '创建成功', 'post_id': p.id}), 201
    except Exception as e:
        db.session.rollback()
        print(f"创建文章失败: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500


@crud_bp.route('/posts/<int:post_id>/edit', methods=['POST'])
@login_required
def edit_post(post_id: int):
    """编辑文章"""
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

        dv = parse_date_yyyy_mm_dd(date_s)
        if dv:
            post.date_posted = dv

        post.brief_summary = form.get('summary') or ''
        post.note = form.get('note') or ''
        st = (form.get('status') or '').strip().lower()
        if st in allowed_status:
            post.status = st

        # 若表单包含 content 字段，则更新（允许空字符串覆盖）
        content_changed = False
        if 'content' in form:
            new_content = form.get('content') or ''
            if new_content and post.content != new_content:
                post.content = new_content
                content_changed = True

        # 优化：如果内容或标题变化，重新渲染 Markdown 缓存
        if content_changed or title:
            post.render_content()

        db.session.commit()
        return jsonify({'success': True, 'message': '更新成功', 'post_id': post.id}), 200
    except Exception as e:
        db.session.rollback()
        print(f"编辑文章失败: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500


@crud_bp.route('/posts/<int:post_id>/delete', methods=['GET'])
@login_required
def delete_post(post_id: int):
    """删除文章"""
    post = Post.query.get_or_404(post_id)

    try:
        db.session.delete(post)
        db.session.commit()
        return jsonify({'success': True, 'message': '删除成功'}), 200
    except Exception as e:
        db.session.rollback()
        print(f"删除文章失败: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500
