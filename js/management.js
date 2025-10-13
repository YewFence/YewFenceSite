/* Front-end only blog management (no backend). */
(function(){
  const BLOGS_JSON_PATH = 'data/blogs.json';
  const POSTS_DIR = 'posts';

  // Utility: fetch JSON
  async function loadBlogs() {
    const res = await fetch(BLOGS_JSON_PATH + '?_=' + Date.now());
    if (!res.ok) throw new Error('无法加载 blogs.json');
    return res.json();
  }

  async function saveBlogs(blogs) {
    // No backend: provide a client-side download of updated blogs.json
    const blob = new Blob([JSON.stringify(blogs, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'blogs.json';
    document.body.appendChild(a);
    a.click();
    a.remove();
    URL.revokeObjectURL(url);
  }

  function downloadFile(name, content) {
    const blob = new Blob([content], { type: 'text/markdown;charset=utf-8' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url; a.download = name; a.click();
    URL.revokeObjectURL(url);
  }

  async function fetchMarkdown(mdFile) {
    const res = await fetch(POSTS_DIR + '/' + mdFile + '?_=' + Date.now());
    if (!res.ok) throw new Error('无法加载 ' + mdFile);
    return res.text();
  }

  // UI helpers
  function el(html) {
    const tpl = document.createElement('template');
    tpl.innerHTML = html.trim();
    return tpl.content.firstElementChild;
  }

  function fmtDateInput(val) {
    // Ensure value fits yyyy-mm-dd
    if (!val) return '';
    return val.slice(0,10);
  }

  // ==== Password panel ====
  function mountPasswordPanel(container) {
    const node = el(`
      <section class="large-card" aria-label="密码管理">
        <h2>密码管理</h2>
        <div class="grid" style="grid-template-columns: 1fr; gap: .75rem;">
          <label class="future">修改密码（仅本地存储，用于演示）</label>
          <input id="oldPw" type="password" placeholder="旧密码" />
          <input id="newPw" type="password" placeholder="新密码（至少 6 位）" />
          <div style="display:flex; gap:.5rem;">
            <button id="btnChangePw" class="btn primary">修改密码</button>
          </div>
          <div id="pwTip" class="future"></div>
        </div>
      </section>
    `);
    container.appendChild(node);
    const oldPw = node.querySelector('#oldPw');
    const newPw = node.querySelector('#newPw');
    const btn = node.querySelector('#btnChangePw');
    const tip = node.querySelector('#pwTip');
    btn.addEventListener('click', async () => {
      const o = oldPw.value.trim();
      const n = newPw.value.trim();
      if (n.length < 6) { tip.textContent = '新密码至少 6 位'; return; }
      const ok = await Auth.changePassword(o, n);
      tip.textContent = ok ? '已修改，请使用新密码重新登录下次会话' : '旧密码错误';
    });
  }

  // ==== Blog editor row ====
  function blogRow(blog) {
    const node = el(`
      <article class="card">
        <div style="display:flex; justify-content:space-between; align-items:center; gap:.75rem;">
          <h3 style="margin:0;">${blog.title}</h3>
          <div class="future">ID: ${blog.id}</div>
        </div>
        <div class="grid" style="grid-template-columns: repeat(auto-fit,minmax(180px,1fr)); gap:.6rem;">
          <label>标题<input class="in-title" type="text" value="${blog.title}"></label>
          <label>作者<input class="in-author" type="text" value="${blog.author}"></label>
          <label>日期<input class="in-date" type="date" value="${fmtDateInput(blog.date)}"></label>
          <label>摘要<input class="in-summary" type="text" value="${blog.summary ?? ''}"></label>
          <label>MD 文件名<input class="in-md" type="text" value="${blog.md_file}"></label>
        </div>
        <div style="display:flex; gap:.5rem; flex-wrap:wrap; margin-top:.5rem;">
          <button class="btn" data-act="preview">预览 MD</button>
          <button class="btn" data-act="download-md">下载 MD</button>
          <label class="btn">
            重新上传 MD
            <input type="file" accept=".md" style="display:none" data-act="upload-md" />
          </label>
          <button class="btn primary" data-act="save-row">更新到列表</button>
          <button class="btn" data-act="remove">从列表移除</button>
        </div>
      </article>
    `);

    // wire events
    node.querySelector('[data-act="preview"]').addEventListener('click', async () => {
      try {
        const text = await fetchMarkdown(blog.md_file);
        const w = window.open('', '_blank');
        w.document.write('<pre>' + (text.replace(/[&<>]/g, s => ({'&':'&amp;','<':'&lt;','>':'&gt;'}[s]))) + '</pre>');
        w.document.close();
      } catch(err) { alert('预览失败：' + err.message); }
    });

    node.querySelector('[data-act="download-md"]').addEventListener('click', async () => {
      try { const text = await fetchMarkdown(blog.md_file); downloadFile(blog.md_file, text); }
      catch(err) { alert('下载失败：' + err.message); }
    });

    node.querySelector('[data-act="upload-md"]').addEventListener('change', async (e) => {
      const file = e.target.files[0]; if (!file) return;
      const text = await file.text();
      // 提供一个带新内容的本地下载，开发者可手动替换 posts 目录中的文件
      downloadFile(blog.md_file, text);
      alert('已生成下载，请替换 posts/' + blog.md_file + ' 文件');
    });

    node.querySelector('[data-act="save-row"]').addEventListener('click', () => {
      blog.title = node.querySelector('.in-title').value.trim();
      blog.author = node.querySelector('.in-author').value.trim();
      blog.date = node.querySelector('.in-date').value;
      blog.summary = node.querySelector('.in-summary').value.trim();
      blog.md_file = node.querySelector('.in-md').value.trim();
      node.querySelector('h3').textContent = blog.title || '(未命名)';
      alert('已更新到内存列表，记得点“保存全部更改”导出 blogs.json');
    });

    node.querySelector('[data-act="remove"]').addEventListener('click', () => {
      node.dispatchEvent(new CustomEvent('remove-blog', { bubbles: true, detail: { id: blog.id } }));
    });

    return node;
  }

  // ==== Management main ====
  async function init() {
    if (!Auth.isAuthenticated()) { window.location.replace('login.html'); return; }

    const wrap = document.getElementById('mgmtRoot');
    if (!wrap) return;

    // Password panel
    mountPasswordPanel(wrap);

    // Blog list panel
    const blogs = await loadBlogs();
    let list = Array.isArray(blogs) ? blogs.slice() : [];

    const panel = el(`
      <section class="large-card" aria-label="博客管理">
        <div class="title-wrapper">
          <h2 id="blogPanelTitle">博客管理</h2>
        </div>
        <div style="display:flex; gap:.5rem; flex-wrap:wrap; margin-bottom:.5rem;">
          <button class="btn primary" id="btnAdd">新增博客</button>
          <button class="btn" id="btnSaveAll">保存全部更改（导出 blogs.json）</button>
          <button class="btn" id="btnExportMd">打包导出全部 MD（Zip）</button>
        </div>
        <div id="blogList" class="grid"></div>
      </section>
    `);
    wrap.appendChild(panel);

    const listEl = panel.querySelector('#blogList');

    function redraw() {
      listEl.innerHTML = '';
      list.forEach(item => {
        const row = blogRow(item);
        row.addEventListener('remove-blog', (e) => {
          const id = e.detail.id;
          list = list.filter(b => b.id !== id);
          redraw();
        });
        listEl.appendChild(row);
      });
    }
    redraw();

    // Add new blog
    panel.querySelector('#btnAdd').addEventListener('click', () => {
      const id = 'id_' + Math.random().toString(36).slice(2, 8);
      const now = new Date().toISOString();
      const item = { id, title: '新文章', author: 'YewFence', date: now, summary: '', md_file: 'new.md' };
      list.unshift(item);
      redraw();
    });

    // Save all -> download blogs.json
    panel.querySelector('#btnSaveAll').addEventListener('click', async () => {
      await saveBlogs(list);
      alert('已导出 blogs.json，请手动替换 data/blogs.json');
    });

    // Export all MD as Zip (optional, fallback: individual)
    panel.querySelector('#btnExportMd').addEventListener('click', async () => {
      try {
        if (!window.JSZip) throw new Error('JSZip 未加载');
        const zip = new JSZip();
        for (const b of list) {
          try { const txt = await fetchMarkdown(b.md_file); zip.file(b.md_file, txt); }
          catch { /* ignore missing */ }
        }
        const blob = await zip.generateAsync({ type: 'blob' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a'); a.href = url; a.download = 'posts.zip'; a.click();
        URL.revokeObjectURL(url);
      } catch (err) {
        alert('打包失败：' + err.message + '，你可以逐个下载 MD');
      }
    });
  }

  // start
  document.addEventListener('DOMContentLoaded', init);
})();
