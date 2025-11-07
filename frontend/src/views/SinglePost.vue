<template>
  <DefaultLayout>
    <main class="blog-container">
      <article v-if="loading" id="blog-content">
        <div id="blog-markdown">
          <h1>加载中...</h1>
          <div class="blog-body">
            <p>正在加载文章内容，请稍候...</p>
          </div>
        </div>
      </article>
      <article v-else-if="post" id="blog-content">
        <div id="blog-markdown">
          <div class="blog-body" v-html="post.content"></div>
        </div>
        <div class="blog-meta">
          <span class="blog-date">{{ formatDate(post.date_posted) }}</span> |
          <span class="blog-author">{{ post.author_name }}</span>
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
    <RouterLink class="btn primary blog-back" to="/blog">返回</RouterLink>
  </DefaultLayout>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useHead } from '@vueuse/head'
import { useRoute, RouterLink } from 'vue-router'
import DefaultLayout from '../components/DefaultLayout.vue'
import { getPost } from '../api/blog'

const route = useRoute()
const loading = ref(true)
const post = ref(null)
const postTitle = ref('Loading')
const metaContent = ref('')

// 格式化日期
const formatDate = (dateStr) => {
  const date = new Date(dateStr)
  return date.toISOString().split('T')[0]
}

// 加载文章
const loadPost = async () => {
  try {
    loading.value = true
    const postId = route.params.id
    const data = await getPost(postId)
    post.value = data.post
    // 设置动态标题和描述
    postTitle.value = data.post.title
    metaContent.value = data.post.brief_summary
  } catch (error) {
    console.error('加载文章失败:', error)
    post.value = null
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  loadPost()
})

useHead({
  title: postTitle,
  meta: [
    { name: 'description', content: metaContent }
  ]
})
</script>

<style>
@import '../assets/css/post.css';
</style>
