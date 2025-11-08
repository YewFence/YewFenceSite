# YewFence's Site

一个简单的个人网站

## 简介

这里有YewFence的自我介绍，兴趣爱好，联系方式
有一个博客页面，可以查看文章，这是公开的
有一个简单的管理后台，可以登录后进行博客的管理

### 功能特性

- ✅ 响应式导航栏
- ✅ 深色/浅色主题切换
- ✅ 博客文章列表和详情
- ✅ 文章管理后台（CRUD操作）
- ✅ 用户登录认证
- ✅ Markdown渲染
- ✅ 博客文章Markdown文件上传和导出
- ✅ 联系方式复制到剪贴板功能

## 技术栈

### 前端
- Vue 3 (Composition API)
- Vite
- Vue Router 4
- Pinia (状态管理)
- Axios (HTTP客户端)
- 原生CSS

### 后端
- Python 3.13
- Flask
- Flask-SQLAlchemy
- Flask-Migrate
- Flask-CORS
- SQLite
- Markdown渲染

### 部署
- Docker & Docker Compose

## 项目架构

本项目采用**前后端分离**架构：

- **前端**: Vue 3 SPA，提供用户界面和交互
- **后端**: Flask RESTful API，提供数据和业务逻辑

## 目录结构

```
backend/                  # Flask后端
  ├── models/             # 数据库模型
  ├── routes/             # Flask路由（提供RESTful API）
  ├── migrations/         # 数据库迁移脚本
  ├── utils/              # 工具函数
  ├── samples/            # 博客示例数据
  ├── scripts/            # 辅助脚本
  ├── docker/             # Docker相关文件
  ├── app.py              # Flask应用工厂
  ├── config.py           # Flask配置
  ├── extensions.py       # Flask扩展（含CORS配置）
  ├── pyproject.toml      # Python项目配置
  ├── uv.lock             # uv依赖锁定文件
  ├── Dockerfile          # 后端Docker构建文件
  └── gunicorn.conf.py    # Gunicorn配置

frontend/                 # Vue 3前端
  ├── src/
  │   ├── api/            # API接口封装
  │   ├── assets/         # 静态资源（CSS、图片）
  │   ├── components/     # Vue公共组件
  │   ├── router/         # 路由配置
  │   ├── stores/         # Pinia状态管理
  │   ├── views/          # 页面组件
  │   ├── App.vue         # 根组件
  │   └── main.js         # 入口文件
  ├── public/             # 公共静态资源
  ├── docker/             # Docker相关文件
  ├── .env.development    # 开发环境变量配置
  ├── package.json        # NPM依赖
  ├── vite.config.js      # Vite配置
  └── Dockerfile          # 前端Docker构建文件

docs/                     # 文档目录 TODO
yewfence_site_data/       # 数据持久化目录（挂载卷）
.env                      # 环境变量配置 (自行创建)
.env.example              # 环境变量配置示例
docker-compose.yml        # Docker Compose配置
docker-compose.override.yml.example  # Docker Compose覆盖配置示例
```

## 快速开始

### Docker （推荐）

1. 配置环境变量
- 复制 `.env.example` 为 `.env`
```bash
cp .env.example .env
```
- 修改 `.env` 中的配置项（如有需要）
2. 启动服务
```bash
docker-compose up -d
```

Docker 会自动构建并启动前后端服务，访问 `http://localhost:8080` 即可。
> docker真好用吧

### 启动开发服务器
#### 前端（Vue 3）

1) 进入前端目录
```bash
cd frontend
```

2) 安装依赖
```bash
npm install
```

3) 配置环境变量（可选）

前端可以选择使用以下环境变量配置文件：
- `.env.development` - 开发环境配置

可以修改 `VITE_API_BASE_URL` 指向你的后端API地址。

4) 启动开发服务器
```bash
npm run dev
```

前端会在 `http://localhost:5173` 启动，并自动代理API请求到后端（如有）。

### 后端（Flask）

> 我使用 Windows / PowerShell 作为示例，Linux / macOS 用户请相应调整命令。

1) 进入后端目录

```pwsh
cd backend
```

> 如果没有安装uv，可以使用以下命令安装
```pwsh
pip install uv
```

2) 创建并初始化环境
```pwsh
uv sync
```

3) 初始化数据库（使用 Flask-Migrate）
```pwsh
$env:FLASK_APP = "app"
flask db upgrade
```

4) 初始化管理员账户（交互式）
先把辅助脚本复制到backend文件夹下
```pwsh
cp scripts/seed.py seed.py
```
运行
```pwsh
python seed.py
```

按提示选择“创建/更新管理员账户”，输入用户名和密码；如需导入文章，亦可在该脚本中选择导入并设置覆盖策略。
> 如果你比较懒的话，可以在第一步输入y回车之后一路回车就好，它会自动：
> 1. 创建管理员账户，用户名：admin，密码：password
> 2. 以覆盖模式导入samples文件夹中的两个示例文章

1) 启动开发服务器
```pwsh
flask run --debug
```

## 开发说明

### 前端开发

#### 添加新页面
1. 在 `frontend/src/views/` 创建页面组件
2. 在 `frontend/src/router/index.js` 添加路由配置
3. 在导航栏组件中添加链接（如需要）

#### 添加新API
1. 在 `frontend/src/api/` 对应的文件中添加API函数
2. 使用封装好的 `api` 实例发送请求

#### 状态管理
使用Pinia管理全局状态：
- `theme.js` - 主题状态
- `auth.js` - 认证状态

### 后端开发

Flask应用结构：
- `routes/` - API路由
- `models/` - 数据库模型
- `utils/` - 工具函数
- `migrations/` - 数据库迁移


## 常见问题
- 本地测试时进不去管理页：我猜你没有创建管理员账户，运行 `python scripts/seed.py` 创建一个管理员账户即可。
- 表格 Markdown 渲染出问题：已启用 `tables` 扩展；请确保表格前后有空行，且每一行前后都要添加"|"。
- 忘记密码：重新运行 `python scripts/seed.py` 选择"创建/更新管理员"并根据引导操作即可重置。或者，如果你就在管理页面，直接在页面上更改密码就行，我没加旧密码校验。

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

## 特别鸣谢
- 感谢[AptS:1547](https://github.com/AptS-1547)的PR提供了Docker支持
- 感谢ice的引导和建议  ~~ice都不告诉我主页，我都没得贴~~
- 感谢[别为馒头](https://github.com/ding113)提供的服务器让我部署我的网站上线
- 感谢所有提出建议的同学们
- 感谢 [Maorx.cn](https://maorx.cn/) 提供的灵感和参考。
- 感谢 Gemini 2.5 pro , GPT 5, Claude Sonnet 4.5在撰写代码和文档过程中提供的帮助。
## 许可证
MIT License © YewFence