#!/bin/sh
set -e
echo "========================================="
echo "YewFence Site Frontend - Startup Script"
echo "========================================="
echo "[1/2] Starting log rotation cron job..."
# 启动 cron 守护进程
crond

echo "[2/2] Starting nginx..."
# 启动 nginx（前台运行）
exec nginx -g "daemon off;"
