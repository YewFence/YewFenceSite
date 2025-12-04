<template>
  <DefaultLayout>
    <main class="login-wrapper">
      <section class="login-card" aria-label="登录面板">
        <h1>{{ content.title }}</h1>
        <p class="muted">{{ content.notice }}</p>
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
            <label for="username">{{ content.form.username.label }}</label>
            <input
              id="username"
              v-model="username"
              type="text"
              :placeholder="content.form.username.placeholder"
              autocomplete="username"
              required
              autofocus
            />
            <label for="password">{{ content.form.password.label }}</label>
            <input
              id="password"
              v-model="password"
              type="password"
              :placeholder="content.form.password.placeholder"
              autocomplete="current-password"
              required
            />
          </div>
          <div class="actions">
            <RouterLink class="btn" to="/">{{ content.buttons.back }}</RouterLink>
            <button class="btn primary" type="submit" :disabled="loading">
              {{ loading ? content.buttons.loading : content.buttons.login }}
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
import { pages } from '@/utils/content'

const content = pages.login

useHead({
  title: content.meta.title,
  meta: [
    { name: 'description', content: content.meta.description },
    { name: 'author', content: content.meta.author }
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
    alertMessage.value = content.messages.emptyFields
    return
  }

  try {
    loading.value = true
    alertMessage.value = ''

    const response = await apiLogin(username.value, password.value)

    if (response.success) {
      alertType.value = 'success'
      alertMessage.value = content.messages.success
      authStore.login(username.value)
      setTimeout(() => {
      router.push('/management')
      }, 1000)
    } else {
      alertType.value = 'error'
      alertMessage.value = response.error || content.messages.error
    }
  } catch (error) {
    alertType.value = 'error'
    alertMessage.value = error?.response?.data?.error || error?.message || content.messages.error
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
