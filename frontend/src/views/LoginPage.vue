<template>
  <DefaultLayout>
    <main class="login-wrapper">
      <section class="login-card" aria-label="登录面板">
        <h1>登录</h1>
        <p class="muted">本页仅用于站点维护人员使用。</p>
        <div v-if="alertMessage" class="alerts" aria-live="polite">
          <div
            :class="['alert', `alert-${alertType}`]"
            role="alert"
          >
            {{ alertIcon }} {{ alertMessage }}
          </div>
        </div>
        <form @submit.prevent="handleLogin" novalidate>
          <div class="field">
            <label for="username">用户名</label>
            <input
              id="username"
              v-model="username"
              type="text"
              placeholder="输入用户名"
              autocomplete="username"
              required
              autofocus
            />
            <label for="password">密码</label>
            <input
              id="password"
              v-model="password"
              type="password"
              placeholder="输入密码"
              autocomplete="current-password"
              required
            />
          </div>
          <div class="actions">
            <RouterLink class="btn" to="/">返回</RouterLink>
            <button class="btn primary" type="submit" :disabled="loading">
              {{ loading ? '登录中...' : '登录' }}
            </button>
          </div>
        </form>
      </section>
    </main>
  </DefaultLayout>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useHead } from '@vueuse/head'
import { useRouter, RouterLink } from 'vue-router'
import DefaultLayout from '../components/DefaultLayout.vue'
import { useAuthStore } from '../stores/auth'
import { loginAlertStore } from '../stores/loginAlert'
import { login as apiLogin } from '../api/auth'

useHead({
  title: '登录 - YewFenceSite',
  meta: [
    { name: 'description', content: '登录以访问管理功能。' },
    { name: 'author', content: 'YewFence' }
  ]
})

const router = useRouter()
const authStore = useAuthStore()
const store = loginAlertStore()
const username = ref('')
const password = ref('')
const loading = ref(false)
const alertType = ref('')
const alertMessage = ref('')

const alertIcon = computed(() => {
  switch (alertType.value) {
    case 'error':
      return '⚠️'
    case 'success':
      return '✅'
    case 'info':
      return 'ℹ️'
    default:
      return ''
  }
})

const handleLogin = async () => {
  if (!username.value || !password.value) {
    alertType.value = 'error'
    alertMessage.value = '请输入用户名和密码'
    return
  }

  try {
    loading.value = true
    alertMessage.value = ''

    const response = await apiLogin(username.value, password.value)

    if (response.success) {
      alertType.value = 'success'
      alertMessage.value = '登录成功！正在跳转...'
      authStore.login(username.value)
      setTimeout(() => {
      router.push('/management')
      }, 1000)
    } else {
      alertType.value = 'error'
      alertMessage.value = response.error || '登录失败，请检查用户名和密码'
    }
  } catch (error) {
    alertType.value = 'error'
    alertMessage.value = error?.response?.data?.error || error?.message || '登录失败，请检查用户名和密码'
  } finally {
    loading.value = false
  }
}

onMounted(async () => {
  const isAuthenticated = await authStore.checkAuth()
  if (isAuthenticated) {
    router.push('/management')
  }
  const storeMessageText = store.messageText
  if (storeMessageText) {
    alertType.value = store.messageType
    alertMessage.value = storeMessageText
    store.clearInfo()
  }
})
</script>

<style>
@import '../assets/css/login.css';
</style>
