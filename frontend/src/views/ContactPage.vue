<template>
  <DefaultLayout>
    <section class="page-hero mini">
      <div class="container">
        <h1>{{ content.hero.title }}</h1>
        <p class="subtitle">{{ content.hero.subtitle }}</p>
      </div>
    </section>
    <section class="section">
      <div class="container">
        <div class="title-wrapper">
          <h2 class="section-title" id="contact-title">{{ content.channels.title }}</h2>
          <!-- 提示信息仅在需要时显示 -->
          <div id="prompt-message" :class="{ 'is-visible': promptVisible }">
            <p>{{ promptText }}</p>
          </div>
        </div>
        <div class="grid projects-grid">
          <article v-for="(channel, index) in content.channels.items" :key="channel.name" class="card">
            <h3>{{ channel.name }}</h3>
            <p class="text-to-copy">{{ channel.value }}</p>
            <button
              class="copy-btn"
              :aria-label="channel.ariaLabel"
              @click="copyText(channel.value, index)"
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
import { pages } from '@/utils/content'

const content = pages.contact

const promptVisible = ref(false)
const promptText = ref(content.channels.prompt.default)

const showPrompt = () => {
  promptVisible.value = true
}

const hidePrompt = () => {
  if (promptText.value === content.channels.prompt.default) {
    promptVisible.value = false
  }
}

const copyText = async (text, index) => {
  try {
    await navigator.clipboard.writeText(text)
    promptText.value = content.channels.prompt.success
    promptVisible.value = true
    setTimeout(() => {
      promptText.value = content.channels.prompt.default
      promptVisible.value = false
    }, 2000)
  } catch (err) {
    console.error('复制失败: ', err)
    promptText.value = content.channels.prompt.error
    promptVisible.value = true
    setTimeout(() => {
      promptText.value = content.channels.prompt.default
      promptVisible.value = false
    }, 2000)
  }
}

// 设置页面标题和描述
useHead({
  title: content.meta.title,
  meta: [
    { name: 'description', content: content.meta.description }
  ]
})
</script>

<style scoped>
/* 提示信息 Prompt message */
.title-wrapper {
    display: flex;
    gap:12px;
    margin-bottom: 2rem;
}

#contact-title {
    margin: 0;
}

#prompt-message {
    align-items: center;
    border: 1px solid var(--color-border);
    border-radius: 4px;
    padding: 2px 10px;
    box-shadow: var(--shadow-md);
    font-size: 14px;
    color: var(--color-accent-hover);
    font-weight: 1000;
    white-space: nowrap;
    /* 初始不可见 */
    opacity: 0;
    /* 不可点击 */
    pointer-events: none;
    transition: opacity 0.4s ease-in-out, transform .4s ease-in-out;
    transform: translateY(0);
}

#prompt-message.is-visible {
    opacity: 1;
    transform: translateY(-3px);
}
</style>
