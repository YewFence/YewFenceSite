<template>
  <div id="app">
    <RouterView />
  </div>
</template>

<script setup>
import { RouterView } from 'vue-router'
import { useThemeStore } from './stores/theme'

// 初始化主题
const themeStore = useThemeStore()

// 设置当前年份
const yearSpan = document.getElementById('year')
if (yearSpan) {
  yearSpan.textContent = new Date().getFullYear()
}
</script>

<style>
/* 全局样式由 style.css 提供 */
</style>
