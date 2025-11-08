# 使用官方 nginx alpine 镜像
FROM nginx:alpine

# 复制自定义 nginx 配置
COPY nginx.conf /etc/nginx/nginx.conf

# 暴露 80 端口
EXPOSE 80

# 启动 nginx（默认命令）
CMD ["nginx", "-g", "daemon off;"]
