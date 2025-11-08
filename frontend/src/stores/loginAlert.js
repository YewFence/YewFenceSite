import { defineStore } from 'pinia'
import { ref } from 'vue'

export const loginAlertStore = defineStore('loginAlert', () => {
  // 1. 准备一个 "中转站" ref
  const messageText = ref('')
  const messageType = ref('')

  // 2. "发送方" 调用的 Action
  function setInfoForLoginPage(Type='info', Text) {
    messageType.value = Type
    messageText.value = Text
  }
  
  // 3. "接收方" 调用的 Action (用完就清空，防止下次还读到)
  function clearInfo() {
    messageType.value = null
    messageText.value = null
  }

  return { messageType, messageText, setInfoForLoginPage, clearInfo }
})