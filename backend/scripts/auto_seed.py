#!/usr/bin/env python3
"""
自动初始化脚本 - 用于 Docker 容器启动时的非交互式初始化

支持通过环境变量自定义配置：
- ADMIN_USERNAME: 管理员用户名（默认：admin）
- ADMIN_PASSWORD: 管理员密码（默认：password）
- SAMPLE_JSON: 示例文章 JSON 路径（默认：samples/blog.json）
- SAMPLE_POSTS_DIR: 示例文章 MD 目录（默认：samples/posts）
"""
import json
import os
from datetime import datetime

from app import create_app
from extensions import db
from models import Admin, Post

app = create_app()

# 从环境变量读取配置
ADMIN_USERNAME = os.environ.get('ADMIN_USERNAME', 'admin')
ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD', 'password')
SAMPLE_JSON = os.environ.get('SAMPLE_JSON', 'samples/blog.json')
SAMPLE_POSTS_DIR = os.environ.get('SAMPLE_POSTS_DIR', 'samples/posts')


def parse_date(s: str | None) -> datetime:
    """解析日期字符串，失败则返回当前时间"""
    if not s:
        return datetime.utcnow()
    for fmt in ('%Y-%m-%d', '%Y/%m/%d', '%Y.%m.%d'):
        try:
            return datetime.strptime(s, fmt)
        except Exception:
            continue
    return datetime.utcnow()


def auto_initialize():
    """自动初始化数据库"""
    print('[Auto Seed] Starting automatic initialization...')
    print(f'[Auto Seed] Admin username: {ADMIN_USERNAME}')

    with app.app_context():
        try:
            # 1. 创建默认管理员账户
            admin = Admin.query.filter_by(username=ADMIN_USERNAME).first()
            if admin is None:
                print(f'[Auto Seed] Creating admin account: {ADMIN_USERNAME}')
                admin = Admin(username=ADMIN_USERNAME)
                admin.set_password(ADMIN_PASSWORD)
                db.session.add(admin)
                print('[Auto Seed] Admin account created')
            else:
                print(f'[Auto Seed] Admin account already exists: {ADMIN_USERNAME}')

            # 2. 导入示例文章（如果存在）
            json_path = SAMPLE_JSON
            md_dir = SAMPLE_POSTS_DIR

            if not os.path.isfile(json_path):
                print(f'[Auto Seed] Sample data not found: {json_path}')
                print('[Auto Seed] Skipping post import')
            else:
                print(f'[Auto Seed] Importing posts from {json_path}...')

                with open(json_path, 'r', encoding='utf-8') as f:
                    entries = json.load(f)

                created = skipped = md_missing = 0

                for idx, entry in enumerate(entries, start=1):
                    title = (entry.get('title') or '').strip()
                    if not title:
                        print(f'[Auto Seed] [{idx}] Skipped: missing title')
                        skipped += 1
                        continue

                    # 检查文章是否已存在
                    existing = Post.query.filter_by(title=title).first()
                    if existing:
                        print(f'[Auto Seed] [{idx}] Skipped: "{title}" already exists')
                        skipped += 1
                        continue

                    # 提取元数据
                    author = (entry.get('author_name') or entry.get('author') or 'YewFence').strip()
                    date_s = entry.get('date') or entry.get('date_posted')
                    brief = entry.get('brief_summary') or ''
                    status = (entry.get('status') or 'hidden').strip().lower()
                    note = entry.get('note') or ''

                    # 读取 Markdown 内容
                    md_path = os.path.join(md_dir, f"{title}.md")
                    if not os.path.isfile(md_path):
                        print(f'[Auto Seed] [{idx}] Warning: MD file not found: {md_path}')
                        md_missing += 1
                        md_content = ''
                    else:
                        with open(md_path, 'r', encoding='utf-8') as mf:
                            md_content = mf.read()

                    # 创建文章
                    post = Post(
                        title=title,
                        author_name=author,
                        brief_summary=brief,
                        content=md_content,
                        date_posted=parse_date(date_s),
                        status=status,
                        note=note
                    )
                    db.session.add(post)
                    created += 1
                    print(f'[Auto Seed] [{idx}] Created: "{title}"')

                print(f'[Auto Seed] Post import summary: created={created}, skipped={skipped}, md_missing={md_missing}')

            # 3. 提交所有更改
            db.session.commit()
            print('[Auto Seed] Initialization completed successfully')
            return True

        except Exception as e:
            db.session.rollback()
            print(f'[Auto Seed] ERROR: {e}')
            import traceback
            traceback.print_exc()
            return False


if __name__ == '__main__':
    success = auto_initialize()
    exit(0 if success else 1)
