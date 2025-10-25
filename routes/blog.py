from flask import Blueprint, render_template, session
from models import Post
from utils import render_md, strip_md_title_if_matches

blog_bp = Blueprint('blog', __name__)


@blog_bp.route('/blog')
def index():
    """显示博客列表页"""
    # 优化：直接在数据库层过滤，而不是加载所有文章后再过滤
    if session.get('logged_in'):
        # 已登录用户可见所有文章
        visible_posts = Post.query.order_by(Post.date_posted.desc()).all()
    else:
        # 未登录用户只能看到 published 状态的文章
        visible_posts = Post.query.filter(Post.status != 'hidden')\
                                  .order_by(Post.date_posted.desc()).all()

    return render_template('blog_index.html', posts=visible_posts, login_status=session.get('logged_in'))


@blog_bp.route('/post_detail/<int:post_id>')
def post_detail(post_id):
    """显示文章详情页"""
    post = Post.query.get_or_404(post_id)

    if post.status == 'hidden' and not session.get('logged_in'):
        return render_template("404.html"), 404

    # 优化：使用缓存的 HTML，如果没有则重新渲染
    if post.rendered_html:
        post_html_from_md_body = post.rendered_html
    else:
        # 首次访问或缓存失效，重新渲染并保存
        post_html_from_md_body = post.render_content()
        from extensions import db
        db.session.commit()

    site_title = "Post | " + post.title

    return render_template("single_post.html",
                          post=post,
                          post_html_from_md_body=post_html_from_md_body,
                          title=site_title)
