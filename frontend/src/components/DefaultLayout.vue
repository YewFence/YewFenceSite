<template>
  <div>
    <SiteHeader />
    <main>
      <slot />
    </main>
    <SiteFooter />
    <BackToTop />
  </div>
</template>

<script setup>
import SiteHeader from './SiteHeader.vue'
import SiteFooter from './SiteFooter.vue'
import BackToTop from './BackToTop.vue'
</script>

<style scoped>
/* Layout样式已在全局CSS中定义 */
</style>
