import { defineStore } from 'pinia'
import { ref } from 'vue'

export const tempDataStore = defineStore('tempData', () => {
  // 1. 准备一个 "中转站" ref
  const message = ref('')
  const data = ref(null)

  // 2. "发送方" 调用的 Action
  function setDataForNextPage(messageText, dataObject) {
    message.value = messageText
    data.value = dataObject
  }
  
  // 3. "接收方" 调用的 Action (用完就清空，防止下次还读到)
  function clearData() {
    message.value = ''
    data.value = null
  }

  return { message, data, setDataForNextPage, clearData }
})