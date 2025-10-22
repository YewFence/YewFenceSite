import json
import os
from datetime import datetime

# 1. 导入你的 app 实例、db 对象和模型
# 我们需要 app 来创建“上下文”
from app import app, db, Admin, Post

# -----------------------------------------------------------------
# ### TODO ###
# 请根据你的实际情况，修改下面 3 个变量！
# -----------------------------------------------------------------

# 1. 你想设置的管理员用户名
ADMIN_USERNAME = 'YewFence'

# 2. 你想设置的管理员密码 (脚本运行后，你可以删除这一行)
ADMIN_PASSWORD = 'yewfence' 

# 3. 你的 JSON 文件的路径 (根据你的截图，它在 data 文件夹里)
#    请把 'your_blogs.json' 换成你真正的文件名
JSON_FILE_PATH = os.path.join('data', 'blogs.json') 

# 4. 你的 .md 文件所在的文件夹 (根据你的截图，它在 posts 文件夹里)
MD_FILES_DIR = 'posts'

# -----------------------------------------------------------------


def migrate():
    """
    执行数据迁移的主函数
    """
    
    # 2. 创建一个应用上下文
    # 这让脚本能像 Flask 应用一样访问数据库
    ctx = app.app_context()
    ctx.push()
    
    print("应用上下文已创建。")

    # --- 任务一：创建管理员账户 ---
    
    # 检查管理员是否已存在
    if Admin.query.filter_by(username=ADMIN_USERNAME).first() is None:
        print(f"正在创建管理员: {ADMIN_USERNAME}...")
        
        # 使用我们之前在 Admin 模型里定义的 set_password 方法
        admin_user = Admin(username=ADMIN_USERNAME)
        admin_user.set_password(ADMIN_PASSWORD)
        
        db.session.add(admin_user)
        print("管理员创建成功。")
    else:
        print(f"管理员 '{ADMIN_USERNAME}' 已存在，跳过创建。")

    # --- 任务二：迁移博客文章 ---
    
    print(f"正在打开 JSON 文件: {JSON_FILE_PATH}...")
    try:
        with open(JSON_FILE_PATH, 'r', encoding='utf-8') as f:
            blog_entries = json.load(f)
    except FileNotFoundError:
        print(f"[错误] JSON 文件未找到！请检查 'JSON_FILE_PATH' 变量。")
        ctx.pop()
        return
    except json.JSONDecodeError:
        print(f"[错误] JSON 文件格式错误，无法解析。")
        ctx.pop()
        return

    print(f"找到 {len(blog_entries)} 篇博客。开始迁移...")
    
    migrated_count = 0
    for entry in blog_entries:
        
        # 检查文章是否已存在 (用标题作为唯一标识)
        if Post.query.filter_by(title=entry['title']).first() is not None:
            print(f"  > 跳过 (已存在): {entry['title']}")
            continue

        print(f"  > 正在迁移: {entry['title']}")

        # 1. 读取 .md 文件内容
        md_file_path = os.path.join(MD_FILES_DIR, entry['md_file'])
        try:
            with open(md_file_path, 'r', encoding='utf-8') as md_f:
                post_content = md_f.read()
        except FileNotFoundError:
            print(f"    [错误] .md 文件未找到: {md_file_path}。跳过此篇。")
            continue
            
        # 2. 转换日期字符串 (你的格式是 "YYYY-MM-DD")
        try:
            post_date = datetime.strptime(entry['date'], '%Y-%m-%d')
        except ValueError:
            print(f"    [警告] 日期格式错误: {entry['date']}。使用当前时间代替。")
            post_date = datetime.utcnow()

        # 3. 使用 ORM 创建 Post 对象
        # (我们忽略了 json 里的 "id"，让数据库自动生成)
        new_post = Post(
            title=entry['title'],
            author_name=entry['author'],
            brief_summary=entry['brief_summary'],
            content=post_content,
            date_posted=post_date,
            status=entry['status']
        )
        
        db.session.add(new_post)
        migrated_count += 1

    # --- 任务三：提交所有更改 ---
    
    try:
        db.session.commit()
        print(f"\n迁移成功！")
        print(f"成功创建/验证管理员。")
        print(f"成功迁移 {migrated_count} 篇新博客。")
        
    except Exception as e:
        db.session.rollback() # 如果出错，回滚所有操作
        print(f"\n[!!! 严重错误 !!!] 提交到数据库时发生错误: {e}")
        print("所有更改已被回滚。")
        
    finally:
        # 4. 弹出（关闭）上下文
        ctx.pop()
        print("应用上下文已关闭。")


# --- 脚本的入口 ---
if __name__ == "__main__":
    migrate()