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
            'toc',
            'pymdownx.tilde'  # 支持删除线 ~~text~~
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


def find_title_in_content(content: str) -> str | None:
    """提取 Markdown 首个标题。

    支持两类标题：
    - ATX: 以一个或多个 # 开头的行（例如: # Title）
    - Setext: 标题行下一行全为 '=' 或 '-'（例如: Title\n=====）

    参数: content: 原始 Markdown 文本

    返回: 文章标题
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
            return t

        # 再尝试识别 Setext 标题（下一行全为 '=' 或 '-'）
        if i + 1 < n:
            title_line = raw.strip()
            underline = lines[i + 1].strip()
            if title_line and (is_all('=', underline) or is_all('-', underline)):
                return title_line
    # 未找到任何标题
    return None
