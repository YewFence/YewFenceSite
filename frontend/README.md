# YewFence's Site - Vue 3 Frontend

这是YewFence个人网站的Vue 3前端项目。

## 技术栈

- **框架**: Vue 3 (Composition API)
- **构建工具**: Vite
- **路由**: Vue Router 4
- **状态管理**: Pinia
- **HTTP客户端**: Axios
- **样式**: 原生CSS

## 开发环境设置

### 安装依赖

```bash
npm install
```

### 启动开发服务器

```bash
npm run dev
```

开发服务器会在 `http://localhost:5173` 启动。

### 构建生产版本

```bash
npm run build
```

构建产物会输出到 `dist/` 目录。

### 预览生产版本

```bash
npm run preview
```

## 环境变量配置

- `.env.development` - 开发环境配置
- `.env.production` - 生产环境配置

修改 `VITE_API_BASE_URL` 指向你的后端API地址。

## 项目结构

```
src/
├── api/              # API接口封装
├── assets/           # 静态资源（CSS、图片）
├── components/       # 公共组件
├── router/           # 路由配置
├── stores/           # Pinia状态管理
├── views/            # 页面组件
├── App.vue           # 根组件
└── main.js           # 入口文件
```

## 部署

### 静态部署

将 `dist/` 目录部署到任何静态文件服务器（Nginx、Apache、Vercel等）。

### Nginx配置示例

```nginx
server {
    listen 80;
    server_name your-domain.com;

    root /path/to/dist;
    index index.html;

    # Vue Router History模式支持
    location / {
        try_files $uri $uri/ /index.html;
    }

    # API代理到Flask后端
    location /api {
        proxy_pass http://localhost:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location /blog {
        proxy_pass http://localhost:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

## 功能特性

- ✅ 响应式导航栏
- ✅ 深色/浅色主题切换
- ✅ 博客文章列表和详情
- ✅ 文章管理后台（CRUD操作）
- ✅ 用户登录认证
- ✅ Markdown渲染
- ✅ 文件上传和导出
- ✅ 复制到剪贴板功能

## 开发说明

### 添加新页面

1. 在 `src/views/` 创建页面组件
2. 在 `src/router/index.js` 添加路由配置
3. 在导航栏组件中添加链接（如需要）

### 添加新API

1. 在 `src/api/` 对应的文件中添加API函数
2. 使用封装好的 `api` 实例发送请求

### 状态管理

使用Pinia管理全局状态：
- `theme.js` - 主题状态
- `auth.js` - 认证状态

## License

MIT
