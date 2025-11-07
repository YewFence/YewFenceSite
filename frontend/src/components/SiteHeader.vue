<template>
  <header class="site-header">
    <div class="container nav-wrapper">
      <RouterLink class="logo" to="/">YewFence's <span>Site</span></RouterLink>
      <nav id="mainNav" class="nav" aria-label="主导航">
        <button
          class="nav-toggle"
          id="navToggle"
          :aria-expanded="isMenuOpen"
          aria-controls="navMenu"
          @click="toggleMenu"
        >☰</button>
        <ul id="navMenu" class="nav-menu" :class="{ open: isMenuOpen }">
          <li><RouterLink to="/" @click="closeMenu">首页</RouterLink></li>
          <li><RouterLink to="/about" @click="closeMenu">关于我</RouterLink></li>
          <li><RouterLink to="/interests" @click="closeMenu">我的兴趣</RouterLink></li>
          <li><RouterLink to="/contact" @click="closeMenu">联系我</RouterLink></li>
          <li><RouterLink to="/blog" @click="closeMenu">个人博客</RouterLink></li>
          <li v-if="showAdminLink"><RouterLink to="/management" @click="closeMenu">管理页</RouterLink></li>
          <li>
            <button
              id="themeSwitcher"
              class="theme-btn"
              aria-label="切换主题"
              @click="toggleTheme"
            >
              {{ themeStore.theme === 'dark' ? '☀️' : '🌙' }}
            </button>
          </li>
        </ul>
      </nav>
    </div>
  </header>
</template>

<script setup>
import { ref, onMounted, onUnmounted, computed } from 'vue'
import { RouterLink } from 'vue-router'
import { useThemeStore } from '../stores/theme'
import { useAuthStore } from '../stores/auth'

const themeStore = useThemeStore()
const isMenuOpen = ref(false)
const showAdminLink = ref(false)

const checkAuth = async () => {
  // 只有在用户已认证时才显示“管理页”链接
  const authStore = useAuthStore()
  const isAuthenticated = await authStore.checkAuth()
  return isAuthenticated
}

const toggleMenu = () => {
  isMenuOpen.value = !isMenuOpen.value
}

const closeMenu = () => {
  isMenuOpen.value = false
}

const toggleTheme = () => {
  themeStore.toggleTheme()
}

// 点击导航区域外时关闭菜单
const handleClickOutside = (e) => {
  const navMenu = document.getElementById('navMenu')
  const navToggle = document.getElementById('navToggle')
  if (navMenu && !navMenu.contains(e.target) && e.target !== navToggle && isMenuOpen.value) {
    closeMenu()
  }
}

onMounted(async () => {
  document.addEventListener('click', handleClickOutside)
  showAdminLink.value = await checkAuth()
})

onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside)
})
</script>

<style scoped>
/* Header样式已在全局CSS中定义 */
.nav-menu a.router-link-active::after{
    /* 鼠标悬停时，水平缩放到 1*/
    transform: scaleX(1);
}

</style>
