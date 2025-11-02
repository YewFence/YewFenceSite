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
  └── entrypoint.sh  # 容器启动脚本
docs/                # 文档文件夹(TODO)
instance/           # 实例文件夹(docker运行后挂载点)
  └── data.db       # SQLite数据库文件
migrations/          # 数据库迁移脚本
models/              # 数据库模型
routes/              # 路由定义
samples/             # 博客示例数据
  ├── blog.json      # 示例文章元数据
  └── posts/         # 示例文章Markdown文件
scripts/             # 脚本文件夹
static/              # 静态资源文件夹
templates/           # HTML模板文件夹
utils/               # 工具函数文件夹
.dockerignore        # Docker构建忽略文件
.env.example         # 环境变量示例文件
app.py               # Flask应用工厂
auto_seed.py         # Docker自动初始化脚本（非交互式）
config.py            # 配置文件
docker-compose.yml   # Docker Compose配置文件
Dockerfile           # Docker镜像构建文件
extensions.py        # Flask扩展
LICENSE              # 许可证文件
README.md            # 项目说明文件
requirements.txt     # Python依赖库清单
seed.py              # 数据库初始化/变更脚本（交互式）
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

## 使用 Docker 部署（推荐生产环境）

### 快速启动

1. **克隆项目**
```bash
git clone <repository-url>
cd MyWebsite
```

2. **（可选但推荐）配置环境变量**
```bash
cp .env.example .env
```

编辑 `.env` 文件，自定义配置：
```env
# 安全密钥（生产环境必须修改！）
SECRET_KEY=your-random-secret-key-here

# 管理员账户（首次启动自动创建）
ADMIN_USERNAME=admin
ADMIN_PASSWORD=your-secure-password
```

3. **启动容器**
```bash
docker compose up -d
```

4. **访问应用**
- 主页：http://localhost:5000/
- 博客：http://localhost:5000/blog
- 管理：http://localhost:5000/login

首次启动会自动：
- ✅ 创建数据库并执行迁移
- ✅ 创建管理员账户（使用 `.env` 中配置的账户，或默认 admin/password）
- ✅ 导入示例文章（从 `samples/` 目录）

### 环境变量说明

| 变量名 | 说明 | 默认值 |
|--------|------|--------|
| `SECRET_KEY` | Flask 密钥，用于 session 加密 | `please-change-this-secret-key-in-production` |
| `ADMIN_USERNAME` | 管理员用户名 | `admin` |
| `ADMIN_PASSWORD` | 管理员密码 | `password` |

**⚠️ 安全提示**：生产环境必须修改 `SECRET_KEY` 和 `ADMIN_PASSWORD`！

生成安全密钥的方法：
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

### 常用命令

```bash
# 启动容器
docker compose up -d

# 查看日志
docker compose logs -f

# 停止容器
docker compose down

# 重启容器
docker compose restart

# 进入容器执行命令
docker compose exec web bash

# 查看容器状态
docker compose ps

# 重新构建镜像
docker compose build --no-cache
```

### 数据持久化

数据库和文章文件通过 Docker 卷挂载到本地：
- `./instance` - 数据库文件（`data.db`）
- `./posts` - Markdown 文章文件

**备份数据**：只需备份这两个目录即可。

### 常见问题

**Q: 如何重新初始化数据？**
```bash
# 方法 1：删除数据库后重启
docker compose down
rm -f instance/data.db
docker compose up -d

# 方法 2：在容器内手动运行初始化
docker compose exec web python auto_seed.py
```

**Q: 如何修改管理员密码？**
1. 登录管理后台（http://localhost:5000/login）
2. 在管理页面点击"修改密码"
3. 或者删除数据库后重启容器，使用新的环境变量

**Q: 端口被占用怎么办？**

修改 `docker-compose.yml` 中的端口映射：
```yaml
ports:
  - "8080:5000"  # 改为 8080 或其他端口
```

**Q: 容器启动失败？**

查看详细日志：
```bash
docker compose logs
```

常见原因：
- 端口冲突：修改端口映射
- 权限问题：确保 `instance/` 目录可写
- 镜像构建失败：尝试 `docker compose build --no-cache`

**感谢 AptS:1547 的 PR 为本项目添加了 Docker 支持！**  
~~虽然PR里有一堆bug~~

## 特别鸣谢
- 感谢 [Maorx.cn](https://maorx.cn/) 提供的灵感和参考。
- 感谢 Gemini 2.5 pro 和 GPT 5在撰写代码和文档过程中提供的帮助。
- 感谢AptS:1547 和 ice 的建议和引导。

## 许可证
MIT License © YewFence