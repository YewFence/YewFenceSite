<template>
  <footer class="site-footer">
    <div class="container footer-inner">
      <p>{{ copyrightText }}</p>
      <p class="small">{{ content.buildInfo }}</p>
    </div>
  </footer>
</template>

<script setup>
import { ref, computed } from 'vue'
import { components } from '@/utils/content'

const content = components.footer
const currentYear = ref(new Date().getFullYear())

const copyrightText = computed(() => {
  return content.copyright.replace('{year}', currentYear.value)
})
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
