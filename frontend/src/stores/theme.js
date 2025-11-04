import { defineStore } from 'pinia'
import { ref, watch } from 'vue'

export const useThemeStore = defineStore('theme', () => {
  const THEME_KEY = 'mysite-theme'

  // 从localStorage读取主题，默认为light
  const theme = ref(localStorage.getItem(THEME_KEY) || 'light')

  // 切换主题
  const toggleTheme = () => {
    theme.value = theme.value === 'dark' ? 'light' : 'dark'
  }

  // 监听主题变化，同步到localStorage和DOM
  watch(theme, (newTheme) => {
    localStorage.setItem(THEME_KEY, newTheme)
    document.documentElement.setAttribute('data-theme', newTheme)

    // 添加过渡动画类
    document.documentElement.classList.add('theme-transition')
    setTimeout(() => {
      document.documentElement.classList.remove('theme-transition')
    }, 700)
  }, { immediate: true })

  return {
    theme,
    toggleTheme
  }
})
