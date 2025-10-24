from datetime import datetime
from extensions import db


class Post(db.Model):
    """文章模型"""
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    author_name = db.Column(db.String(80), default='YewFence')
    brief_summary = db.Column(db.Text)
    content = db.Column(db.Text, nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, index=True)
    status = db.Column(db.String(30), nullable=False, default='draft', index=True)
    note = db.Column(db.Text, nullable=True)

    # Markdown 渲染缓存
    rendered_html = db.Column(db.Text, nullable=True)

    def __repr__(self):
        """返回字符串表示"""
        return f'<Post {self.title}>'

    def render_content(self):
        """渲染并缓存 Markdown 内容"""
        from utils.markdown_helper import render_md, strip_md_title_if_matches

        # 去掉标题（如果与数据库标题重复）
        content_without_title = strip_md_title_if_matches(self.content or '', self.title)
        # 渲染为 HTML
        self.rendered_html = render_md(content_without_title or '')
        return self.rendered_html
