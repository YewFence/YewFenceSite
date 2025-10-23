// Management page script: No HTML/CSS injected; all structure lives in management.html
(function(){

  // 触发浏览器下载（本地生成文件）
  // name: 文件名，content: 文本内容
  function downloadFile(name, content) {
    const blob = new Blob([content], { type: 'text/markdown;charset=utf-8' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url; a.download = name; a.click();
    URL.revokeObjectURL(url);
  }


  // 向后端请求导出当前数据库中的 blogs.json 并触发下载
  async function downloadBlogsFromServer() {
    const res = await fetch('/api/posts/export_json');
    if (!res.ok) throw new Error('导出失败');
    const blob = await res.blob();
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url; a.download = 'blogs.json'; a.click();
    URL.revokeObjectURL(url);
  }

  function bindRow(row) {
    // 辅助：获取行的数字 ID（兼容不同结构）
    const getRowId = () => {
      const v = row.querySelector('.v-id')?.textContent?.trim();
      if (v && /^\d+$/.test(v)) return v;
      const t = row.querySelector('.future')?.textContent || '';
      if (t && /^\d+$/.test(t)) return t;
      return null;
    };

    // 下载 MD：请求后端接口，后端会以文章标题作为文件名返回 Markdown
    row.querySelector('[data-act="download-md"]')?.addEventListener('click', async () => {
      try {
        const id = getRowId();
        if (!id) { alert('无法获取文章 ID'); return; }
        // 直接跳转下载，由后端设置 Content-Disposition 为 “标题.md”
        const a = document.createElement('a');
        a.href = `/api/posts/${id}/md`;
        document.body.appendChild(a);
        a.click();
        a.remove();
      } catch(err) { alert('下载失败：' + err.message); }
    });

    // 上传 MD：将文件内容 POST 到后端，写入数据库的 post.content
    row.querySelector('[data-act="upload-md"]')?.addEventListener('change', async (e) => {
      const id = getRowId();
      if (!id) { alert('无法获取文章 ID'); e.target.value = ''; return; }
      const file = e.target.files?.[0];
      if (!file) return;
      const text = await file.text();
      if (!window.confirm('将用所选 Markdown 覆盖数据库中的文章内容，是否继续？')) { e.target.value = ''; return; }
      try {
        const res = await fetch(`/api/posts/${id}/md`, {
          method: 'POST',
          headers: { 'Content-Type': 'text/markdown; charset=utf-8' },
          body: text
        });
        if (!res.ok) throw new Error('上传失败 ' + res.status);
        alert('已更新数据库中的 Markdown 内容');
      } catch (err) {
        alert('更新失败：' + (err?.message || err));
      } finally {
        e.target.value = '';
      }
    });
  }

  // 编辑弹窗逻辑：使用原生表单提交（POST），无需批量更新
  function bindEditModal() {
    // 获取各个元素
    const mask = document.getElementById('editModal');
    const form = document.getElementById('editForm');
    if (!mask || !form) return;
    const fTitle = document.getElementById('fTitle');
    const fAuthor = document.getElementById('fAuthor');
    const fDate = document.getElementById('fDate');
    const fSummary = document.getElementById('fSummary');
    const fNote = document.getElementById('fNote');
    const fStatus = document.getElementById('fStatus');
    const fMdFile = document.getElementById('fMdFile');
    const fContent = document.getElementById('fContent');
    let currentRow = null;

    // 定义开关窗口的方法
    const open = (row) => { currentRow = row; mask.setAttribute('aria-hidden','false'); };
    const close = () => { mask.setAttribute('aria-hidden','true'); currentRow = null; };

    // 即时校验（简化）：标题非空，日期为空或 YYYY-MM-DD
    function validateField(fieldEl, checkFn) {
      const label = fieldEl.closest('.field');
      if (!label) return true;
      const ok = checkFn(fieldEl.value);
      label.classList.toggle('invalid', !ok);
      return ok;
    }
    const isNonEmpty = v => (v ?? '').trim().length > 0;
    const isDate = v => (!v) || /^\d{4}-\d{2}-\d{2}$/.test(v);
    fTitle?.addEventListener('input', ()=> validateField(fTitle, isNonEmpty));
    fDate?.addEventListener('input', ()=> validateField(fDate, isDate));

    // 打开编辑弹窗：填充表单并设置 action
    document.getElementById('mgmtRoot')?.addEventListener('click', (e)=>{
      // e是点击事件，绑定在大元素上，确认其点击了哪一个编辑按钮
      const btn = e.target.closest('[data-act="edit-row"]');
      if (!btn) return;
      // 直接在前端页面获取对应信息
      const row = e.target.closest('.blog-row');
      if (!row) return;
      // 填充值
      fTitle.value = row.querySelector('.v-title')?.textContent || '';
      fAuthor.value = row.querySelector('.v-author')?.textContent || '';
      fDate.value = row.querySelector('.v-date')?.textContent || '';
      fSummary.value = row.querySelector('.v-summary')?.textContent || '';
      fNote.value = row.querySelector('.v-note')?.textContent || '';
      fStatus.value = row.querySelector('.v-status')?.textContent || 'hidden';
      // 根据当前值更新选择框风格
      reflectStatusStyle();
      // 清错误态
      form.querySelectorAll('.field').forEach(n=> n.classList.remove('invalid'));
      // 设置表单 action
      const id = row.querySelector('.future')?.textContent || '';
      form.action = `/management/posts/${id}/edit`;
      form.method = 'post';
      if (fContent) fContent.value = '';
      open(row);
    });

    // 打开新建弹窗
    const btnAdd = document.getElementById('btnAddNewPost');
    btnAdd.addEventListener('click', () => {
      const mask = document.getElementById('editModal');
      const form = document.getElementById('editForm');
      if (!mask || !form) return;
      // 清空表单并设为新建模式
      form.reset();
      form.action = '/management/posts/new';
      form.method = 'post';
      // 一些默认值
      const fDate = document.getElementById('fDate');
      if (fDate && !fDate.value) fDate.value = new Date().toISOString().slice(0,10);
      // 清错误态
      form.querySelectorAll('.field').forEach(n=> n.classList.remove('invalid'));
      // 打开弹窗
      document.getElementById('fContent')?.setAttribute('value', '');
      mask.setAttribute('aria-hidden','false');
    });

    // 关闭：点击遮罩或取消或 Esc
    mask.addEventListener('click', (e)=>{
      if (e.target === mask || 
          e.target.matches('[data-edit="close"], [data-edit="cancel"], [data-edit="upload"]')) {
        close();
      }
    });
    document.addEventListener('keydown', (e)=>{ if (mask.getAttribute('aria-hidden')==='false' && e.key==='Escape') {
        close();
      }
    });

    // 表单提交前校验；若无效则阻止提交
    form.addEventListener('submit', (e)=>{
      const okDate = validateField(fDate, isDate);
      if (!okDate) {
        e.preventDefault();
        return false;
      }
      // 允许原生提交，提交后由服务器重定向回管理页
      return true;
    });

    // 选择 Markdown 文件时，读入文本写入隐藏 content 字段
    fMdFile?.addEventListener('change', async (e) => {
      const file = e.target.files?.[0];
      if (file) console.log('read file successfully');
      if (!file) { if (fContent) fContent.value = ''; return; }
      try {
        const txt = await file.text();
        console.log('读取到的 MD 内容：', txt);
        if (fContent) fContent.value = txt;
      } catch {
        if (fContent) fContent.value = '';
      }
    });

    // 状态选择风格切换
    function reflectStatusStyle() {
      if (!fStatus) return;
      const val = (fStatus.value || '').toLowerCase();
      fStatus.classList.toggle('is-published', val === 'published');
      fStatus.classList.toggle('is-hidden', val !== 'published');
    }
    fStatus?.addEventListener('change', reflectStatusStyle);
  }

  function initScrollToHash() {
    // 1. 检查当前 URL 是否包含锚点 (hash)
    if (window.location.hash) {
        
        // 2. 使用 setTimeout 将任务推迟到下一个事件循环
        // 为什么? 我们需要给浏览器“足够的时间”来先完成“滚动到锚点”这个默认动作。
        // 如果不延迟，JS 运行太快，URL 瞬间被清理，浏览器就不知道该往哪滚了。
        setTimeout(() => {
            
            // 3. 【关键】修改 URL，去掉锚点
            // history.replaceState(stateObj, title, newUrl)
            // - 它会替换当前的历史记录，所以按“返回”不会回到带锚点的 URL。
            // - window.location.pathname 是 /index
            // - window.location.search 是 ?query=... (如果有的话)
            history.replaceState(
                null, 
                document.title, 
                window.location.pathname + window.location.search
            );

        }, 3000); // 3000 毫秒的延迟通常就足够了
      }
    }

  function init() {
    document.querySelectorAll('.blog-row').forEach(bindRow);
    bindEditModal();
    initScrollToHash();
  }

  document.addEventListener('DOMContentLoaded', init);
})();
