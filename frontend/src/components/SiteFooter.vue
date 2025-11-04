<template>
  <footer class="site-footer">
    <div class="container footer-inner">
      <p>© <span id="year">{{ currentYear }}</span> YewFence,保留所有权利。</p>
      <p class="small">由 Vue 3 + Vite 构建。</p>
    </div>
  </footer>
</template>

<script setup>
import { ref } from 'vue'

const currentYear = ref(new Date().getFullYear())
</script>

<style scoped>
/* Footer样式已在全局CSS中定义 */
</style>
