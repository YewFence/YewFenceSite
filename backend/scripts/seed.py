import json
import os
from datetime import datetime
from getpass import getpass

# 导入 Flask 应用上下文和模型
from app import create_app
from extensions import db
from models import Admin, Post

# 创建应用实例
app = create_app()

# ---------------
# 交互辅助函数
# ---------------

def ask_yn(prompt: str, default: str = 'y') -> bool:
    d = default.lower() if default in ('y', 'n') else 'y'
    hint = 'Y/n' if d == 'y' else 'y/N'
    while True:
        ans = input(f"{prompt} ({hint}): ").strip().lower()
        if not ans:
            return d == 'y'
        if ans in ('y', 'yes'):
            return True
        if ans in ('n', 'no'):
            return False
        print('请输入 y 或 n。')

def ask_str(prompt: str, default: str | None = None, allow_empty: bool = False) -> str:
    while True:
        hint = f" (默认 {default})" if default is not None else ''
        s = input(f"{prompt}{hint}: ").strip()
        if s:
            return s
        if s == '' and allow_empty:
            return ''
        if default is not None:
            return default
        print('输入不能为空。')

def parse_date(s: str | None) -> datetime:
    if not s:
        return datetime.utcnow()
    for fmt in ('%Y-%m-%d', '%Y/%m/%d', '%Y.%m.%d'):
        try:
            return datetime.strptime(s, fmt)
        except Exception:
            continue
    return datetime.utcnow()


def migrate():
    print('安全提示：该脚本会修改数据库，建议先备份 data.db。')
    if not ask_yn('你确定要继续吗？', default='n'):
        print('已取消。')
        return

    print('\n你想执行哪些操作？')
    print('1) 创建/更新管理员账户')
    print('2) 导入 JSON + MD 到数据库')
    print('3) 两者都做')
    choice = ask_str('请输入 1/2/3', default='3')
    if choice not in ('1', '2', '3', ''):
        print('无效选择，已取消。')
        return

    do_admin = choice in ('1', '3')
    do_posts = choice in ('2', '3')

    # --- 收集管理员信息 ---
    admin_username = None
    admin_password = None
    if do_admin:
        print('\n[管理员设置] 如用户已存在将更新其密码')
        admin_username = ask_str('请输入管理员用户名', default='admin')
        while True:
            p1 = getpass('请输入管理员密码(若为空则默认为password) :')
            p2 = getpass('请再次输入以确认: ')
            if p1 != p2:
                print('两次输入不一致，请重试。')
                continue
            if not p1:
                p1 = 'password'
                print('密码为空，已设置为默认密码 "password"')
            admin_password = p1
            break

    # --- 收集导入文章信息 ---
    json_path = None
    md_dir = None
    mode = None  # skip/overwrite/clear
    if do_posts:
        print('\n[导入文章] 将根据 JSON 中的 title 去 posts 目录查找同名 .md 文件')
        json_path = ask_str('请输入 blog.json 的路径', default='samples/blog.json')
        md_dir = ask_str('请输入 .md 文件所在文件夹', default='samples/posts')
        print('覆盖策略：')
        print('  1) 跳过已存在（按标题判断）')
        print('  2) 覆盖已存在（按标题更新内容与元数据）')
        print('  3) 清空数据库中的文章后再全部导入')
        m = ask_str('请选择 1/2/3', default='2')
        if m == '1':
            mode = 'skip'
        elif m == '2':
            mode = 'overwrite'
        elif m == '3':
            mode = 'clear'
        else:
            print('无效选择，已取消。')
            return

    # --- 执行 ---
    with app.app_context():
        try:
            # 管理员
            if do_admin:
                admin = Admin.query.filter_by(username=admin_username).first()
                if admin is None:
                    print(f"创建管理员: {admin_username}")
                    admin = Admin(username=admin_username)
                    admin.set_password(admin_password)
                    db.session.add(admin)
                else:
                    print(f"更新管理员密码: {admin_username}")
                    admin.set_password(admin_password)

            created = updated = skipped = md_missing = 0

            # 文章
            if do_posts:
                if mode == 'clear':
                    print('清空现有文章...')
                    Post.query.delete()

                print(f"读取 JSON: {json_path}")
                try:
                    with open(json_path, 'r', encoding='utf-8') as f:
                        entries = json.load(f)
                except FileNotFoundError:
                    print('[错误] 找不到 JSON 文件。')
                    return
                except json.JSONDecodeError as e:
                    print(f'[错误] JSON 解析失败: {e}')
                    return

                for idx, entry in enumerate(entries, start=1):
                    title = (entry.get('title') or '').strip()
                    if not title:
                        print(f"[{idx}] 跳过：缺少 title")
                        skipped += 1
                        continue

                    # 兼容不同键名
                    author = (entry.get('author_name') or entry.get('author') or 'YewFence').strip()
                    date_s = entry.get('date') or entry.get('date_posted')
                    brief = entry.get('brief_summary') or ''
                    status = (entry.get('status') or 'hidden').strip().lower()
                    note = entry.get('note') or ''

                    md_path = os.path.join(md_dir, f"{title}.md")
                    if not os.path.isfile(md_path):
                        print(f"[{idx}] [缺少MD] {md_path}")
                        md_missing += 1
                        if mode == 'skip':
                            skipped += 1
                            continue
                        # 覆盖或清空模式下，没有 MD 也可只更新元数据/创建空内容
                        md_content = ''
                    else:
                        with open(md_path, 'r', encoding='utf-8') as mf:
                            md_content = mf.read()

                    existing = Post.query.filter_by(title=title).first()
                    if existing is None:
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
                        print(f"[{idx}] 创建: {title}")
                    else:
                        if mode == 'skip':
                            skipped += 1
                            print(f"[{idx}] 跳过(已存在): {title}")
                        else:  # overwrite 或 clear 后导入
                            existing.author_name = author
                            existing.brief_summary = brief
                            existing.content = md_content
                            existing.date_posted = parse_date(date_s)
                            existing.status = status
                            existing.note = note
                            updated += 1
                            print(f"[{idx}] 覆盖: {title}")

            db.session.commit()
            print('\n迁移完成。')
            if do_admin:
                print(' - 管理员设置已应用。')
            if do_posts:
                print(f' - 文章 创建: {created}，更新: {updated}，跳过: {skipped}，缺少MD: {md_missing}')
        except Exception as e:
            db.session.rollback()
            print(f"[严重错误] 发生异常：{e}")


if __name__ == '__main__':
    migrate()