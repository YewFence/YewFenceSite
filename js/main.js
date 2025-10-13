/* Main interaction script for MySite */
// 站点主要交互脚本（自执行函数，避免全局变量污染）
(function () {
  const root = document.documentElement;
  const navToggle = document.getElementById('navToggle');
  const navMenu = document.getElementById('navMenu');
  const themeBtn = document.getElementById('themeSwitcher');
  const backToTop = document.getElementById('backToTop');
  const yearSpan = document.getElementById('year');
  const contactForm = document.getElementById('contactForm');
  const formStatus = document.getElementById('formStatus');
  const siteHeader = document.querySelector('.site-header');
  const hero = document.querySelector('.hero');

  // 设置当前年份（页脚版权）
  if (yearSpan) yearSpan.textContent = new Date().getFullYear();

  // ============== 主题切换（深/浅色） ==============
  // c查询localStorage中有没有主题存储
  const THEME_KEY = 'mysite-theme';
  const savedTheme = localStorage.getItem(THEME_KEY);
  if (savedTheme) root.setAttribute('data-theme', savedTheme);

  //主要功能函数
  function toggleTheme() {
    const next = root.getAttribute('data-theme') === 'dark' ? 'light' : 'dark';
    // // 添加过渡类以触发展示动画
    root.classList.add('theme-transition');
    // 切换主题属性
    root.setAttribute('data-theme', next);
    localStorage.setItem(THEME_KEY, next);
    if (themeBtn) themeBtn.textContent = next === 'dark' ? '☀️' : '🌙';
    // 在动画结束后移除（与 CSS 中最长 .65s 对齐，稍加余量）
    clearTimeout(window.__themeTransitionTimer);
    window.__themeTransitionTimer = setTimeout(() => {
      root.classList.remove('theme-transition');
    }, 700);
  }
  //主要程序
  if (themeBtn) {
    themeBtn.addEventListener('click', toggleTheme);
    // 初始化按钮图标（根据当前主题）
    const current = root.getAttribute('data-theme');
    themeBtn.textContent = current === 'dark' ? '☀️' : '🌙';
  }

  // ============== 返回顶部按钮显示/隐藏逻辑 ==============
  const showAt = 480; // 滚动超过该像素显示按钮
  function onScroll() {
    if (!backToTop) return;
    if (window.scrollY > showAt) {
      backToTop.hidden = false;
      backToTop.style.opacity = '1';
    } else {
      backToTop.style.opacity = '0';
      setTimeout(() => { if (window.scrollY <= showAt) backToTop.hidden = true; }, 250);
    }
  }
  window.addEventListener('scroll', onScroll, { passive: true });
  if (backToTop) backToTop.addEventListener('click', () => window.scrollTo({ top: 0, behavior: 'smooth' }));

  // ===============复制按钮代码================
  // 复制按钮功能
  const copyTexts = document.querySelectorAll('.text-to-copy');
  const copyButtons = document.querySelectorAll('.copy-btn');
  //提示文本框
  const promptDiv = document.getElementById('prompt-message');
  const showPrompt = (index) => {
    if (promptDiv) {
      const promptDivP = promptDiv.firstElementChild;
      // 从父元素 article 的 data-copy-text 属性中获取要复制的文本
      const textToCopy = copyTexts[index].textContent;

      // 使用 Clipboard API 进行复制
      navigator.clipboard.writeText(textToCopy).then(() => {
        // --- 成功 ---
        console.log('文本已复制');
        // 显示提示信息
        promptDivP.textContent = '已复制到剪贴板';
        promptDiv.classList.add('is-visible');
        // 2秒后隐藏提示信息
        setTimeout(() => {
          promptDivP.textContent = '点击以复制';
        }, 2000);
      });
    }
  }
  if (copyButtons && promptDiv) {
    const promptDivP = promptDiv.firstElementChild;
    copyButtons.forEach((copyButton, index) => {
      try {
        copyButton.addEventListener('click', () => showPrompt(index));
      } catch (err) {
        // --- 失败 ---
        console.error('复制失败: ', err);
          promptDivP.textContent = '复制失败，请手动复制';
          promptDiv.classList.add('is-visible');
          setTimeout(() => {
            promptDivP.textContent = '点击以复制';
          }, 2000);
      }
    });
  }

  //复制按钮提示信息触发器
  // 1. 选中目标元素
  const targetElement = document.getElementById('prompt-message');

  if (targetElement) {
    // 2. 监听“鼠标进入”触发器事件
    copyButtons.forEach((copyButton) => {
      copyButton.addEventListener('mouseenter', () => {
        // 当鼠标进入时，给目标元素添加 .is-visible 类
        targetElement.classList.add('is-visible');
      });

      // 3. 监听“鼠标离开”触发器事件
      copyButton.addEventListener('mouseleave', () => {
        // 当鼠标离开时，从目标元素移除 .is-visible 类
        targetElement.classList.remove('is-visible');
      });
    });
  }
})();