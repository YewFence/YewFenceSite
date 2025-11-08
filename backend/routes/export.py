from flask import Blueprint, request, jsonify, make_response, json, current_app
from urllib.parse import quote
import io
import zipfile
from models import Post
from extensions import db
from utils import login_required, parse_date_yyyy_mm_dd, safe_filename

export_bp = Blueprint('export', __name__, url_prefix='/api')

# 导出相关路由
@export_bp.route('/posts/export_json', methods=['GET'])
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


@export_bp.route('/posts/<int:post_id>/md', methods=['GET', 'POST', 'PUT'])
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
    filename_base = safe_filename(post.title)
    filename_utf8 = quote(f"{filename_base}.md")

    resp = current_app.response_class(response=content, mimetype='text/markdown; charset=utf-8')
    resp.headers['Content-Disposition'] = f"attachment; filename*=UTF-8''{filename_utf8}"
    return resp


@export_bp.route('/posts/export_md_zip', methods=['GET'])
@login_required
def export_md_zip():
    """导出所有文章为 ZIP 压缩包"""
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        all_posts = Post.query.order_by(Post.id.desc()).all()
        for post in all_posts:
            filename_base = safe_filename(post.title)
            filename = f"{filename_base}.md"
            content = post.content or ''
            zip_file.writestr(filename, content)

    zip_buffer.seek(0)
    resp = make_response(zip_buffer.read())
    resp.headers['Content-Type'] = 'application/zip'
    resp.headers['Content-Disposition'] = "attachment; filename=all_posts_md.zip"
    return resp