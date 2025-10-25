from flask import Blueprint, request, redirect, url_for, jsonify, make_response, json
from datetime import datetime
from urllib.parse import quote
import io
import zipfile

from models import Post
from extensions import db
from utils import login_required, render_md, find_title_in_content, strip_md_title_if_matches

api_bp = Blueprint('api', __name__, url_prefix='/api')


# 工具函数
def _parse_date_yyyy_mm_dd(s: str):
    """解析日期字符串 YYYY-MM-DD"""
    try:
        if not s:
            return None
        return datetime.strptime(s, '%Y-%m-%d')
    except Exception:
        return None


def _safe_filename(title: str) -> str:
    """生成安全的文件名"""
    base = (title or 'post').strip()
    # 替换 Windows 不允许的字符 \\/:*?"<>|
    base = ''.join('_' if c in '\\/:*?"<>|' else c for c in base)
    # 去掉结尾的句点或空格（Windows 不允许）
    base = base.rstrip(' .') or 'post'
    # 控制长度
    if len(base) > 120:
        base = base[:120]
    return base


# 导出相关路由
@api_bp.route('/posts/export_json', methods=['GET'])
@login_required
def export_json():
    """导出所有文章为 JSON 格式"""
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

    # 直接用 UTF-8 文本返回，避免中文被转义为 \uXXXX
    body = json.dumps(payload, ensure_ascii=False)
    resp = make_response(body)
    resp.headers['Content-Type'] = 'application/json; charset=utf-8'
    resp.headers['Content-Disposition'] = 'attachment; filename=blog.json'
    return resp


@api_bp.route('/posts/<int:post_id>/md', methods=['GET', 'POST', 'PUT'])
@login_required
def post_markdown(post_id: int):
    """下载或更新文章的 Markdown 内容"""
    post = Post.query.get_or_404(post_id)

    if request.method in ('POST', 'PUT'):
        # 更新 Markdown 内容
        try:
            content = request.get_data(as_text=True) or ''
            post.content = content
            # 优化：更新 Markdown 后重新渲染缓存
            post.render_content()
            db.session.commit()
            return jsonify({'ok': True, 'id': post.id}), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({'ok': False, 'error': str(e)}), 500

    # GET 下载 Markdown
    content = post.content or ''
    filename_base = _safe_filename(post.title)
    filename_utf8 = quote(f"{filename_base}.md")

    from flask import current_app
    resp = current_app.response_class(response=content, mimetype='text/markdown; charset=utf-8')
    resp.headers['Content-Disposition'] = f"attachment; filename*=UTF-8''{filename_utf8}"
    return resp


@api_bp.route('/posts/export_md_zip', methods=['GET'])
@login_required
def export_md_zip():
    """导出所有文章为 ZIP 压缩包"""
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        all_posts = Post.query.order_by(Post.id.desc()).all()
        for post in all_posts:
            filename_base = _safe_filename(post.title)
            filename = f"{filename_base}.md"
            content = post.content or ''
            zip_file.writestr(filename, content)

    zip_buffer.seek(0)
    resp = make_response(zip_buffer.read())
    resp.headers['Content-Type'] = 'application/zip'
    resp.headers['Content-Disposition'] = "attachment; filename=all_posts_md.zip"
    return resp


# 文章预览路由
@api_bp.route('/posts/<int:post_id>/preview', methods=['GET'])
@login_required
def post_preview(post_id: int):
    """预览文章"""
    from flask import render_template
    post = Post.query.get_or_404(post_id)
    md = strip_md_title_if_matches(post.content or '', post.title)
    post_html_from_md_body = render_md(md)
    site_title = "PostReview | " + post.title
    return render_template("single_post.html",
                          post=post,
                          post_html_from_md_body=post_html_from_md_body,
                          title=site_title)


# CRUD 路由
@api_bp.route('/posts/new', methods=['POST'])
@login_required
def create_post():
    """创建新文章"""
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

        # 若未填写标题，则尝试从 Markdown 内容首个一级标题推断
        if not p.title:
            p.title = find_title_in_content(p.content or '') or '无标题'

        # 优化：创建文章时立即渲染 Markdown 并缓存
        p.render_content()

        db.session.add(p)
        db.session.commit()
        return redirect(url_for('auth.management'))
    except Exception as e:
        db.session.rollback()
        print(f"创建文章失败: {str(e)}")
        return redirect(url_for('auth.management'))


@api_bp.route('/posts/<int:post_id>/edit', methods=['POST'])
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

        dv = _parse_date_yyyy_mm_dd(date_s)
        if dv:
            post.date_posted = dv

        post.brief_summary = form.get('summary')
        post.note = form.get('note')
        st = (form.get('status') or '').strip().lower()
        if st in allowed_status:
            post.status = st

        # 若表单包含 content 字段，则更新（允许空字符串覆盖）
        content_changed = False
        if 'content' in form:
            new_content = form.get('content') or ''
            if post.content != new_content:
                post.content = new_content
                content_changed = True

        # 优化：如果内容或标题变化，重新渲染 Markdown 缓存
        if content_changed or title:
            post.render_content()

        db.session.commit()
        return redirect(url_for('auth.management') + f"#post-{post.id}")
    except Exception as e:
        db.session.rollback()
        print(f"编辑文章失败: {str(e)}")
        return redirect(url_for('auth.management') + f"#post-{post.id}")


@api_bp.route('/posts/<int:post_id>/delete', methods=['GET'])
@login_required
def delete_post(post_id: int):
    """删除文章"""
    post = Post.query.get_or_404(post_id)

    try:
        db.session.delete(post)
        db.session.commit()
        return redirect(url_for('auth.management'))
    except Exception as e:
        db.session.rollback()
        print(f"删除文章失败: {str(e)}")
        return redirect(url_for('auth.management') + f"#post-{post.id}")
