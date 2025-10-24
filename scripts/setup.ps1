# 一键初始化并启动站点（Windows PowerShell）
# 用法：在项目根目录右键“在 PowerShell 中打开”，然后运行：
#   .\scripts\setup.ps1

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

function Write-Info($msg) { Write-Host "[INFO] $msg" -ForegroundColor Cyan }
function Write-Ok($msg)   { Write-Host "[ OK ] $msg" -ForegroundColor Green }
function Write-Warn($msg) { Write-Host "[WARN] $msg" -ForegroundColor Yellow }
function Write-Err($msg)  { Write-Host "[ERR ] $msg" -ForegroundColor Red }

# 1) 检查 Python
Write-Info "检查 Python..."
try {
    $pyVersion = (& python --version) 2>$null
    if (-not $pyVersion) { throw "python 未找到" }
    Write-Ok "已找到 $pyVersion"
}
catch {
    Write-Err "未检测到 Python。请先安装 Python，并将其加入 PATH。"
    exit 1
}

# 2) 创建并激活虚拟环境
if (-not (Test-Path .venv)) {
    Write-Info "创建虚拟环境 .venv..."
    python -m venv .venv
    Write-Ok "虚拟环境创建完成"
} else {
    Write-Info ".venv 已存在，跳过创建"
}

Write-Info "激活虚拟环境..."
. .\.venv\Scripts\Activate.ps1
Write-Ok "虚拟环境已激活"

# 3) 升级 pip
Write-Info "升级 pip..."
python -m pip install --upgrade pip

# 4) 安装依赖（优先使用 requirements.txt；否则安装基础依赖）
if (Test-Path requirements.txt) {
    Write-Info "安装 requirements.txt 依赖..."
    python -m pip install -r requirements.txt
} else {
    Write-Warn "未找到 requirements.txt，将安装基础依赖集合（Flask/SQLAlchemy/Migrate/Markdown/Pygments）"
    python -m pip install flask flask_sqlalchemy flask_migrate sqlalchemy markdown pygments
    # 可选：生成一份 requirements.txt 方便后续复现
    (python -m pip freeze) | Set-Content -Encoding UTF8 requirements.txt
    Write-Ok "已生成 requirements.txt"
}

# 5) 数据库迁移
$env:FLASK_APP = "app"
if (Test-Path migrations) {
    Write-Info "检测到 migrations 目录，执行数据库升级..."
    flask db upgrade
} else {
    Write-Warn "未检测到 migrations 目录，将初始化并创建首个迁移..."
    flask db init
    flask db migrate -m "init"
    flask db upgrade
}
Write-Ok "数据库就绪"

# 6) 询问是否初始化/更新管理员账户（交互式）
$doAdmin = Read-Host "是否运行 seed.py 初始化/更新管理员账户？(Y/n)"
if ([string]::IsNullOrWhiteSpace($doAdmin) -or $doAdmin.ToLower() -eq 'y' -or $doAdmin.ToLower() -eq 'yes') {
    Write-Info "启动交互式管理员/文章迁移脚本..."
    python seed.py
} else {
    Write-Info "已跳过管理员初始化"
}

# 7) 启动开发服务器
Write-Info "启动开发服务器 (Ctrl+C 可停止)..."
flask run --debug
