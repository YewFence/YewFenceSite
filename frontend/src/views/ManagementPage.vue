<template>
  <DefaultLayout>
    <main class="mgmt-wrapper">
      <div class="container" id="mgmtRoot">
        <div style="display:flex; justify-content:space-between; align-items:center; gap:1rem; margin-bottom:1rem;">
          <h1 style="margin:0;">管理页面</h1>
          <div style="display:flex; gap:.5rem; flex-wrap:wrap;">
            <button class="btn" @click="handleLogout">退出登录</button>
            <RouterLink class="btn" to="/">返回首页</RouterLink>
          </div>
        </div>
        <div class="large-card" aria-label="账户与安全">
          <div class="title-wrapper">
            <h2>密码修改</h2>
          </div>
          <form id="changePwdForm" class="change-password" @submit.prevent="changePassword" novalidate>
            <div class="grid">
              <label>新密码
                <input type="password" v-model="new_password" autocomplete="new-password">
              </label>
              <label>确认新密码
                <input type="password" v-model="confirm_password" autocomplete="new-password">
              </label>
            </div>
            <div class="form-actions">
              <button class="btn primary" type="submit" @click="changePassword">修改密码</button>
              <button class="btn" type="reset">重置</button>
            </div>
          </form>
        </div>

        <!-- 导出按钮 -->
        <div class="export-section">
          <h2>数据导出</h2>
          <div style="display:flex; gap:.5rem; flex-wrap:wrap;">
            <button class="btn" @click="exportJson">导出JSON</button>
            <button class="btn" @click="exportMdZip">导出Markdown压缩包</button>
          </div>
        </div>

        <!-- 文章列表 -->
        <div class="posts-section">
          <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:1rem;">
            <h2>文章管理</h2>
            <button class="btn primary" @click="openCreateModal">新建文章</button>
          </div>

          <div v-if="loading" class="loading">加载中...</div>
          <div v-else-if="posts.length === 0" class="empty">暂无文章</div>
          <div v-else class="post-list">
            <div v-for="post in posts" :key="post.id" class="post-item large-card" :id="`post-${post.id}`">
              <div class="post-meta">
                <div class="post-kv">
                  <span class="k">ID</span>
                  <span class="v v-id future">{{ post.id }}</span>
                </div>
                <div class="post-kv">
                  <span class="k">作者</span>
                  <span class="v v-author">{{ post.author_name }}</span>
                </div>
                <div class="post-kv">
                  <span class="k">日期</span>
                  <span class="v v-date">{{ formatDate(post.date_posted) }}</span>
                </div>
                <div class="post-kv" style="grid-column:1/-1;">
                  <span class="k">标题</span>
                  <span class="v v-title">{{ post.title }}</span>
                </div>
                <div class="post-kv" style="grid-column:1/-1;">
                  <span class="k">摘要</span>
                  <span class="v v-summary">{{ post.brief_summary }}</span>
                </div>
                <div class="post-kv" style="grid-column:1/-1;">
                  <span class="k">备注</span>
                  <span class="v v-note">{{ post.note }}</span>
                </div>
              </div>
              <div class="post-actions">
                <button class="btn small" @click="editPost(post)">编辑</button>
                <button class="btn small" @click="downloadMarkdown(post.id)">下载MD</button>
                <a :href="`/blog/${post.id}/preview`" target="_blank" class="btn small">预览</a>
                <button class="btn small danger" @click="deletePost(post.id)">删除</button>
              </div>
            </div>
          </div>
        </div>

        <!-- 编辑弹窗 -->
        <div v-if="showEditModal" class="edit-mask" @click.self="closeEditModal">
          <div class="edit-panel">
            <div class="edit-head">
              <strong>{{ editingPost ? '编辑文章信息' : '新建文章' }}</strong>
              <button class="close-x" @click="closeEditModal">×</button>
            </div>
            <div class="edit-body">
              <form class="edit-grid" @submit.prevent="savePost">
                <label class="field">
                  标题
                  <input v-model="formData.title" type="text" />
                  <span class="hint">可选，为空则自动检测</span>
                </label>
                <label class="field">
                  作者
                  <input v-model="formData.author" type="text" />
                  <span class="hint">可选，为空则默认为YewFence</span>
                </label>
                <label class="field">
                  日期
                  <input v-model="formData.date" type="date" />
                </label>
                <label class="field" style="grid-column:1/-1;">
                  摘要
                  <textarea v-model="formData.summary" rows="3"></textarea>
                </label>
                <label class="field" style="grid-column:1/-1;">
                  备注
                  <textarea v-model="formData.note" rows="2"></textarea>
                  <span class="hint">可选，不对外显示</span>
                </label>
                <label class="field">
                  状态
                  <select v-model="formData.status">
                    <option value="published">公开</option>
                    <option value="hidden">隐藏</option>
                  </select>
                </label>
                <label class="field" style="grid-column:1/-1;">
                  上传 Markdown
                  <input type="file" accept=".md" @change="handleFileUpload" />
                  <span class="hint">选择 .md 文件后，会在保存时覆盖文章内容</span>
                </label>
              </form>
            </div>
            <div class="edit-foot">
              <button class="btn" @click="closeEditModal">取消</button>
              <button class="btn primary" @click="savePost" :disabled="saving">
                {{ saving ? '保存中...' : '保存' }}
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
import DefaultLayout from '../components/DefaultLayout.vue'
import { useAuthStore } from '../stores/auth'
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

const router = useRouter()
const authStore = useAuthStore()

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
    alert('加载文章失败')
  } finally {
    loading.value = false
  }
}

// 修改密码
const changePassword = async (event) => {
  const userName = sessionStorage.getItem('username') || 'yewfence'
  console.log('Changing password for user:', userName)
  const newPassword = new_password.value
  const confirmPassword = confirm_password.value
  if (!newPassword || !confirmPassword) {
    alert('请输入新密码和确认密码')
    return
  }

  if (newPassword !== confirmPassword) {
    alert('两次输入的密码不一致')
    return
  }

  try {
    const response = await apiUpdatePassword(userName, newPassword)
    if (response.error) {
      throw new Error(response.error)
    } else if (response.success === "true") {
      alert('密码修改成功，请重新登录')
    }
    await apiLogout()
    authStore.logout()
    router.push('/login')
  } catch (error) {
    console.error('密码修改失败:', error)
    alert('密码修改失败: ' + (error.response?.data?.error || error.message))
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
    const content = await file.text()
    formData.value.content = content
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
  if (!confirm('确定要删除这篇文章吗？此操作不可恢复。')) {
    return
  }

  try {
    await apiDeletePost(id)
    alert('文章删除成功')
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
    router.push('/login')
  } catch (error) {
    console.error('登出失败:', error)
  }
}

onMounted(async () => {
  const isAuth = await authStore.checkAuth()
  if (!isAuth) {
    router.push('/login')
  } else {
    loadPosts()
  }
})
</script>

<style>
@import '../assets/css/management.css';

.export-section {
  margin-bottom: 2rem;
  padding: 1rem;
  background: var(--surface-bg);
  border-radius: 8px;
}

.posts-section {
  margin-top: 2rem;
}

.post-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.post-item {
  padding: 1rem;
  background: var(--surface-bg);
  border-radius: 8px;
  border: 1px solid var(--color-border);
}

.post-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.5rem;
}

.post-header h3 {
  margin: 0;
}

.post-status {
  padding: 0.2rem 0.5rem;
  border-radius: 4px;
  font-size: 0.8rem;
}

.post-status.published {
  background: var(--color-success, #28a745);
  color: white;
}

.post-status.hidden {
  background: var(--color-muted, #6c757d);
  color: white;
}

.post-meta {
  color: var(--color-muted);
  font-size: 0.9rem;
  margin-bottom: 0.5rem;
}

.post-summary {
  margin: 0.5rem 0;
}

.post-actions {
  display: flex;
  gap: 0.5rem;
  flex-wrap: wrap;
  margin-top: 0.5rem;
}

.btn.small {
  padding: 0.3rem 0.6rem;
  font-size: 0.9rem;
}

.btn.danger {
  background: var(--color-danger, #dc3545);
  color: white;
}

.btn.danger:hover {
  background: var(--color-danger-dark, #c82333);
}
</style>
