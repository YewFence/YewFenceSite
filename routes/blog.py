from flask import Blueprint, render_template, session, jsonify
from models import Post
from utils import render_md

blog_bp = Blueprint('blog', __name__, url_prefix='/api')


@blog_bp.route('/blog')
def index():
    """返回博客列表JSON数据"""
    # 优化：直接在数据库层过滤，而不是加载所有文章后再过滤
    if session.get('logged_in'):
        # 已登录用户可见所有文章
        visible_posts = Post.query.order_by(Post.date_posted.desc()).all()
    else:
        # 未登录用户只能看到 published 状态的文章
        visible_posts = Post.query.filter(Post.status != 'hidden')\
                                  .order_by(Post.date_posted.desc()).all()

    posts_data = []
    for post in visible_posts:
        posts_data.append({
            'id': post.id,
            'title': post.title,
            'author_name': post.author_name,
            'date_posted': post.date_posted.strftime('%Y-%m-%d') if post.date_posted else None,
            'brief_summary': post.brief_summary or '',
            'note': post.note or '',
            'status': post.status
        })

    return jsonify({'posts': posts_data, 'login_status': session.get('logged_in')})


@blog_bp.route('/blog/<int:post_id>')
def post_detail(post_id):
    """返回文章详情JSON数据"""
    post = Post.query.get_or_404(post_id)

    if post.status == 'hidden' and not session.get('logged_in'):
        return jsonify({'error': '文章不存在'}), 404

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
