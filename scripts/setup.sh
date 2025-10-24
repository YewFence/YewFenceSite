#!/usr/bin/env bash
# 一键初始化并启动站点（macOS/Linux，zsh/bash）
# 用法：在项目根目录执行：
#   bash ./scripts/setup.sh

set -euo pipefail

info() { printf "\033[36m[INFO]\033[0m %s\n" "$*"; }
ok()   { printf "\033[32m[ OK ]\033[0m %s\n" "$*"; }
warn() { printf "\033[33m[WARN]\033[0m %s\n" "$*"; }
err()  { printf "\033[31m[ERR ]\033[0m %s\n" "$*"; }

# 1) 检查 Python 解释器
if command -v python3 >/dev/null 2>&1; then
  PY=python3
elif command -v python >/dev/null 2>&1; then
  PY=python
else
  err "未检测到 Python，请先安装 python3 并加入 PATH。"
  exit 1
fi
info "使用解释器: $($PY -V)"

# 2) 创建并激活虚拟环境
if [ ! -d .venv ]; then
  info "创建虚拟环境 .venv..."
  $PY -m venv .venv
  ok "虚拟环境创建完成"
else
  info ".venv 已存在，跳过创建"
fi

# shellcheck disable=SC1091
source .venv/bin/activate
ok "虚拟环境已激活 ($(python -V 2>/dev/null || true))"

# 3) 升级 pip
info "升级 pip..."
python -m pip install --upgrade pip >/dev/null

# 4) 安装依赖
if [ -f requirements.txt ]; then
  info "安装 requirements.txt 依赖..."
  python -m pip install -r requirements.txt
else
  warn "未找到 requirements.txt，将安装基础依赖集合（Flask/SQLAlchemy/Migrate/Markdown/Pygments）"
  python -m pip install flask flask_sqlalchemy flask_migrate sqlalchemy markdown pygments
  info "生成 requirements.txt 以便复现..."
  python -m pip freeze > requirements.txt
  ok "已生成 requirements.txt"
fi

# 5) 数据库迁移
export FLASK_APP=app
if [ -d migrations ]; then
  info "检测到 migrations 目录，执行数据库升级..."
  flask db upgrade
else
  warn "未检测到 migrations 目录，将初始化并创建首个迁移..."
  flask db init
  flask db migrate -m "init"
  flask db upgrade
fi
ok "数据库就绪"

# 6) 询问是否初始化/更新管理员账户（交互式）
read -r -p "是否运行 seed.py 初始化/更新管理员账户？(Y/n): " DO_ADMIN
DO_ADMIN=${DO_ADMIN:-Y}
case "${DO_ADMIN^^}" in
  Y|YES)
    info "启动交互式管理员/文章迁移脚本..."
    $PY seed.py
    ;;
  *)
    info "已跳过管理员初始化"
    ;;
esac

# 7) 启动开发服务器
info "启动开发服务器 (Ctrl+C 可停止)..."
flask run --debug
