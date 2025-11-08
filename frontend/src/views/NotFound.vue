<template>
  <DefaultLayout>
    <main class="error-container theme-transition">
      <section class="error-card">
        <div class="error-hero" aria-hidden="true">
          <span class="d1">4</span>
          <span class="d2">0</span>
          <span class="d3">4</span>
        </div>
        <h1 class="error-title">页面不见了</h1>
        <p class="error-desc">抱歉，你访问的页面不存在或已被移动。你可以返回上一页，或前往首页继续浏览。</p>
        <div class="error-actions">
          <RouterLink class="btn primary" to="/">返回首页</RouterLink>
          <button class="btn" type="button" @click="goBack">返回上一页</button>
        </div>
      </section>
    </main>
  </DefaultLayout>
</template>

<script setup>
import { useRouter, RouterLink } from 'vue-router'
import { useHead } from '@vueuse/head';
import DefaultLayout from '../components/DefaultLayout.vue'

const router = useRouter()

useHead ({
  title: "404 页面未找到 - YewFenceSite",
  meta: [
    { name: 'description', content: '抱歉，你访问的页面不存在或已被移动。你可以返回上一页，或前往首页继续浏览。' }
  ]
})

const goBack = () => {
  router.go(-1)
}
</script>

<style>
@import '../assets/css/error.css';
</style>
