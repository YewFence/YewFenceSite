import api from './config'

// 登录
export const login = (username, password) => {
  const formData = new FormData()
  formData.append('username', username)
  formData.append('password', password)

  return api.post('/login', formData, {
    headers: {
      'Content-Type': 'multipart/form-data'
    }
  })
}

// 登出
export const logout = () => {
  return api.get('/logout')
}

// 获取管理页面数据
export const getManagementData = () => {
  return api.get('/management')
}
