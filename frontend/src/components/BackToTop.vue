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
/* 返回顶部按钮 Back to top */
.back-to-top {
    position: fixed;
    right: 1rem;
    bottom: 1.25rem;
    padding: .55rem .7rem;
    border-radius: var(--radius-sm);
    background: var(--color-accent);
    color: #fff;
    border: none;
    cursor: pointer;
    box-shadow: var(--shadow-md);
    opacity: .9;
    transition: var(--transition);
}

.back-to-top:hover {
    opacity: 1;
}

</style>
