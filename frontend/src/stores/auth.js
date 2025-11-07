import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useAuthStore = defineStore('auth', () => {
  const isAuthenticated = ref(false)

  // 检查登录状态（从cookie或localStorage）
  const checkAuth = () => {
    // 这里可以通过检查cookie或发送请求到后端验证
    // 简单实现：检查sessionStorage
    isAuthenticated.value = sessionStorage.getItem('authenticated') === 'true'
  }

  const login = (userName) => {
    isAuthenticated.value = true
    sessionStorage.setItem('username', userName)
    sessionStorage.setItem('authenticated', 'true')
  }

  const logout = () => {
    isAuthenticated.value = false
    sessionStorage.removeItem('authenticated')
    sessionStorage.removeItem('username')
  }

  return {
    isAuthenticated,
    checkAuth,
    login,
    logout
  }
})
