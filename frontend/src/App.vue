<template>
  <div id="app">
    <RouterView />
  </div>
</template>

<script setup>
import { RouterView } from 'vue-router'
import { useThemeStore } from './stores/theme'
import { useHead } from '@vueuse/head'

// 初始化主题
const themeStore = useThemeStore()

// 设置当前年份
const yearSpan = document.getElementById('year')
if (yearSpan) {
  yearSpan.textContent = new Date().getFullYear()
}

// 设置全局标题和描述
useHead({
  title: 'YewFenceSite',
  meta: [
    { name: 'description', content: "YewFence's Site" },
    { name: 'author', content: 'YewFence' }
  ]
})
</script>

<style>
/* 全局样式由 style.css 提供 */
</style>
