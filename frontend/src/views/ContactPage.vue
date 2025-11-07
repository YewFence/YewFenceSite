<template>
  <DefaultLayout>
    <section class="page-hero mini">
      <div class="container">
        <h1>联系我</h1>
        <p class="subtitle">欢迎交流 · 闲聊 · 学习</p>
      </div>
    </section>
    <section class="section">
      <div class="container">
        <div class="title-wrapper">
          <h2 class="section-title" id="contact-title">联系渠道</h2>
          <!-- 提示信息仅在需要时显示 -->
          <div id="prompt-message" :class="{ 'is-visible': promptVisible }">
            <p>{{ promptText }}</p>
          </div>
        </div>
        <div class="grid projects-grid">
          <article class="card">
            <h3>Email</h3>
            <p class="text-to-copy">cloudmapleaf@outlook.com</p>
            <button
              class="copy-btn"
              aria-label="copy my email"
              @click="copyText('cloudmapleaf@outlook.com', 0)"
              @mouseenter="showPrompt"
              @mouseleave="hidePrompt"
            ></button>
          </article>
          <article class="card">
            <h3>GitHub</h3>
            <p class="text-to-copy">https://github.com/YewFence</p>
            <button
              class="copy-btn"
              aria-label="copy my github page"
              @click="copyText('https://github.com/YewFence', 1)"
              @mouseenter="showPrompt"
              @mouseleave="hidePrompt"
            ></button>
          </article>
          <article class="card">
            <h3>Blog</h3>
            <p class="text-to-copy">https://yewyard.cn/blog</p>
            <button
              class="copy-btn"
              aria-label="copy my blog"
              @click="copyText('https://yewyard.cn/blog', 2)"
              @mouseenter="showPrompt"
              @mouseleave="hidePrompt"
            ></button>
          </article>
        </div>
      </div>
    </section>
  </DefaultLayout>
</template>

<script setup>
import { ref } from 'vue'
import { useHead } from '@vueuse/head'
import DefaultLayout from '../components/DefaultLayout.vue'

const promptVisible = ref(false)
const promptText = ref('点击以复制')

const showPrompt = () => {
  promptVisible.value = true
}

const hidePrompt = () => {
  if (promptText.value === '点击以复制') {
    promptVisible.value = false
  }
}

const copyText = async (text, index) => {
  try {
    await navigator.clipboard.writeText(text)
    promptText.value = '已复制到剪贴板'
    promptVisible.value = true
    setTimeout(() => {
      promptText.value = '点击以复制'
      promptVisible.value = false
    }, 2000)
  } catch (err) {
    console.error('复制失败: ', err)
    promptText.value = '复制失败，请手动复制'
    promptVisible.value = true
    setTimeout(() => {
      promptText.value = '点击以复制'
      promptVisible.value = false
    }, 2000)
  }
}

// 设置页面标题和描述
useHead({
  title: '联系我 - YewFenceSite',
  meta: [
    { name: 'description', content: 'YewFence的联系信息' }
  ]
})
</script>

<style scoped>
/* 页面样式已在全局CSS中定义 */
</style>
