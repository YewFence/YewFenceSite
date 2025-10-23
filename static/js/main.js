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
  const heroInner = document.querySelector('.hero .hero-inner');

  // 设置当前年份（页脚版权）
  if (yearSpan) yearSpan.textContent = new Date().getFullYear();

  // ============== 移动端导航开合 ==============
  if (navToggle && navMenu) {
    navToggle.addEventListener('click', () => {
      const open = navMenu.classList.toggle('open');
      navToggle.setAttribute('aria-expanded', String(open));
    });
    // 点击导航区域外时关闭（仅在菜单已展开时）
    document.addEventListener('click', (e) => {
      if (!navMenu.contains(e.target) && e.target !== navToggle && navMenu.classList.contains('open')) {
        navMenu.classList.remove('open');
        navToggle.setAttribute('aria-expanded', 'false');
      }
    });
  }

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

  // ============== 可访问性：Esc 关闭菜单（简化版焦点管理） ==============
  if (navMenu && navToggle) {
    navMenu.addEventListener('keydown', (e) => {
      if (e.key === 'Escape' && navMenu.classList.contains('open')) {
        navMenu.classList.remove('open');
        navToggle.setAttribute('aria-expanded', 'false');
        navToggle.focus();
      }
    });
  }
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
/* 太困难了，多平台适配如同地狱，我还是选择css吧
  //============== 全屏切片滚动控制 =================
  // 1. 获取所有的全屏切片
  const scrollers = document.querySelectorAll('.scroller');
  const totalScrollers = scrollers.length;

  // 2. 初始化当前切片的索引和滚动状态
  let currentScrollerIndex = 0;
  let isScrolling = false; // 用于控制“冷却时间”的标志

  // 3. 监听鼠标滚轮事件
  // 'wheel' 事件会在鼠标滚轮滚动时触发
  if (scrollers) {
    function scrollToCurrentSection(Index) {
      // 设置正在滚动标志，防止连续触发
      isScrolling = true;

      // 使用 scrollIntoView 平滑滚动到当前索引对应的切片
      console.log(scrollers[Index]);
      scrollers[Index].scrollIntoView({
        behavior: 'smooth'
      });

      // 设置一个“冷却时间”，时长约等于滚动动画的时间。
      // 在这段时间内，所有新的滚动事件都会被忽略。
      setTimeout(() => {
        isScrolling = false;
      }, 700); // 700毫秒 = 0.7秒
    }

    function handleScrollEvent(event) {
      // 如果正在滚动中，则忽略本次事件，直接返回
      event.preventDefault(); // 阻止默认滚动行为
      if (isScrolling) {
        console.log('正在滚动，忽略本次事件');
        return;
      }
      const isLastScroller = currentScrollerIndex === totalScrollers - 1;
      const isScrollingDown = event.deltaY > 0;

      if (currentScrollerIndex === totalScrollers && !isScrollingDown) {
        // 如果在最底部，并且用户向上滚动
        console.log('最底部时向上滚动');
        currentScrollerIndex = totalScrollers - 1;
        scrollToCurrentSection(currentScrollerIndex);
        return;
      }
      if (currentScrollerIndex === totalScrollers && isScrollingDown) {
        // 如果在最底部，并且用户继续向下滚动，忽略事件
        console.log('最底部时继续向下滚动，忽略事件');
        return;
      }
      if (isLastScroller && isScrollingDown) {
        // 如果已经在最后一个切片，并且用户继续向下滚动，直接滚动至页面底部
        window.scrollTo({ top: document.body.scrollHeight, behavior: 'smooth' });
        console.log('已经在最后一个切片，直接滚动至最低端');
        currentScrollerIndex = totalScrollers; // 标记为超过最后一个切片
        return;
      }
      //不在最下面，也不在最后一个画面且向下滚动，正常逻辑
      // event.deltaY > 0 表示向下滚动
      // event.deltaY < 0 表示向上滚动
      if (isScrollingDown) {
        // 向下滚动
        console.log('向下滚动');
        console.log(currentScrollerIndex);
        if (!isLastScroller) {
          currentScrollerIndex++;
          scrollToCurrentSection(currentScrollerIndex);
          return;
        }
      } else {
        // 向上滚动
        console.log('向上滚动');
        console.log(currentScrollerIndex);
        if (currentScrollerIndex > 0) {
          currentScrollerIndex--;
          scrollToCurrentSection(currentScrollerIndex);
          return;
        }
        
      }
    }
    //增加核心侦测器
    window.addEventListener('wheel', handleScrollEvent, { passive: false });
  }
*/
})();

// ================= 隐藏入口：快速点击 YewFence 五次跳转登录 =================
(function () {
  // 仅在首页存在 .hero-inner 时启用
  const heroInner = document.querySelector('.hero .hero-inner');
  if (!heroInner) return;
  // 目标：h1 内的 .accent（YewFence 文本）
  const target = heroInner.querySelector('h1 .accent');
  if (!target) return;

  let clickCount = 0;
  let firstClickAt = 0;
  const WINDOW_MS = 1500; // 1.5 秒内点击 5 次
  const REQUIRED = 5;

  function reset() {
    clickCount = 0;
    firstClickAt = 0;
  }

  target.addEventListener('click', () => {
    const now = Date.now();
    if (firstClickAt === 0 || now - firstClickAt > WINDOW_MS) {
      // 开启新窗口
      firstClickAt = now;
      clickCount = 1;
      return;
    }
    clickCount += 1;
    if (clickCount >= REQUIRED) {
      reset();
      // 静默跳转，避免可见提示
      window.location.href = 'login';
    }
  });

  // 超时自动重置
  setInterval(() => {
    if (firstClickAt && Date.now() - firstClickAt > WINDOW_MS) reset();
  }, 300);
})();