<script setup>
import { ref } from 'vue'
import { MessageCircle, X, Send } from 'lucide-vue-next'

const isOpen = ref(false)
const message = ref('')
const chatMessages = ref([])
const loading = ref(false)

const toggleChat = () => {
  isOpen.value = !isOpen.value
}

const sendMessage = async () => {
  if (!message.value.trim()) return
  
  // 사용자 메시지 추가
  chatMessages.value.push({
    type: 'user',
    content: message.value
  })
  
  const userMessage = message.value
  message.value = ''
  loading.value = true

  try {
    // 백엔드 서버로 요청 보내기
    const response = await fetch('http://localhost:3000/api/chat', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        message: userMessage
      })
    })

    if (!response.ok) {
      throw new Error('API 요청이 실패했습니다.')
    }

    const data = await response.json()
    
    // 봇 응답 추가
    chatMessages.value.push({
      type: 'bot',
      content: data.message
    })
  } catch (error) {
    console.error('Error:', error)
    chatMessages.value.push({
      type: 'bot',
      content: '죄송합니다. 오류가 발생했습니다. 다시 시도해주세요.'
    })
  }
  
  loading.value = false
}
</script>

<!-- 나머지 템플릿과 스타일 코드는 동일 -->

<template>
  <div class="chat-container">
    <!-- 채팅 버튼 -->
    <button 
      @click="toggleChat" 
      class="chat-button"
      :class="{ 'open': isOpen }"
    >
      <MessageCircle v-if="!isOpen" />
      <X v-else />
    </button>

    <!-- 채팅창 -->
    <div class="chat-window" :class="{ 'open': isOpen }">
      <div class="chat-header">
        <h3>Chat Assistant</h3>
      </div>
      
      <div class="chat-messages" ref="messageContainer">
        <div 
          v-for="(msg, index) in chatMessages" 
          :key="index"
          class="message"
          :class="msg.type"
        >
          {{ msg.content }}
        </div>
      </div>

      <div class="chat-input">
        <input
          v-model="message"
          @keyup.enter="sendMessage"
          placeholder="메시지를 입력하세요..."
          :disabled="loading"
        />
        <button 
          @click="sendMessage"
          :disabled="loading || !message.trim()"
        >
          <Send />
        </button>
      </div>
    </div>
  </div>
</template>

<style scoped>
.chat-container {
  position: fixed;
  bottom: 20px;
  right: 20px;
  z-index: 1000;
}

.chat-button {
  width: 50px;
  height: 50px;
  border-radius: 50%;
  background-color: #007bff;
  border: none;
  color: white;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 2px 10px rgba(0,0,0,0.2);
  transition: all 0.3s ease;
}

.chat-button:hover {
  background-color: #0056b3;
  transform: scale(1.1);
}

.chat-window {
  position: absolute;
  bottom: 70px;
  right: 0;
  width: 300px;
  height: 400px;
  background-color: white;
  border-radius: 10px;
  box-shadow: 0 5px 15px rgba(0,0,0,0.2);
  display: flex;
  flex-direction: column;
  display: none;
}

.chat-window.open {
  display: flex;
}

.chat-header {
  padding: 15px;
  background-color: #007bff;
  color: white;
  border-radius: 10px 10px 0 0;
}

.chat-header h3 {
  margin: 0;
  font-size: 16px;
}

.chat-messages {
  flex: 1;
  padding: 15px;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.message {
  padding: 8px 12px;
  border-radius: 15px;
  max-width: 80%;
  word-break: break-word;
}

.message.user {
  background-color: #007bff;
  color: white;
  align-self: flex-end;
}

.message.bot {
  background-color: #f1f3f5;
  color: black;
  align-self: flex-start;
}

.chat-input {
  padding: 15px;
  display: flex;
  gap: 10px;
  border-top: 1px solid #eee;
}

.chat-input input {
  flex: 1;
  padding: 8px 12px;
  border: 1px solid #ddd;
  border-radius: 20px;
  outline: none;
}

.chat-input button {
  padding: 8px;
  background-color: #007bff;
  border: none;
  border-radius: 50%;
  color: white;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
}

.chat-input button:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}
</style>