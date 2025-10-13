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

  // ==== 确认对话框（Promise 版） ====
  function injectConfirmStylesOnce() {
    if (document.getElementById('confirmStyles')) return;
    const style = document.createElement('style');
    style.id = 'confirmStyles';
    style.textContent = `
    .modal-mask { position: fixed; inset: 0; background: rgba(0,0,0,.35); display:flex; align-items:center; justify-content:center; z-index: 2000; }
    .modal-card { width: min(420px, 92vw); background: var(--color-bg); border:1px solid var(--color-border); border-radius: var(--radius-md); box-shadow: var(--shadow-md); }
    .modal-head { padding: .9rem 1rem; border-bottom: 1px solid var(--color-border); font-weight: 600; }
    .modal-body { padding: 1rem; color: var(--color-text); }
    .modal-foot { padding: .75rem 1rem; border-top: 1px solid var(--color-border); display:flex; gap:.5rem; justify-content:flex-end; }
    .modal-danger { color: var(--color-danger); }
    `;
    document.head.appendChild(style);
  }

  function showConfirm({ title = '确认操作', message = '是否继续？', danger = false, okText = '确定', cancelText = '取消' } = {}) {
    injectConfirmStylesOnce();
    return new Promise((resolve) => {
      const node = el(`
        <div class="modal-mask" role="dialog" aria-modal="true">
          <div class="modal-card" role="document">
            <div class="modal-head ${danger ? 'modal-danger' : ''}">${title}</div>
            <div class="modal-body">${message}</div>
            <div class="modal-foot">
              <button class="btn" data-act="cancel">${cancelText}</button>
              <button class="btn primary" data-act="ok">${okText}</button>
            </div>
          </div>
        </div>
      `);
      document.body.appendChild(node);
      const cleanup = () => node.remove();
      node.querySelector('[data-act="cancel"]').addEventListener('click', () => { cleanup(); resolve(false); });
      node.querySelector('[data-act="ok"]').addEventListener('click', () => { cleanup(); resolve(true); });
      const onKey = (e) => { if (e.key === 'Escape') { document.removeEventListener('keydown', onKey); cleanup(); resolve(false);} };
      document.addEventListener('keydown', onKey);
    });
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
          <h3 style="margin:0; display:flex; align-items:center; gap:.5rem;">
            <span>${blog.title}</span>
            <span class="future" style="font-size:.8rem; border:1px solid var(--color-border); padding:.1rem .4rem; border-radius:6px;">${(blog.status||'published')==='published'?'已发布':'草稿'}</span>
          </h3>
          <div class="future">ID: ${blog.id}</div>
        </div>
        <div class="grid" style="grid-template-columns: repeat(auto-fit,minmax(180px,1fr)); gap:.6rem;">
          <label>标题<input class="in-title" type="text" value="${blog.title}"></label>
          <label>作者<input class="in-author" type="text" value="${blog.author}"></label>
          <label>日期<input class="in-date" type="date" value="${fmtDateInput(blog.date)}"></label>
          <label>摘要<input class="in-summary" type="text" value="${blog.summary ?? ''}"></label>
          <label>MD 文件名<input class="in-md" type="text" value="${blog.md_file}"></label>
          <label>状态
            <select class="in-status">
              <option value="published" ${((blog.status||'published')==='published')?'selected':''}>已发布</option>
              <option value="draft" ${((blog.status||'published')==='draft')?'selected':''}>草稿</option>
            </select>
          </label>
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
      const ok = await showConfirm({ title: '替换 MD', message: '将用所选文件内容替换 ' + blog.md_file + '，并生成下载，请手动更新 posts 文件。继续？', okText:'替换' });
      if (!ok) { e.target.value = ''; return; }
      const text = await file.text();
      downloadFile(blog.md_file, text);
      alert('已生成下载，请替换 posts/' + blog.md_file + ' 文件');
    });

    node.querySelector('[data-act="save-row"]').addEventListener('click', async () => {
      const ok = await showConfirm({ title:'更新条目', message:'保存当前行的更改到列表（内存），仍需“保存全部更改”来导出 blogs.json。是否继续？', okText:'更新' });
      if (!ok) return;
      blog.title = node.querySelector('.in-title').value.trim();
      blog.author = node.querySelector('.in-author').value.trim();
      blog.date = node.querySelector('.in-date').value;
      blog.summary = node.querySelector('.in-summary').value.trim();
      blog.md_file = node.querySelector('.in-md').value.trim();
      blog.status = node.querySelector('.in-status').value;
      node.querySelector('h3 span:first-child').textContent = blog.title || '(未命名)';
      node.querySelector('h3 .future').textContent = (blog.status==='published')?'已发布':'草稿';
      alert('已更新到内存列表，记得点“保存全部更改”导出 blogs.json');
    });

    node.querySelector('[data-act="remove"]').addEventListener('click', async () => {
      const ok = await showConfirm({ title:'移除博客', message:`确定从列表中移除《${blog.title}》？此操作只影响内存，仍需保存全部更改以导出。`, okText:'移除', danger:true });
      if (!ok) return;
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
      const item = { id, title: '新文章', author: 'YewFence', date: now, summary: '', md_file: 'new.md', status: 'draft' };
      list.unshift(item);
      redraw();
    });

    // Save all -> download blogs.json
    panel.querySelector('#btnSaveAll').addEventListener('click', async () => {
      const ok = await showConfirm({ title:'导出 blogs.json', message:'将导出当前列表为 blogs.json 文件，请手动替换 data/blogs.json。是否继续？', okText:'导出' });
      if (!ok) return;
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
