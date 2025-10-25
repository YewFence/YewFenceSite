# YewFence's Site

一个简单的个人网站

## 简介

这里有YewFence的自我介绍，兴趣爱好，联系方式  
有一个博客页面，可以查看文章，这是公开的  
有一个简单的管理后台，可以登录后进行博客的管理  

## 使用工具
- HTML
- CSS
- JavaScripts
- Python 3.13
- SQLite
- Flask
- Jinja2
- Docker (可选)

## 目录结构
```
docker/              # Docker相关文件
docs/                # 文档文件夹(TODO)
migrations/          # 数据库迁移脚本
models/              # 数据库模型
routes/              # 路由定义
samples/             # 博客示例数据
scripts/             # 脚本文件夹
static/              # 静态资源文件夹
templates/           # HTML模板文件夹
utils/               # 工具函数文件夹
.env.example         # 环境变量示例文件
app.py               # 后端服务器脚本
config.py            # 配置文件加载脚本
data.db              # SQLite数据库文件(自行迁移生成)
docker-compose.yml   # Docker Compose配置文件
Dockerfile           # Dockerfile
extensions.py        # Flask扩展
LICENSE              # 许可证文件
README.md            # 项目说明文件
requirements.txt     # Python依赖库清单
seed.py              # 数据库初始化/变更脚本
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
> 如果你比较懒的话，可以在第一步输入y回车之后一路回车就好，它会自动：
> 1. 创建管理员账户，用户名：admin，密码：password
> 2. 以覆盖模式导入samples文件夹中的两个示例文章

6) 启动开发服务器
```pwsh
flask run --debug
```

7) 本地访问
- 主页：http://127.0.0.1:5000/
- 博客：http://127.0.0.1:5000/blog
- 管理：http://127.0.0.1:5000/management

## 在 macOS/Linux 上本地运行与访问（zsh/bash）

1) 克隆该项目进入项目目录

2) 创建并激活虚拟环境
```bash
python -m venv .venv
source .venv/Scripts/activate
```

1) 安装依赖
```bash
python -m pip install -r requirements.txt
```

1) 初始化数据库（使用 Flask-Migrate）
```bash
export FLASK_APP=app
flask db upgrade
```

1) 初始化管理员账户（交互式，可选）
```bash
python3 seed.py
```
按照提示创建/更新管理员账号；也可选择导入文章并设置覆盖策略。
> 如果你比较懒的话，可以在第一步输入y回车之后一路回车就好，它会自动：
> 1. 创建管理员账户，用户名：admin，密码：password
> 2. 以覆盖模式导入samples文件夹中的两个示例文章

1) 启动开发服务器
```bash
flask run --debug
```

1) 本地访问
- 主页：http://127.0.0.1:5000/
- 博客：http://127.0.0.1:5000/blog
- 管理：http://127.0.0.1:5000/management

### 一键脚本（AI这一块）
#### Windows / PowerShell
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

#### macOS / Linux (zsh/bash)
同样的，在 macOS/Linux 下也有对应的一键脚本：
```bash
bash ./scripts/setup.sh
```
功能与 PowerShell 版本一致：创建虚拟环境、安装依赖、迁移数据库、可选管理员初始化，并启动开发服务器。  
对了，这个我没测试过，买不起mac喵，还没学Linux，可能会出奇妙的问题喵，欢迎反馈。

## 常见问题
- 进不去管理页：我猜你没有创建管理员账户，运行 `python seed.py` 创建一个管理员账户即可。
- 显示找不到requirements.txt：确保你在项目根目录运行脚本/命令
- 端口被占用：添加 `--port 5050` 指定端口，例如 `flask run --debug --port 5050`。
- 表格 Markdown 渲染出问题：已启用 `tables` 扩展；请确保表格前后有空行，且每一行前后都要添加"|"。
- 忘记密码：重新运行 `python seed.py` 选择“创建/更新管理员”并根据引导操作即可重置。或者，如果你就在管理页面，直接在页面上更改密码就行，我没加旧密码校验。

## 部署到生产环境 (Docker)
感谢AptS:1547的PR  
按照1547的说法，已经支持了Docker，但我还没学喵，麻烦你们自己研究了喵

## 特别鸣谢
- 感谢 [Maorx.cn](https://maorx.cn/) 提供的灵感和参考。
- 感谢 Gemini 2.5 pro 和 GPT 5在撰写代码和文档过程中提供的帮助。
- 感谢AptS:1547 和 ice 的建议和引导。

## 许可证
MIT License © YewFence