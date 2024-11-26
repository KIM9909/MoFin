<template>
  <div class="dashboard-container">
    <div v-if="authStore.isLogin">
      <!-- 필수 정보 입력 알림 -->
      <div v-if="!hasRequiredInfo" class="info-alert">
        <p class="alert-title">정보 필요</p>
        <p class="alert-message">재무상태 분석을 위해 프로필 정보를 완성해주세요.</p>
        <router-link to="/profile" class="alert-link">
          프로필 수정하기
        </router-link>
      </div>

      <!-- 메인 대시보드 영역 -->
      <div v-else-if="recommendationStore.financeStatus" class="dashboard-grid">
        <!-- 전체 너비를 차지하는 재무상태 카드 -->
        <div class="full-width-card">
          <FinanceStatusCard 
            :status-data="recommendationStore.financeStatus" 
            class="card-hover-effect"
          />
        </div>

        <!-- 2열 그리드로 배치되는 카드들 -->
        <div class="card-hover-effect">
          <AssetComparison 
            :status-data="recommendationStore.financeStatus"
          />
        </div>
        <div class="card-hover-effect">
          <SavingPotential 
            :status-data="recommendationStore.financeStatus"
          />
        </div>
      </div>

      <!-- 로딩 상태 -->
      <div v-else-if="recommendationStore.loading" class="loading-container">
        <div class="loading-content">
          <div class="loading-spinner"></div>
          <p class="loading-text">재무상태 정보를 불러오는 중...</p>
        </div>
      </div>
    </div>

    <!-- 로그인하지 않은 상태 -->
    <div v-else class="login-prompt">
      <p class="prompt-text">
        재무상태 분석을 위해서는 로그인이 필요합니다.
      </p>
      <router-link to="/signin" class="login-button">
        로그인하기
      </router-link>
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useRecommendationStore } from '@/stores/recommendation'
import FinanceStatusCard from '@/components/finance/FinanceStatusCard.vue'
import AssetComparison from '@/components/finance/AssetComparison.vue'
import SavingPotential from '@/components/finance/SavingPotential.vue'

const authStore = useAuthStore()
const recommendationStore = useRecommendationStore()

const hasRequiredInfo = computed(() => {
  const userDetails = authStore.userDetails
  return userDetails?.birth && userDetails?.annual_income && userDetails?.total_assets
})

onMounted(async () => {
  if (authStore.isLogin && hasRequiredInfo.value) {
    try {
      await recommendationStore.fetchFinanceStatus()
      console.log('재무상태 데이터 로드됨:', recommendationStore.financeStatus)
    } catch (error) {
      console.error('재무상태 정보 로드 실패:', error)
    }
  }
})
</script>

<style scoped>
.dashboard-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 32px 16px;
}

.info-alert {
  background: linear-gradient(to right, #fef3c7, #fef9c3);
  border-left: 4px solid #f59e0b;
  padding: 20px;
  margin-bottom: 24px;
  border-radius: 0 12px 12px 0;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}

.alert-title {
  font-weight: 600;
  color: #92400e;
  margin-bottom: 8px;
}

.alert-message {
  color: #92400e;
  margin-bottom: 12px;
}

.alert-link {
  display: inline-block;
  color: #2563eb;
  text-decoration: none;
  font-weight: 500;
  padding: 4px 0;
  border-bottom: 1px solid transparent;
  transition: all 0.3s ease;
}

.alert-link:hover {
  color: #1d4ed8;
  border-bottom-color: currentColor;
}

.dashboard-grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: 24px;
}

@media (min-width: 1024px) {
  .dashboard-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

.full-width-card {
  grid-column: 1 / -1;
}

.card-hover-effect {
  transition: all 0.3s ease;
}

.card-hover-effect:hover {
  transform: translateY(-4px);
}

.loading-container {
  min-height: 400px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.loading-content {
  text-align: center;
}

.loading-spinner {
  width: 48px;
  height: 48px;
  border: 3px solid #e5e7eb;
  border-radius: 50%;
  border-top-color: #3b82f6;
  margin: 0 auto 16px;
  animation: spin 1s linear infinite;
}

.loading-text {
  color: #6b7280;
  font-size: 16px;
}

.login-prompt {
  min-height: 400px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  background: white;
  border-radius: 16px;
  padding: 32px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
}

.prompt-text {
  font-size: 20px;
  color: #4b5563;
  margin-bottom: 24px;
  text-align: center;
}

.login-button {
  background: linear-gradient(to right, #3b82f6, #2563eb);
  color: white;
  font-weight: 600;
  padding: 12px 32px;
  border-radius: 12px;
  text-decoration: none;
  transition: all 0.3s ease;
  box-shadow: 0 4px 6px rgba(59, 130, 246, 0.2);
}

.login-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 8px rgba(59, 130, 246, 0.3);
  background: linear-gradient(to right, #2563eb, #1d4ed8);
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

/* 반응형 조정 */
@media (max-width: 640px) {
  .dashboard-container {
    padding: 16px;
  }

  .login-prompt {
    padding: 24px;
    margin: 0 16px;
  }

  .prompt-text {
    font-size: 18px;
  }

  .login-button {
    width: 100%;
    text-align: center;
  }
}
</style>