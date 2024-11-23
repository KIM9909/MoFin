<script setup>
import { ref, onMounted, nextTick } from 'vue'
import { MessageCircle, X, Send } from 'lucide-vue-next'

const isOpen = ref(false)
const message = ref('')
const chatMessages = ref([])
const loading = ref(false)
const messageContainer = ref(null)

const toggleChat = () => {
  isOpen.value = !isOpen.value
  if (isOpen.value && chatMessages.value.length === 0) {
    // 초기 웰컴 메시지
    chatMessages.value.push({
      type: 'bot',
      content: '안녕하세요! 저는 달콤한 금융 정보를 알려주는 MoFin이에요! 무엇을 도와드릴까요? 😊'
    })
  }
}

// 메시지 자동 스크롤
const scrollToBottom = async () => {
  await nextTick()
  if (messageContainer.value) {
    messageContainer.value.scrollTop = messageContainer.value.scrollHeight
  }
}

const sendMessage = async () => {
  if (!message.value.trim()) return
  
  chatMessages.value.push({
    type: 'user',
    content: message.value
  })
  
  const userMessage = message.value
  message.value = ''
  loading.value = true
  
  scrollToBottom()

  try {
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
    
    if (loading.value) {
      chatMessages.value.push({
        type: 'bot',
        content: data.message
      })
      scrollToBottom()
    }
  } catch (error) {
    console.error('Error:', error)
    chatMessages.value.push({
      type: 'bot',
      content: '앗! 제가 실수를 했네요 🥺 다시 한 번 말씀해 주시겠어요?'
    })
  }
  
  loading.value = false
}

// 로딩 중일 때 머핀이 움직이는 효과
const loadingDots = ref('...')
let loadingInterval

onMounted(() => {
  setInterval(() => {
    loadingDots.value = loadingDots.value.length >= 3 ? '' : loadingDots.value + '.'
  }, 500)
})
</script>

<template>
  <div class="chat-container">
    <!-- 채팅 버튼 -->
    <button 
      @click="toggleChat" 
      class="chat-button"
      :class="{ 'open': isOpen }"
    >
      <div class="muffin-icon" v-if="!isOpen">🧁</div>
      <X v-else />
    </button>

    <!-- 채팅창 -->
    <div class="chat-window" :class="{ 'open': isOpen }">
      <div class="chat-header">
        <div class="header-content">
          <div class="muffin-avatar"></div>
          <h3>MoFin</h3>
        </div>
      </div>
      
      <div class="chat-messages" ref="messageContainer">
        <div 
          v-for="(msg, index) in chatMessages" 
          :key="index"
          class="message"
          :class="msg.type"
        >
          <div v-if="msg.type === 'bot'" class="bot-message-container">
            <div class="mini-muffin"></div>
            <div class="message-content">{{ msg.content }}</div>
          </div>
          <div v-else class="message-content">{{ msg.content }}</div>
        </div>
        <div v-if="loading" class="message bot">
          <div class="bot-message-container">
            <div class="mini-muffin"></div>
            <div class="message-content loading-animation">
              MoFin이 생각중{{ loadingDots }}
            </div>
          </div>
        </div>
      </div>

      <div class="chat-input">
        <input
          v-model="message"
          @keyup.enter="sendMessage"
          placeholder="MoFin에게 물어보세요!"
          :disabled="loading"
        />
        <button 
          @click="sendMessage"
          :disabled="loading || !message.trim()"
          class="send-button"
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
  font-family: 'Pretendard', sans-serif;
}

.chat-button {
  width: 60px;
  height: 60px;
  border-radius: 50%;
  background-color: #FFB067;
  border: none;
  color: white;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 4px 15px rgba(255, 176, 103, 0.4);
  transition: all 0.3s ease;
}

.muffin-icon {
  font-size: 30px;
  animation: bounce 2s infinite;
}

.chat-button:hover {
  background-color: #FF9240;
  transform: scale(1.1);
}

.chat-window {
  position: absolute;
  bottom: 80px;
  right: 0;
  width: 320px;
  height: 500px;
  background-color: #FFF9F5;
  border-radius: 20px;
  box-shadow: 0 5px 25px rgba(255, 176, 103, 0.3);
  display: none;
  overflow: hidden;
}

.chat-window.open {
  display: flex;
  flex-direction: column;
  animation: slideIn 0.3s ease;
}

.chat-header {
  padding: 15px;
  background: linear-gradient(135deg, #FFB067 0%, #FF9240 100%);
  color: white;
}

.header-content {
  display: flex;
  align-items: center;
  gap: 10px;
}

.muffin-avatar {
  font-size: 24px;
  animation: bounce 2s infinite;
}

.chat-header h3 {
  margin: 0;
  font-size: 18px;
  font-weight: 600;
}

.chat-messages {
  flex: 1;
  padding: 20px;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  gap: 12px;
  background: url("data:image/svg+xml,%3Csvg width='52' height='26' viewBox='0 0 52 26' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cg fill='%23FFB067' fill-opacity='0.1'%3E%3Cpath d='M10 10c0-2.21-1.79-4-4-4-3.314 0-6-2.686-6-6h2c0 2.21 1.79 4 4 4 3.314 0 6 2.686 6 6 0 2.21 1.79 4 4 4 3.314 0 6 2.686 6 6 0 2.21 1.79 4 4 4v2c-3.314 0-6-2.686-6-6 0-2.21-1.79-4-4-4-3.314 0-6-2.686-6-6zm25.464-1.95l8.486 8.486-1.414 1.414-8.486-8.486 1.414-1.414z' /%3E%3C/g%3E%3C/g%3E%3C/svg%3E");
}

.bot-message-container {
  display: flex;
  align-items: flex-start;
  gap: 8px;
}

.mini-muffin {
  font-size: 16px;
  margin-top: 2px;
}

.message {
  padding: 10px 15px;
  border-radius: 18px;
  max-width: 85%;
  word-break: break-word;
  line-height: 1.4;
}

.message.user {
  background: linear-gradient(135deg, #FFB067 0%, #FF9240 100%);
  color: white;
  align-self: flex-end;
  border-bottom-right-radius: 5px;
}

.message.bot {
  background-color: white;
  color: #333;
  align-self: flex-start;
  border-bottom-left-radius: 5px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
}

.loading-animation {
  color: #666;
  font-style: italic;
}

.chat-input {
  padding: 15px;
  display: flex;
  gap: 10px;
  background-color: white;
  border-top: 1px solid rgba(255, 176, 103, 0.2);
}

.chat-input input {
  flex: 1;
  padding: 12px 18px;
  border: 2px solid rgba(255, 176, 103, 0.3);
  border-radius: 25px;
  outline: none;
  transition: all 0.3s ease;
  font-size: 14px;
}

.chat-input input:focus {
  border-color: #FFB067;
  box-shadow: 0 0 0 3px rgba(255, 176, 103, 0.2);
}

.send-button {
  width: 45px;
  height: 45px;
  background: linear-gradient(135deg, #FFB067 0%, #FF9240 100%);
  border: none;
  border-radius: 50%;
  color: white;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s ease;
}

.send-button:hover:not(:disabled) {
  transform: scale(1.1);
}

.send-button:disabled {
  background: #E0E0E0;
  cursor: not-allowed;
}

@keyframes bounce {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-5px); }
}

@keyframes slideIn {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* 스크롤바 스타일링 */
.chat-messages::-webkit-scrollbar {
  width: 6px;
}

.chat-messages::-webkit-scrollbar-track {
  background: rgba(255, 176, 103, 0.1);
}

.chat-messages::-webkit-scrollbar-thumb {
  background: rgba(255, 176, 103, 0.3);
  border-radius: 3px;
}

.chat-messages::-webkit-scrollbar-thumb:hover {
  background: rgba(255, 176, 103, 0.5);
}
</style>