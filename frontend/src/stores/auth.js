import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useAuthStore = defineStore('auth', () => {
  const user_name = ref(null)

  // 检查登录状态（从cookie或localStorage）
  const checkAuth = async () => {
    // 这里可以通过检查cookie或发送请求到后端验证
    // 简单实现：检查sessionStorage
    try {
      const response = await fetch('/api/auth/status')
      const data = await response.json()
      return data.authenticated
    } catch (error) {
      console.error('Error checking auth status:', error)
      return false
    }
  }

  const login = (userName) => {
    sessionStorage.setItem('username', userName)
    user_name.value = userName
  }

  const logout = () => {
    sessionStorage.removeItem('username')
    user_name.value = null
  }

  return {
    checkAuth,
    login,
    logout,
    user_name
  }
})
