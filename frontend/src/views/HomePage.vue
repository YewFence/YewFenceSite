<template>
  <DefaultLayout>
    <!-- section分隔网页滚动的吸附点 -->
    <section class="hero scroller" id="hero">
      <div class="container hero-inner">
        <h1>你好，我是 <span class="accent" @click="handleSecretClick">YewFence</span></h1>
        <p class="subtitle">一名前端初学者</p>
        <div class="hero-actions">
        </div>
      </div>
      <div class="scroll-indicator" aria-hidden="true">↓ Scroll</div>
    </section>

    <section class="section scroller about-preview" id="about">
      <div class="container">
        <h2 class="section-title">关于我</h2>
        <p>这里是YewFence，华南师范大学的2025级学生<br>
            热爱编程与游戏<br>
            爱刷b站但是不常更新<br>
            爱看github，但也不常push代码<br>
            偶尔看看番和轻小说，是个浓度不算高的二次元<br>
            超绝死宅<br>
            想要了解与计算机有关的一切<br>
            很高兴认识你</p>
        <ul class="tag-list">
          <li>编程</li>
          <li>游戏</li>
          <li>二次元</li>
        </ul>
      </div>
    </section>

    <section class="section scroller projects-preview" id="projects">
      <div class="container">
        <h2 class="section-title">个人成分</h2>
        <div class="grid projects-grid">
          <article class="card">
            <h3>游戏成分</h3>
            <p>啥都玩点，来者不拒</p>
            <RouterLink class="card-link" to="/interests#p1"></RouterLink>
          </article>
          <article class="card">
            <h3>兴趣编程</h3>
            <p>想研究一堆AI</p>
            <RouterLink class="card-link" to="/interests#p2"></RouterLink>
          </article>
          <article class="card">
            <h3>二次元</h3>
            <p>不知不觉也是看了很多番和小说了，虽然不多，但是也很多了<s>废话</s></p>
            <RouterLink class="card-link" to="/interests#p3"></RouterLink>
          </article>
        </div>
        <div class="center mt">
          <RouterLink to="/interests" class="btn small">查询成分</RouterLink>
        </div>
      </div>
    </section>

    <section class="section scroller contact-cta" id="contact">
      <div class="container narrow">
        <h2 class="section-title">个人账号</h2>
        <p>想找我聊天？欢迎联系我</p>
        <RouterLink to="/contact" class="btn primary">前往联系页面</RouterLink>
      </div>
    </section>
  </DefaultLayout>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter, RouterLink } from 'vue-router'
import DefaultLayout from '../components/DefaultLayout.vue'

const router = useRouter()

// 隐藏入口：快速点击 YewFence 五次跳转登录
let clickCount = 0
let firstClickAt = 0
const WINDOW_MS = 1500 // 1.5 秒内点击 5 次
const REQUIRED = 5

const handleSecretClick = () => {
  const now = Date.now()
  if (firstClickAt === 0 || now - firstClickAt > WINDOW_MS) {
    // 开启新窗口
    firstClickAt = now
    clickCount = 1
    return
  }
  clickCount += 1
  if (clickCount >= REQUIRED) {
    clickCount = 0
    firstClickAt = 0
    // 静默跳转
    router.push('/login')
  }
}

// 超时自动重置
setInterval(() => {
  if (firstClickAt && Date.now() - firstClickAt > WINDOW_MS) {
    clickCount = 0
    firstClickAt = 0
  }
}, 300)
</script>

<style scoped>
/* 页面样式已在全局CSS中定义 */
</style>
