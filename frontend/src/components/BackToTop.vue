<template>
  <button
    id="backToTop"
    aria-label="返回顶部"
    class="back-to-top"
    :hidden="!isVisible"
    :style="{ opacity: isVisible ? '1' : '0' }"
    @click="scrollToTop"
  >↑</button>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'

const isVisible = ref(false)
const showAt = 480

const handleScroll = () => {
  isVisible.value = window.scrollY > showAt
}

const scrollToTop = () => {
  window.scrollTo({ top: 0, behavior: 'smooth' })
}

onMounted(() => {
  window.addEventListener('scroll', handleScroll, { passive: true })
})

onUnmounted(() => {
  window.removeEventListener('scroll', handleScroll)
})
</script>

<style scoped>
/* BackToTop样式已在全局CSS中定义 */
</style>
