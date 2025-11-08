<template>
  <DefaultLayout>
    <main class="blog-container">
      <!-- 预览模式提示横幅 -->
      <div class="preview-banner" v-if="!loading">
        <span class="preview-icon">👁️</span>
        <span class="preview-text">预览模式 - 仅登录用户可见</span>
      </div>

      <article v-if="loading" id="blog-content">
        <div id="blog-markdown">
          <h1>加载中...</h1>
          <div class="blog-body">
            <p>正在加载文章预览，请稍候...</p>
          </div>
        </div>
      </article>
      <article v-else-if="post" id="blog-content">
        <div id="blog-markdown">
          <h1>{{ post.title }}</h1>
          <div class="blog-body" v-html="post.content"></div>
        </div>
        <div class="blog-meta">
          <span class="blog-date">{{ formatDate(post.date_posted) }}</span> |
          <span class="blog-author">{{ post.author_name }}</span>
          <span v-if="post.status === 'hidden'" class="status-badge hidden">隐藏</span>
          <span v-else class="status-badge published">已发布</span>
        </div>
      </article>
      <article v-else id="blog-content">
        <div id="blog-markdown">
          <h1>文章不存在</h1>
          <div class="blog-body">
            <p>抱歉，您访问的文章不存在或已被删除。</p>
          </div>
        </div>
      </article>
    </main>
    <RouterLink class="btn primary blog-back" to="/management">返回管理</RouterLink>
  </DefaultLayout>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useHead } from '@vueuse/head'
import { useRoute, RouterLink } from 'vue-router'
import DefaultLayout from '../components/DefaultLayout.vue'
import { previewPost } from '../api/blog'

const route = useRoute()
const loading = ref(true)
const post = ref(null)
const postTitle = ref('')
const pageTitle = ref('')

// 格式化日期
const formatDate = (dateStr) => {
  const date = new Date(dateStr)
  return date.toISOString().split('T')[0]
}

// 加载文章预览
const loadPost = async () => {
  try {
    loading.value = true
    const postId = route.params.id
    const data = await previewPost(postId)
    post.value = data.post
    postTitle.value = post.value.title
    pageTitle.value = `${postTitle.value} - 预览 - YewFenceSite`
  } catch (error) {
    console.error('加载文章预览失败:', error)
    post.value = null
  } finally {
    loading.value = false
  }
}

useHead({
  title: pageTitle,
  meta: [
    { name: 'description', content: '文章预览页面，仅登录用户可见。' },
    { name: 'author', content: 'YewFence' }
  ]
})


onMounted(() => {
  loadPost()
})
</script>

<style>
@import '../assets/css/post.css';

/* 预览模式横幅样式 */
.preview-banner {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 12px 20px;
  border-radius: 8px;
  margin-bottom: 20px;
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 14px;
  font-weight: 500;
  box-shadow: 0 2px 8px rgba(102, 126, 234, 0.3);
}

.preview-icon {
  font-size: 18px;
}

.preview-text {
  flex: 1;
}

/* 状态徽章样式 */
.status-badge {
  margin-left: 10px;
  padding: 2px 8px;
  border-radius: 4px;
  font-size: 12px;
  font-weight: 600;
}

.status-badge.hidden {
  background-color: #fbbf24;
  color: #78350f;
}

.status-badge.published {
  background-color: #10b981;
  color: white;
}
</style>
