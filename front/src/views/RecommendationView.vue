<template>
  <div class="recommendations-container">
    <div v-if="authStore.isLogin">
      <div v-if="!hasRequiredInfo" class="info-alert">
        <p class="alert-title">정보 필요</p>
        <p class="alert-message">맞춤형 추천을 위해 프로필 정보를 완성해주세요.</p>
        <router-link to="/profile" class="alert-link">
          프로필 수정하기
        </router-link>
      </div>

      <div v-else>
        <!-- 로딩 상태 -->
        <div v-if="recommendationStore.loading" class="loading-state">
          <div class="loading-spinner"></div>
          <p class="loading-text">추천 정보를 불러오는 중...</p>
        </div>

        <!-- 에러 상태 -->
        <div v-else-if="recommendationStore.error" class="error-alert">
          <p>{{ recommendationStore.error }}</p>
        </div>

        <!-- 추천 정보 표시 -->
        <div v-else-if="recommendationStore.recommendations" class="recommendations-content">
          <!-- 생애주기 정보 -->
          <div class="section-wrapper">
            <ProductSection
              :title="'생애주기 맞춤 추천'"
              :description="recommendationStore.recommendations.life_cycle.description"
              :cycle-info="recommendationStore.recommendations.life_cycle"
            />
          </div>

          <!-- 소득 수준별 추천 -->
          <div class="section-wrapper">
            <IncomeSection
              :income-info="recommendationStore.recommendations.income_level"
              :investment-suggestion="recommendationStore.recommendations.investment_suggestion"
              :status-data="recommendationStore.financeStatus"
            />
          </div>

          <!-- 추천 예금상품 -->
          <div class="section-wrapper">
            <RecommendedProducts
              title="추천 예금상품"
              :products="recommendationStore.recommendations.recommended_deposits"
              product-type="deposit"
            />
          </div>

          <!-- 추천 적금상품 -->
          <div class="section-wrapper">
            <RecommendedProducts
              title="추천 적금상품"
              :products="recommendationStore.recommendations.recommended_savings"
              product-type="savings"
            />
          </div>
        </div>
      </div>
    </div>
    <div v-else class="login-prompt">
      <p class="prompt-message">
        추천 서비스를 이용하기 위해서는 로그인이 필요합니다.
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
  import ProductSection from '@/components/recommendations/ProductSection.vue'
  import IncomeSection from '@/components/recommendations/IncomeSection.vue'
  import RecommendedProducts from '@/components/recommendations/RecommendedProducts.vue'
  
  const authStore = useAuthStore()
  const recommendationStore = useRecommendationStore()
  
  const hasRequiredInfo = computed(() => {
    const userInfo = authStore.userDetails
    return userInfo?.birth && userInfo?.annual_income && userInfo?.total_assets
  })
  
  onMounted(async () => {
    if (authStore.isLogin && hasRequiredInfo.value) {
      try {
        await recommendationStore.fetchRecommendations()
      } catch (error) {
        console.error('추천 정보 로드 실패:', error)
      }
    }
  })
  </script>

<style scoped>
.recommendations-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 32px 16px;
}

.info-alert {
  background: linear-gradient(135deg, #fff7ed, #ffedd5);
  border-left: 4px solid #f97316;
  padding: 20px;
  margin-bottom: 24px;
  border-radius: 0 12px 12px 0;
  box-shadow: 0 2px 8px rgba(249, 115, 22, 0.1);
}

.alert-title {
  font-weight: 600;
  color: #9a3412;
  margin-bottom: 8px;
  font-size: 16px;
}

.alert-message {
  color: #9a3412;
  margin-bottom: 12px;
  font-size: 14px;
}

.alert-link {
  color: #2563eb;
  text-decoration: none;
  font-weight: 500;
  font-size: 14px;
  padding-bottom: 2px;
  border-bottom: 1px solid transparent;
  transition: all 0.3s ease;
}

.alert-link:hover {
  color: #1d4ed8;
  border-bottom-color: currentColor;
}

.loading-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 48px 0;
}

.loading-spinner {
  width: 40px;
  height: 40px;
  border: 3px solid #e5e7eb;
  border-radius: 50%;
  border-top-color: #3b82f6;
  animation: spin 1s linear infinite;
  margin-bottom: 16px;
}

.loading-text {
  color: #6b7280;
  font-size: 16px;
}

.error-alert {
  background: linear-gradient(135deg, #fee2e2, #fecaca);
  border-left: 4px solid #ef4444;
  padding: 20px;
  margin-bottom: 24px;
  border-radius: 0 12px 12px 0;
  color: #991b1b;
}

.recommendations-content {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.section-wrapper {
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.section-wrapper:hover {
  transform: translateY(-4px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
}

.login-prompt {
  text-align: center;
  padding: 48px 20px;
  background: white;
  border-radius: 16px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
}

.prompt-message {
  color: #4b5563;
  font-size: 18px;
  margin-bottom: 24px;
}

.login-button {
  display: inline-block;
  background: linear-gradient(135deg, #3b82f6, #2563eb);
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
  background: linear-gradient(135deg, #2563eb, #1d4ed8);
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

/* 반응형 조정 */
@media (max-width: 768px) {
  .recommendations-container {
    padding: 16px;
  }

  .section-wrapper {
    margin-bottom: 16px;
  }

  .login-prompt {
    margin: 0 16px;
    padding: 32px 16px;
  }

  .prompt-message {
    font-size: 16px;
  }

  .login-button {
    width: 100%;
    text-align: center;
  }
}
</style>