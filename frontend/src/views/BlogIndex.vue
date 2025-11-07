<template>
  <DefaultLayout>
    <section class="page-hero mini">
      <div class="container">
        <h1>个人博客</h1>
        <p class="subtitle">分享编程与生活的点滴</p>
      </div>
    </section>
    <section class="section">
      <div v-if="isAuth" class="container admin-container">
        <span class="logo">Welcome, {{ authStore.user_name }}!</span>
        <RouterLink class="btn primary" to="/management">管理后台</RouterLink>
        <button class="btn primary" @click="handleLogout">登出</button>
      </div>
      <div class="container">
        <div id="blogs-list" class="large-cards-list">
          <!-- 加载中 -->
          <article v-if="loading" class="large-card" id="loadingMessage">
            <h2>加载中...</h2>
            <p class="meta">请稍候</p>
            <p>如果长时间未加载，请检查网络连接或刷新页面。</p>
          </article>
          <!-- 博客列表 -->
          <article
            v-for="post in posts"
            :key="post.id"
            class="large-card"
          >
            <h2 class="blog-list-item-title">{{ post.title }}</h2>
            <p class="blog-list-item-meta">
              <span class="blog-list-item-artistic-character">Posted on</span>
              <span class="blog-list-item-date"> {{ formatDate(post.date_posted) }}</span>
              <span> By </span>
              <span class="blog-list-item-author">{{ post.author_name }}</span>
              <span v-if="post.status !== 'published'" class="status-badge">{{ post.status }}</span>
            </p>
            <p class="blog-list-item-brief-summary">{{ post.brief_summary }}</p>
            <RouterLink class="card-link blog-list-item-link" :to="`/blog/${post.id}`"></RouterLink>
          </article>
          <!-- 无文章 -->
          <article v-if="!loading && posts.length === 0" class="large-card">
            <h2>暂无文章</h2>
            <p class="meta">还没有发布任何文章</p>
          </article>
        </div>
      </div>
    </section>
  </DefaultLayout>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useHead } from '@vueuse/head'
import { RouterLink, useRouter } from 'vue-router'
import DefaultLayout from '../components/DefaultLayout.vue'
import { useAuthStore } from '../stores/auth'
import { getPosts } from '../api/blog'
import { logout as apiLogout } from '../api/auth'

useHead({
  title: '个人博客 - YewFenceSite',
  meta: [
    { name: 'description', content: '分享编程与生活的点滴' },
    { name: 'author', content: 'YewFence' }
  ]
})

const router = useRouter()
const authStore = useAuthStore()
const loading = ref(true)
const posts = ref([])
const isAuth = ref(false)

// 格式化日期
const formatDate = (dateStr) => {
  const date = new Date(dateStr)
  return date.toISOString().split('T')[0]
}

// 加载文章列表
const loadPosts = async () => {
  try {
    loading.value = true
    const data = await getPosts()
    posts.value = data.posts || []
  } catch (error) {
    console.error('加载文章失败:', error)
  } finally {
    loading.value = false
  }
}

// 登出
const handleLogout = async () => {
  try {
    await apiLogout()
    authStore.logout()
    router.push('/blog')
    alert('已成功登出')
    isAuth.value = false
  } catch (error) {
    console.error('登出失败:', error)
  }
}

onMounted(async () => {
  isAuth.value = await authStore.checkAuth()
  loadPosts()
})
</script>

<style scoped>
.status-badge {
  font-size: .8rem;
  border: 1px solid var(--color-border);
  padding: .1rem .4rem;
  border-radius: 6px;
}
.admin-container {
  padding: 1rem;
  background: var(--surface-bg);
}
.admin-container .logo {
  font-weight: 600;
  color: var(--color-accent, #2b8aef);
  margin-right: .5rem;
}
.admin-container .btn {
  padding: .4rem .7rem;
  font-size: .95rem;
}
@media (max-width: 560px) {
  .admin-section {
    flex-direction: column;
    align-items: stretch;
  }
  .admin-section .logo {
    margin-bottom: .35rem;
  }
  .admin-section .btn {
    width: 100%;
  }
}
</style>
