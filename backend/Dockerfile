# 使用 Python 3.13 官方镜像
FROM python:3.13-slim

# 设置工作目录
WORKDIR /app

# 设置环境变量
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    FLASK_ENV=production

# 安装系统依赖
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# 安装 uv
RUN pip install --no-cache-dir uv

# 复制依赖文件
COPY pyproject.toml .

# 安装 Python 依赖
RUN uv pip install --system -r pyproject.toml && \
    uv pip install --system gunicorn

# 复制项目文件
COPY . .

# 复制启动脚本
COPY ./docker/entrypoint.sh ./entrypoint.sh
RUN chmod +x ./entrypoint.sh

# 创建数据目录和日志目录
RUN mkdir -p /app/instance /var/log/gunicorn

# 暴露端口
EXPOSE 5000

# 健康检查
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD python -c "from urllib.request import urlopen; urlopen('http://localhost:5000/api/health', timeout=2)" || exit 1

# 使用 entrypoint 启动
ENTRYPOINT ["./entrypoint.sh"]

