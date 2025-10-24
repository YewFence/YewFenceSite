# YewFence's Site

一个简单的个人网站，在AI的帮助下完成

## 简介

这里有YewFence的自我介绍，兴趣爱好，联系方式
有一个博客页面，可以查看文章，这是对外的
有一个简单的管理后台，可以登录后发表文章，删除文章

## 使用工具
- HTML
- CSS
- JavaScripts
- Python 3.13
- SQLite
- Flask

## 目录结构
```
MyWebsite/
  templates/        # HTML模板文件夹
    index.html        # 首页
    about.html        # 关于我
    interest.html     # 兴趣爱好
    contact.html      # 联系我
  blog_index.html   # 文章列表页
    single_post.html  # 文章详情页
    management.html   # 管理页面
  migrations/         # python数据库迁移脚本（自动生成的，看不懂喵）
  static/             # 静态资源文件夹
    css/
      style.css       # 全站通用样式
      post.css        # 文章页面样式
      management_style.css  # 管理页面样式
    js/
      main.js         # 通用交互脚本
      management.js   # 管理页面交互脚本
    images/           # 图片资源文件夹
      Gemini_YewFence.png # 背景图片
  README.md         # 当前说明文件
  .gitignore        # Git忽略文件清单
  data.db           # SQLite数据库文件
  app.py            # 后端服务器脚本
  requirements.txt  # Python依赖库清单
```

## 本地运行与访问（Windows / PowerShell）

1) 克隆本仓库到本地，并进入目录

2) 创建并激活虚拟环境
```pwsh
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

3) 安装依赖
```pwsh
python -m pip install -r requirements.txt
```

4) 初始化数据库（使用 Flask-Migrate）
```pwsh
$env:FLASK_APP = "app"
flask db upgrade
```

5) 初始化管理员账户（交互式）
```pwsh
python seed.py
```
按提示选择“创建/更新管理员账户”，输入用户名和密码；如需导入文章，亦可在该脚本中选择导入并设置覆盖策略。

6) 启动开发服务器
```pwsh
flask run --debug
```

7) 本地访问
- 主页：http://127.0.0.1:5000/
- 博客：http://127.0.0.1:5000/blog
- 管理：http://127.0.0.1:5000/management

## 在 macOS 上本地运行与访问（zsh/bash）

1) 打开终端并进入项目目录

2) 创建并激活虚拟环境
```bash
python -m venv .venv
source .venv/bin/activate
```

3) 安装依赖
```bash
python -m pip install -r requirements.txt
```

4) 初始化数据库（使用 Flask-Migrate）
```bash
export FLASK_APP=app
flask db upgrade
```
如果你的项目是第一次使用迁移（还没有 migrations 目录），请先执行：
```bash
flask db init
flask db migrate -m "init"
flask db upgrade
```

5) 初始化管理员账户（交互式，可选）
```bash
python3 seed.py
```
按照提示创建/更新管理员账号；也可选择导入文章并设置覆盖策略。

6) 启动开发服务器
```bash
flask run --debug
```

7) 本地访问
- 主页：http://127.0.0.1:5000/
- 博客：http://127.0.0.1:5000/blog
- 管理：http://127.0.0.1:5000/management

### 一键脚本（AI这一块）
如果你想一键完成环境准备、数据库迁移、可选的管理员初始化，并直接启动服务，可在项目根目录运行：
```pwsh
./scripts/setup.ps1
```
脚本将自动：
- 检查 Python → 创建并激活 .venv
- 安装依赖（优先使用 requirements.txt；否则安装基础依赖并自动生成 requirements.txt）
- 初始化或升级数据库（Flask-Migrate）
- 询问你是否运行 `seed.py` 初始化/更新管理员或导入文章（交互式）
- 启动 `flask run --debug`

在 macOS/Linux 下也有对应的一键脚本：
```bash
bash ./scripts/setup.sh
```
功能与 PowerShell 版本一致：创建虚拟环境、安装依赖、迁移数据库、可选管理员初始化，并启动开发服务器。  
对了，这个我没测试过，买不起mac喵，还没学Linux，可能会出奇妙的问题喵，欢迎反馈。

## 常见问题
- 进不去管理页：我猜你没有创建管理员账户，重新运行 `python seed.py` 创建一个管理员账户即可。对了，我没加用户名校验，密码正确就好了，用户名别重复就行
- 显示找不到requirements.txt：确保你在项目根目录运行命令
- 端口被占用：添加 `--port 5050` 指定端口，例如 `flask run --debug --port 5050`。
- 表格 Markdown 渲染出问题：已启用 `tables` 扩展；请确保表格前后有空行，且前后要添加"|"。
- 管理员忘记密码：重新运行 `python seed.py` 选择“创建/更新管理员”即可重置。或者，如果你就在管理页面，直接输入新密码就行，我没加旧密码校验。

## 部署到生产环境
不懂喵，欢迎 PR

## 特别鸣谢
- 感谢 [Maorx.cn](https://maorx.cn/) 提供的灵感和参考。
- 感谢 Gemini 2.5 pro 和 GPT 5在撰写代码和文档过程中提供的帮助。
- 感谢AptS:1547 和 ice 的建议和引导。

## 许可证
MIT License © YewFence