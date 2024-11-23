<template>
    <div class="container mx-auto px-4 py-8">
      <div v-if="authStore.isLogin">
        <div v-if="!hasRequiredInfo" class="bg-yellow-100 border-l-4 border-yellow-500 text-yellow-700 p-4 mb-4">
          <p class="font-bold">정보 필요</p>
          <p>맞춤형 추천을 위해 프로필 정보를 완성해주세요.</p>
          <router-link 
            to="/profile" 
            class="text-blue-600 hover:text-blue-800 underline"
          >
            프로필 수정하기
          </router-link>
        </div>
  
        <div v-else>
          <!-- 로딩 상태 -->
          <div v-if="recommendationStore.loading" class="text-center py-8">
            <p class="text-gray-600">추천 정보를 불러오는 중...</p>
          </div>
  
          <!-- 에러 상태 -->
          <div v-else-if="recommendationStore.error" class="bg-red-100 border-l-4 border-red-500 text-red-700 p-4">
            <p>{{ recommendationStore.error }}</p>
          </div>
  
          <!-- 추천 정보 표시 -->
          <div v-else-if="recommendationStore.recommendations" class="space-y-6">
            <!-- 생애주기 정보 -->
            <ProductSection
              :title="'생애주기 맞춤 추천'"
              :description="recommendationStore.recommendations.life_cycle.description"
              :cycle-info="recommendationStore.recommendations.life_cycle"
            />
  
            <!-- 소득 수준별 추천 -->
            <IncomeSection
              :income-info="recommendationStore.recommendations.income_level"
              :investment-suggestion="recommendationStore.recommendations.investment_suggestion"
            />
  
            <!-- 추천 예금상품 -->
            <RecommendedProducts
              title="추천 예금상품"
              :products="recommendationStore.recommendations.recommended_deposits"
              product-type="deposit"
            />
  
            <!-- 추천 적금상품 -->
            <RecommendedProducts
              title="추천 적금상품"
              :products="recommendationStore.recommendations.recommended_savings"
              product-type="savings"
            />
          </div>
        </div>
      </div>
      <div v-else>
        <p class="text-center py-8">
          추천 서비스를 이용하기 위해서는 로그인이 필요합니다.
        </p>
        <div class="text-center">
          <router-link
            to="/signin"
            class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"
          >
            로그인하기
          </router-link>
        </div>
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