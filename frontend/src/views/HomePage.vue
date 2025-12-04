<template>
  <DefaultLayout>
    <!-- section分隔网页滚动的吸附点 -->
    <section class="hero scroller" id="hero">
      <div class="container hero-inner">
        <h1 id="main-title">{{ content.hero.greeting }} <span class="accent" @click="handleSecretClick">{{ content.hero.name }}</span></h1>
        <p class="subtitle">{{ content.hero.subtitle }}</p>
        <div class="hero-actions">
        </div>
      </div>
      <div class="scroll-indicator" aria-hidden="true">{{ content.hero.scrollIndicator }}</div>
    </section>

    <section class="section scroller about-preview" id="about">
      <div class="container">
        <h2 class="section-title">{{ content.about.title }}</h2>
        <p v-html="content.about.intro"></p>
        <ul class="tag-list">
          <li v-for="tag in content.about.tags" :key="tag">{{ tag }}</li>
        </ul>
      </div>
    </section>

    <section class="section scroller projects-preview" id="projects">
      <div class="container">
        <h2 class="section-title">{{ content.projects.title }}</h2>
        <div class="grid projects-grid">
          <article v-for="card in content.projects.cards" :key="card.title" class="card">
            <h3>{{ card.title }}</h3>
            <p v-html="card.description"></p>
            <RouterLink class="card-link" :to="card.link"></RouterLink>
          </article>
        </div>
        <div class="center mt">
          <RouterLink :to="content.projects.buttonLink" class="btn small">{{ content.projects.buttonText }}</RouterLink>
        </div>
      </div>
    </section>

    <section class="section scroller contact-cta" id="contact">
      <div class="container narrow">
        <h2 class="section-title">{{ content.contact.title }}</h2>
        <p>{{ content.contact.description }}</p>
        <RouterLink :to="content.contact.buttonLink" class="btn primary">{{ content.contact.buttonText }}</RouterLink>
      </div>
    </section>
  </DefaultLayout>
</template>

<script setup>
import { useHead } from '@vueuse/head'
import { useRouter, RouterLink } from 'vue-router'
import DefaultLayout from '../components/DefaultLayout.vue'
import { pages } from '@/utils/content'

const content = pages.home
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

useHead ({
  title: content.meta.title,
  meta: [
    { name: 'description', content: content.meta.description },
    { name: 'author', content: content.meta.author }
  ]
})

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
#main-title {
  text-shadow: 3px 3px 6px rgba(0, 0, 0, 0.8),
               0 0 30px rgba(0, 0, 0, 0.5),
               0 0 40px rgba(0, 0, 0, 0.3);
  user-select: none;
  -webkit-user-select: none;
  -moz-user-select: none;
  -ms-user-select: none;
}

#main-title .accent {
  user-select: none;
  -webkit-user-select: none;
  -moz-user-select: none;
  -ms-user-select: none;
}
</style>
