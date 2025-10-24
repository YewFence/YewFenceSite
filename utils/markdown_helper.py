import re

# Markdown 渲染函数
try:
    from markdown import markdown as _md_render

    def render_md(text: str) -> str:
        """渲染 Markdown 文本为 HTML

        启用扩展：
        - extra: 一揽子功能（abbr、attr_list、def_list、fenced_code、footnotes、tables、smarty 等）
        - tables: 显式开启表格，确保管道表语法被识别
        - attr_list: 支持 {#id .class} 属性列表
        - sane_lists: 更贴近 GFM 的列表解析，减少与表格的歧义
        - fenced_code: 三反引号代码块
        - codehilite: 代码高亮（需要 Pygments）
        - toc: 目录（根据标题生成）
        """
        exts = [
            'extra',
            'tables',
            'attr_list',
            'sane_lists',
            'fenced_code',
            'codehilite',
            'toc'
        ]
        return _md_render(
            text or "",
            extensions=exts,
            extension_configs={
                'codehilite': {
                    'guess_lang': False,
                    'noclasses': False
                }
            }
        )
except Exception:
    def render_md(text: str) -> str:
        """降级方案：直接返回预格式化文本"""
        return f"<pre>{(text or '').replace('<','&lt;').replace('>','&gt;')}</pre>"


def find_title_in_content(content: str, target: str = 'title') -> str | None:
    """提取 Markdown 首个标题，或返回移除首个标题后的正文。

    支持两类标题：
    - ATX: 以一个或多个 # 开头的行（例如: # Title）
    - Setext: 标题行下一行全为 '=' 或 '-'（例如: Title\n=====）

    参数:
      content: 原始 Markdown 文本
      target: 'title' 返回标题文本；'post' 返回移除首个标题后的正文

    返回:
      - 当 target='title'：返回首个标题文本，未找到则返回 None
      - 当 target='post' ：返回移除首个标题后的正文；未找到标题则返回原内容
    """
    if content is None:
        return None if target == 'title' else ''

    lines = content.splitlines()
    n = len(lines)

    def atx_title(s: str) -> str | None:
        s1 = s.strip()
        if s1.startswith('#'):
            txt = s1.lstrip('#').strip()
            # 去掉行尾可选的关闭井号序列（例如 "# Title ####"）
            txt = re.sub(r"\s#+\s*$", "", txt).strip()
            return txt or None
        return None

    def is_all(ch: str, s: str) -> bool:
        return bool(s) and all(c == ch for c in s)

    for i in range(n):
        raw = lines[i]
        # 先识别 ATX 标题
        t = atx_title(raw)
        if t:
            if target == 'title':
                return t
            # target == 'post': 删除该行
            return "\n".join(lines[:i] + lines[i+1:])

        # 再尝试识别 Setext 标题（下一行全为 '=' 或 '-'）
        if i + 1 < n:
            title_line = raw.strip()
            underline = lines[i + 1].strip()
            if title_line and (is_all('=', underline) or is_all('-', underline)):
                if target == 'title':
                    return title_line
                # target == 'post': 删除标题行与下划线行
                return "\n".join(lines[:i] + lines[i+2:])

    # 未找到任何标题
    return None if target == 'title' else content


def strip_md_title_if_matches(content: str, db_title: str) -> str:
    """若 MD 首个标题与数据库标题相同（忽略大小写与前后空白），则返回去掉该标题后的正文，否则返回原内容。"""
    raw = content or ''
    md_title = find_title_in_content(raw, target='title')
    norm = lambda s: (s or '').strip().lower()
    if norm(md_title) == norm(db_title):
        return find_title_in_content(raw, target='post') or ''
    return raw
