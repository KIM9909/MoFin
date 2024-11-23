<template>
    <div class="container mx-auto px-4 py-8">
      <div v-if="authStore.isLogin">
        <div v-if="!hasRequiredInfo" class="bg-yellow-100 border-l-4 border-yellow-500 text-yellow-700 p-4 mb-4">
          <p class="font-bold">정보 필요</p>
          <p>재무상태 분석을 위해 프로필 정보를 완성해주세요.</p>
          <router-link 
            to="/profile" 
            class="text-blue-600 hover:text-blue-800 underline"
          >
            프로필 수정하기
          </router-link>
        </div>
  
        <div v-else-if="recommendationStore.financeStatus" class="space-y-6">
          <FinanceStatusCard :status-data="recommendationStore.financeStatus" />
          <AssetComparison :status-data="recommendationStore.financeStatus" />
          <SavingPotential :status-data="recommendationStore.financeStatus" />
        </div>
  
        <div v-else-if="recommendationStore.loading" class="text-center py-8">
          <p class="text-gray-600">재무상태 정보를 불러오는 중...</p>
        </div>
      </div>
      <div v-else>
        <p class="text-center py-8">
          재무상태 분석을 위해서는 로그인이 필요합니다.
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