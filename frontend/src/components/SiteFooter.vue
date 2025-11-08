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
/* 页脚 Footer */
.site-footer {
    padding: 2.5rem 0 2.25rem;
    background: transparent;
    margin-top: 2rem;
}

.footer-inner {
    text-align: center;
    font-size: .8rem;
    color: var(--color-text-light);
}
</style>
