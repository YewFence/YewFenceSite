<template>
  <DefaultLayout>
    <main class="mgmt-wrapper">
      <div class="container" id="mgmtRoot">
        <div style="display:flex; justify-content:space-between; align-items:center; gap:1rem; margin-bottom:1rem;">
          <h1 style="margin:0;">{{ content.header.title }}</h1>
          <span class="logo">{{ content.header.welcomePrefix }} {{ user_name }}!</span>
          <div style="display:flex; gap:.5rem; flex-wrap:wrap;">
            <button class="btn" @click="handleLogout">{{ content.header.logoutButton }}</button>
            <RouterLink class="btn" to="/">{{ content.header.homeButton }}</RouterLink>
          </div>
        </div>
        <div class="large-card" aria-label="账户与安全">
          <div class="title-wrapper">
            <h2>{{ content.password.title }}</h2>
          </div>
          <form id="changePwdForm" class="change-password" @submit.prevent="changePassword" novalidate>
            <div class="grid">
              <label>{{ content.password.newPassword }}
                <input type="password" v-model="new_password" autocomplete="new-password">
              </label>
              <label>{{ content.password.confirmPassword }}
                <input type="password" v-model="confirm_password" autocomplete="new-password">
              </label>
            </div>
            <div class="form-actions">
              <button class="btn primary" type="submit" @click="changePassword">{{ content.password.submitButton }}</button>
              <button class="btn" type="reset">{{ content.password.resetButton }}</button>
            </div>
          </form>
        </div>

        <!-- 导出按钮 -->
        <div class="export-section">
          <h2>{{ content.export.title }}</h2>
          <div style="display:flex; gap:.5rem; flex-wrap:wrap;">
            <button class="btn" @click="exportJson">{{ content.export.jsonButton }}</button>
            <button class="btn" @click="exportMdZip">{{ content.export.mdZipButton }}</button>
          </div>
        </div>

        <!-- 文章列表 -->
        <div class="posts-section">
          <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:1rem;">
            <h2>{{ content.posts.title }}</h2>
            <button class="btn primary" @click="openCreateModal">{{ content.posts.newButton }}</button>
          </div>

          <div v-if="loading" class="loading">{{ content.posts.loading }}</div>
          <div v-else-if="posts.length === 0" class="empty">{{ content.posts.empty }}</div>
          <div v-else class="post-list">
            <div v-for="post in posts" :key="post.id" class="post-item large-card" :id="`post-${post.id}`">
              <div class="post-meta">
                <div class="post-kv">
                  <span class="k">{{ content.posts.labels.id }}</span>
                  <span class="v v-id future">{{ post.id }}</span>
                </div>
                <div class="post-kv">
                  <span class="k">{{ content.posts.labels.author }}</span>
                  <span class="v v-author">{{ post.author_name }}</span>
                </div>
                <div class="post-kv">
                  <span class="k">{{ content.posts.labels.date }}</span>
                  <span class="v v-date">{{ formatDate(post.date_posted) }}</span>
                </div>
                <div class="post-kv" style="grid-column:1/-1;">
                  <span class="k">{{ content.posts.labels.title }}</span>
                  <span class="v v-title">{{ post.title }}</span>
                </div>
                <div class="post-kv" style="grid-column:1/-1;">
                  <span class="k">{{ content.posts.labels.summary }}</span>
                  <span class="v v-summary">{{ post.brief_summary }}</span>
                </div>
                <div class="post-kv" style="grid-column:1/-1;">
                  <span class="k">{{ content.posts.labels.note }}</span>
                  <span class="v v-note">{{ post.note }}</span>
                </div>
              </div>
              <div class="post-actions">
                <button class="btn small" @click="editPost(post)">{{ content.posts.actions.edit }}</button>
                <button class="btn small" @click="downloadMarkdown(post.id)">{{ content.posts.actions.downloadMd }}</button>
                <a :href="`/blog/${post.id}/preview`" target="_blank" class="btn small">{{ content.posts.actions.preview }}</a>
                <button class="btn small danger" @click="deletePost(post.id)">{{ content.posts.actions.delete }}</button>
              </div>
            </div>
          </div>
        </div>

        <!-- 编辑弹窗 -->
        <div v-if="showEditModal" class="edit-mask" @click.self="closeEditModal">
          <div class="edit-panel">
            <div class="edit-head">
              <strong>{{ editingPost ? content.editModal.editTitle : content.editModal.createTitle }}</strong>
              <button class="close-x" @click="closeEditModal">×</button>
            </div>
            <div class="edit-body">
              <form class="edit-grid" @submit.prevent="savePost">
                <label class="field">
                  {{ content.editModal.fields.title.label }}
                  <input v-model="formData.title" type="text" />
                  <span class="hint">{{ content.editModal.fields.title.hint }}</span>
                </label>
                <label class="field">
                  {{ content.editModal.fields.author.label }}
                  <input v-model="formData.author" type="text" />
                  <span class="hint">{{ content.editModal.fields.author.hint }}</span>
                </label>
                <label class="field">
                  {{ content.editModal.fields.date.label }}
                  <input v-model="formData.date" type="date" />
                </label>
                <label class="field" style="grid-column:1/-1;">
                  {{ content.editModal.fields.summary.label }}
                  <textarea v-model="formData.summary" rows="3"></textarea>
                </label>
                <label class="field" style="grid-column:1/-1;">
                  {{ content.editModal.fields.note.label }}
                  <textarea v-model="formData.note" rows="2"></textarea>
                  <span class="hint">{{ content.editModal.fields.note.hint }}</span>
                </label>
                <label class="field">
                  {{ content.editModal.fields.status.label }}
                  <select v-model="formData.status"
                  :class='formData.status + "-select"'
                  class="edit-panel">
                    <option value="published" id="published-select">{{ content.editModal.fields.status.options.published }}</option>
                    <option value="hidden" id="hidden-select">{{ content.editModal.fields.status.options.hidden }}</option>
                  </select>
                </label>
                <label class="field" style="grid-column:1/-1;">
                  {{ content.editModal.fields.upload.label }}
                  <input type="file" accept=".md" @change="handleFileUpload" id="fMdFile"/>
                  <span class="hint">{{ content.editModal.fields.upload.hint }}</span>
                </label>
              </form>
            </div>
            <div class="edit-foot">
              <button class="btn" @click="closeEditModal">{{ content.editModal.buttons.cancel }}</button>
              <button class="btn primary" @click="savePost" :disabled="saving">
                {{ saving ? content.editModal.buttons.saving : content.editModal.buttons.save }}
              </button>
            </div>
          </div>
        </div>
      </div>
    </main>
  </DefaultLayout>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter, RouterLink } from 'vue-router'
import { useHead } from '@vueuse/head'
import DefaultLayout from '../components/DefaultLayout.vue'
import { useAuthStore } from '../stores/auth'
import { loginAlertStore } from '../stores/loginAlert'
import {
  getPosts,
  createPost,
  editPost as apiEditPost,
  deletePost as apiDeletePost,
  downloadPostMarkdown,
  exportPostsJson,
  exportPostsMdZip
} from '../api/blog'
import { logout as apiLogout, updatePassword as apiUpdatePassword } from '../api/auth'
import { pages } from '@/utils/content'

const content = pages.management

const router = useRouter()
const authStore = useAuthStore()
const store = loginAlertStore()
const user_name = ref('')
const loading = ref(true)
const saving = ref(false)
const posts = ref([])
const showEditModal = ref(false)
const editingPost = ref(null)
const formData = ref({
  title: '',
  author: '',
  date: '',
  summary: '',
  note: '',
  status: 'hidden',
  content: ''
})
const uploadedFile = ref(null)
const new_password = ref('')
const confirm_password = ref('')

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
    alert(content.messages.loadError)
  } finally {
    loading.value = false
  }
}

// 修改密码
const changePassword = async () => {
  const userName = sessionStorage.getItem('username') || 'yewfence'
  const newPassword = new_password.value?.trim()
  const confirmPassword = confirm_password.value?.trim()

  if (!newPassword || !confirmPassword) {
    alert(content.messages.passwordEmpty)
    return
  }
  if (newPassword !== confirmPassword) {
    alert(content.messages.passwordMismatch)
    return
  }

  try {
    const result = await apiUpdatePassword(userName, newPassword)
    if (result?.error) {
      throw new Error(result.error)
    }
    if (result?.success === true || result?.success === 'true') {
      console.log('密码修改成功')
    } else {
      console.warn('未知错误')
    }
    await apiLogout()
    authStore.logout()
    store.setInfoForLoginPage('success', content.messages.passwordSuccess)
    router.push('/login')
  } catch (error) {
    const msg = error?.response?.data?.error || error?.message || '未知错误'
    console.error('密码修改失败:', error)
    alert('密码修改失败: ' + msg)
  }
}

// 打开新建弹窗
const openCreateModal = () => {
  editingPost.value = null
  formData.value = {
    title: '',
    author: '',
    date: new Date().toISOString().split('T')[0],
    summary: '',
    note: '',
    status: 'hidden',
    content: ''
  }
  showEditModal.value = true
}

// 打开编辑弹窗
const editPost = (post) => {
  editingPost.value = post
  formData.value = {
    title: post.title,
    author: post.author_name,
    date: formatDate(post.date_posted),
    summary: post.brief_summary || '',
    note: post.note || '',
    status: post.status,
    content: ''
  }
  showEditModal.value = true
}

// 关闭编辑弹窗
const closeEditModal = () => {
  showEditModal.value = false
  editingPost.value = null
  uploadedFile.value = null
}

// 处理文件上传
const handleFileUpload = async (event) => {
  const file = event.target.files[0]
  if (file) {
    uploadedFile.value = file
    const fileContent = await file.text()
    formData.value.content = fileContent
  }
}

// 保存文章
const savePost = async () => {
  try {
    saving.value = true

    const data = new FormData()
    data.append('title', formData.value.title)
    data.append('author', formData.value.author)
    data.append('date', formData.value.date)
    data.append('summary', formData.value.summary)
    data.append('note', formData.value.note)
    data.append('status', formData.value.status)
    if (formData.value.content) {
      data.append('content', formData.value.content)
    }

    if (editingPost.value) {
      const response = await apiEditPost(editingPost.value.id, data)
      alert(`文章更新成功！文章 ID: ${response.post_id || editingPost.value.id}`)
    } else {
      const response = await createPost(data)
      alert(`文章创建成功！文章 ID: ${response.post_id}`)
    }

    closeEditModal()
    loadPosts()
  } catch (error) {
    console.error('保存失败:', error)
    alert('保存失败: ' + (error.response?.data?.error || error.message))
  } finally {
    saving.value = false
  }
}

// 删除文章
const deletePost = async (id) => {
  if (!confirm(content.messages.deleteConfirm)) {
    return
  }

  try {
    await apiDeletePost(id)
    alert(content.messages.deleteSuccess)
    loadPosts()
  } catch (error) {
    console.error('删除失败:', error)
    alert('删除失败: ' + (error.response?.data?.error || error.message))
  }
}

// 下载Markdown
const downloadMarkdown = async (id) => {
  try {
    const blob = await downloadPostMarkdown(id)
    const url = window.URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = `post-${id}.md`
    a.click()
    window.URL.revokeObjectURL(url)
  } catch (error) {
    console.error('下载失败:', error)
    alert('下载失败')
  }
}

// 导出JSON
const exportJson = async () => {
  try {
    const blob = await exportPostsJson()
    const url = window.URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = 'blog.json'
    a.click()
    window.URL.revokeObjectURL(url)
  } catch (error) {
    console.error('导出失败:', error)
    alert('导出失败')
  }
}

// 导出Markdown压缩包
const exportMdZip = async () => {
  try {
    const blob = await exportPostsMdZip()
    const url = window.URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = 'all_posts_md.zip'
    a.click()
    window.URL.revokeObjectURL(url)
  } catch (error) {
    console.error('导出失败:', error)
    alert('导出失败')
  }
}

// 登出
const handleLogout = async () => {
  try {
    await apiLogout()
    authStore.logout()
    const alertStore = loginAlertStore()
    alertStore.setInfoForLoginPage('info', content.messages.logoutSuccess)
    router.push('/login')
  } catch (error) {
    console.error('登出失败:', error)
  }
}

useHead({
  title: content.meta.title,
  meta: [
    { name: 'description', content: content.meta.description },
    { name: 'author', content: content.meta.author }
  ]
})

onMounted(async () => {
  const isAuth = await authStore.checkAuth()
  if (!isAuth) {
    store.setInfoForLoginPage('info', content.messages.loginRequired)
    router.push('/login')
  } else {
    user_name.value = localStorage.getItem('username') || ''
    await loadPosts()
  }
})
</script>

<style>
@import '../assets/css/management.css';
.logo {
    /* 默认向flexbox起点对齐 */
    font-size: 1.35rem;
    font-weight: 600;
    letter-spacing: .5px;
}

.logo span {
    color: var(--color-accent);
}
</style>
