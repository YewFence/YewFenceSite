import api from './config'

// 获取博客文章列表
export const getPosts = () => {
  return api.get('/api/blog')
}

// 获取单篇文章
export const getPost = (id) => {
  return api.get(`/api/blog/${id}`)
}

// 导出文章列表为JSON
export const exportPostsJson = () => {
  return api.get('/api/posts/export_json', {
    responseType: 'blob'
  })
}

// 导出文章为Markdown ZIP
export const exportPostsMdZip = () => {
  return api.get('/api/posts/export_md_zip', {
    responseType: 'blob'
  })
}

// 下载单篇文章的Markdown
export const downloadPostMarkdown = (id) => {
  return api.get(`/api/posts/${id}/md`, {
    responseType: 'blob'
  })
}

// 更新文章Markdown内容
export const updatePostMarkdown = (id, content) => {
  return api.post(`/api/posts/${id}/md`, content, {
    headers: {
      'Content-Type': 'text/plain'
    }
  })
}

// 预览文章
export const previewPost = (id) => {
  return api.get(`/api/blog/${id}/preview`)
}

// 创建文章
export const createPost = (formData) => {
  return api.post('/api/posts/new', formData, {
    headers: {
      'Content-Type': 'multipart/form-data'
    }
  })
}

// 编辑文章
export const editPost = (id, formData) => {
  return api.post(`/api/posts/${id}/edit`, formData, {
    headers: {
      'Content-Type': 'multipart/form-data'
    }
  })
}

// 删除文章
export const deletePost = (id) => {
  return api.get(`/api/posts/${id}/delete`)
}
