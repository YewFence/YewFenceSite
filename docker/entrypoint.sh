#!/bin/bash
set -e

echo "========================================="
echo "YewFence Blog - Startup Script"
echo "========================================="

# 1. 检查数据库连接
echo "[1/4] Checking database connection..."
python -c "
from app import create_app
from extensions import db

app = create_app()
with app.app_context():
    try:
        db.engine.connect()
        print('[OK] Database connection successful')
    except Exception as e:
        print(f'[ERROR] Database connection failed: {e}')
        exit(1)
"

# 2. 执行数据库迁移
echo ""
echo "[2/4] Running database migrations..."
flask db upgrade

# 3. 检查是否需要初始化数据
echo ""
echo "[3/4] Checking data initialization status..."
NEED_INIT=$(python -c "
from app import create_app
from models import Admin
from extensions import db

app = create_app()
with app.app_context():
    admin_count = Admin.query.count()
    if admin_count == 0:
        print('yes')
    else:
        print('no')
        print(f'[OK] Found {admin_count} admin account(s)', flush=True)
" | head -n 1)

if [ "$NEED_INIT" = "yes" ]; then
    echo "[INFO] No admin accounts found. Running auto-initialization..."
    python auto_seed.py
    if [ $? -eq 0 ]; then
        echo "[OK] Auto-initialization completed successfully"
    else
        echo "[ERROR] Auto-initialization failed"
        exit 1
    fi
fi

# 4. 启动应用
echo ""
echo "========================================="
echo "[4/4] Starting Gunicorn server..."
echo "========================================="
exec gunicorn \
    --bind 0.0.0.0:5000 \
    --workers 4 \
    --threads 2 \
    --timeout 60 \
    --access-logfile - \
    --error-logfile - \
    --log-level info \
    "app:create_app()"
