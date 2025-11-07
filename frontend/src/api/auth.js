import api from './config'

// 登录
export const login = (username, password) => {
  const formData = new FormData()
  formData.append('username', username)
  formData.append('password', password)

  return api.post('/api/auth/login', formData, {
    headers: {
      'Content-Type': 'multipart/form-data'
    }
  })
}

export const updatePassword = (userName, newPassword) => {
  const formData = new FormData()
  formData.append('username', userName)
  formData.append('new_password', newPassword)

  return api.post('/api/auth/change_password', formData, {
    headers: {
      'Content-Type': 'multipart/form-data'
    }
  })
}

// 登出
export const logout = () => {
  return api.get('/api/auth/logout')
}

// 获取管理页面数据
export const getManagementData = () => {
  return api.get('/api/management/posts')
}
