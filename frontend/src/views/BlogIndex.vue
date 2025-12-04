<template>
  <DefaultLayout>
    <section class="page-hero mini">
      <div class="container">
        <h1>{{ content.hero.title }}</h1>
        <p class="subtitle">{{ content.hero.subtitle }}</p>
      </div>
    </section>
    <section class="section">
      <div v-if="isAuth" class="container admin-container">
        <span class="logo">{{ content.admin.welcomePrefix }} {{ user_name }}!</span>
        <button id='logoutButton' class="btn primary" @click="handleLogout">{{ content.admin.logoutButton }}</button>
      </div>
      <div class="container">
        <div id="blogs-list" class="large-cards-list">
          <!-- 加载中 -->
          <article v-if="loading" class="large-card" id="loadingMessage">
            <h2>{{ content.loading.title }}</h2>
            <p class="meta">{{ content.loading.subtitle }}</p>
            <p>{{ content.loading.hint }}</p>
          </article>
          <!-- 博客列表 -->
          <article
            v-for="post in posts"
            :key="post.id"
            class="large-card"
          >
            <h2 class="blog-list-item-title">{{ post.title }}</h2>
            <p class="blog-list-item-meta">
              <span class="blog-list-item-artistic-character">{{ content.post.postedOn }} </span>
              <span class="blog-list-item-date"> {{ formatDate(post.date_posted) }}</span>
              <span class="blog-list-item-artistic-character"> {{ content.post.by }} </span>
              <span class="blog-list-item-author">{{ post.author_name }} </span>
              <span v-if="isAuth" class="status-badge">{{ post.status }}</span>
            </p>
            <p class="blog-list-item-brief-summary">{{ post.brief_summary }}</p>
            <RouterLink class="card-link blog-list-item-link" :to="`/blog/${post.id}`"></RouterLink>
          </article>
          <!-- 无文章 -->
          <article v-if="!loading && posts.length === 0" class="large-card">
            <h2>{{ content.empty.title }}</h2>
            <p class="meta">{{ content.empty.subtitle }}</p>
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
import { pages } from '@/utils/content'

const content = pages.blog

useHead({
  title: content.meta.title,
  meta: [
    { name: 'description', content: content.meta.description },
    { name: 'author', content: content.meta.author }
  ]
})

const router = useRouter()
const authStore = useAuthStore()
const loading = ref(true)
const posts = ref([])
const isAuth = ref(false)
const user_name = ref('')

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
  if (isAuth.value) {
    user_name.value = localStorage.getItem('username') || ''
  }
  await loadPosts()
})
</script>

<style scoped>
/* Blog */
/* 文章列表样式(感觉都没有什么要整的) */

.blog-list-item-artistic-character {
    color: var(--color-accent);
}

.blog-meta {
    margin-top: 2rem;
    font-size: .85rem;
    color: var(--color-text-alt);
    display: flex;
    gap: 1.5rem;
    flex-wrap: wrap;
}

.blog-meta-item {
    display: flex;
    align-items: center;
    gap: .4rem;
}

.blog-meta-item-icon {
    font-size: 1.1rem;
    color: var(--color-accent);
}

.blog-meta-item:hover .blog-meta-item-icon {
    color: var(--color-accent-hover);
}

#logoutButton {
  margin-left: 0.5rem;
}
.status-badge {
  font-size: .8rem;
  border: 1px solid var(--color-border);
  padding: .1rem .4rem;
  margin-left: .5rem;
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
