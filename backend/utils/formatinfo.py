from datetime import datetime

# 工具函数
def parse_date_yyyy_mm_dd(s: str):
    """解析日期字符串 YYYY-MM-DD"""
    try:
        if not s:
            return None
        return datetime.strptime(s, '%Y-%m-%d')
    except Exception:
        return None


def safe_filename(title: str) -> str:
    """生成安全的文件名"""
    base = (title or 'post').strip()
    # 替换 Windows 不允许的字符 \\/:*?"<>|
    base = ''.join('_' if c in '\\/:*?"<>|' else c for c in base)
    # 去掉结尾的句点或空格（Windows 不允许）
    base = base.rstrip(' .') or 'post'
    # 控制长度
    if len(base) > 120:
        base = base[:120]
    return base