# 使用官方镜像作为基础镜像
FROM node:20-alpine AS builder

# 启用 corepack 并安装 pnpm
RUN corepack enable && corepack prepare pnpm@latest --activate

# 设置工作目录
WORKDIR /app

# 复制 package.json 和 pnpm-lock.yaml
COPY package.json pnpm-lock.yaml ./

# 安装依赖（使用 frozen-lockfile 确保依赖版本一致）
RUN pnpm install --frozen-lockfile

# 复制源代码
COPY . .

# 构建生产版本
RUN pnpm build

# 构建产物在 /app/dist 目录

# 使用轻量级的 Nginx 镜像来运行生产版本
FROM nginx:alpine

# 复制构建产物到 Nginx 目录
COPY --from=builder /app/dist /usr/share/nginx/html

# 复制自定义的 Nginx 配置文件（如果有）
COPY ./nginx.conf /etc/nginx/conf.d/default.conf

# 暴露端口 80
EXPOSE 80

# 启动 Nginx
CMD ["nginx", "-g", "daemon off;"]