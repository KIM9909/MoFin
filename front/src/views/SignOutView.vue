<template>
  <div class="logout-container">
    <div class="logout-card">
      <!-- 로고나 아이콘 -->
      <div class="logout-icon">👋</div>
      
      <h1 class="title">로그아웃이 완료되었습니다.</h1>
      <h2 class="subtitle">다음에 또 이용해주세요</h2>
      
      <!-- 프로그레스 바와 카운트다운 -->
      <div class="redirect-info">
        <div class="progress-bar">
          <div class="progress" :style="{ width: progressWidth + '%' }"></div>
        </div>
        <p class="redirect-text">{{ countdown }}초 후 메인 페이지로 이동합니다.</p>
      </div>

      <!-- 즉시 이동 버튼 -->
      <button @click="goHome" class="home-button">
        메인으로 바로가기
      </button>
    </div>
  </div>
</template>

<script setup>
import { useAuthStore } from '@/stores/auth'
import { useRouter } from 'vue-router'
import { onMounted, ref, onUnmounted } from 'vue'

const authStore = useAuthStore()
const router = useRouter()

// 카운트다운과 프로그레스 바를 위한 상태
const countdown = ref(3)
const progressWidth = ref(100)
let timer

onMounted(() => {
  authStore.logout()
  
  // 카운트다운과 프로그레스 바 업데이트
  timer = setInterval(() => {
    countdown.value--
    progressWidth.value = (countdown.value / 3) * 100
    
    if (countdown.value <= 0) {
      clearInterval(timer)
      router.push({ name: 'home' })
    }
  }, 1000)
})

onUnmounted(() => {
  if (timer) clearInterval(timer)
})

// 즉시 홈으로 이동하는 함수
const goHome = () => {
  clearInterval(timer)
  router.push({ name: 'home' })
}
</script>

<style scoped>
.logout-container {
  min-height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  background-color: #f5f5f5;
  padding: 20px;
}

.logout-card {
  background: white;
  padding: 40px;
  border-radius: 20px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  text-align: center;
  max-width: 400px;
  width: 100%;
  animation: slideUp 0.5s ease-out;
}

.logout-icon {
  font-size: 48px;
  margin-bottom: 20px;
  animation: wave 1s infinite;
}

.title {
  color: #2c662f;
  font-size: 1.8rem;
  margin-bottom: 10px;
}

.subtitle {
  color: #666;
  font-size: 1.2rem;
  margin-bottom: 30px;
  font-weight: normal;
}

.redirect-info {
  margin: 30px 0;
}

.progress-bar {
  width: 100%;
  height: 4px;
  background-color: #eee;
  border-radius: 2px;
  overflow: hidden;
  margin-bottom: 15px;
}

.progress {
  height: 100%;
  background-color: #2c662f;
  transition: width 0.3s linear;
}

.redirect-text {
  color: #666;
  font-size: 0.9rem;
}

.home-button {
  background-color: #2c662f;
  color: white;
  border: none;
  padding: 12px 24px;
  border-radius: 8px;
  cursor: pointer;
  font-size: 1rem;
  transition: background-color 0.3s;
}

.home-button:hover {
  background-color: #235024;
}

/* 애니메이션 */
@keyframes slideUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes wave {
  0% { transform: rotate(0deg); }
  25% { transform: rotate(-10deg); }
  75% { transform: rotate(10deg); }
  100% { transform: rotate(0deg); }
}

/* 반응형 디자인 */
@media (max-width: 480px) {
  .logout-card {
    padding: 30px 20px;
  }

  .title {
    font-size: 1.5rem;
  }

  .subtitle {
    font-size: 1rem;
  }
}
</style>