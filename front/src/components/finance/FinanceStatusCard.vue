<template>
    <div class="bg-white rounded-lg shadow-lg p-6">
      <h2 class="text-2xl font-semibold mb-6">재무상태 분석</h2>
      
      <!-- 점수 표시 -->
      <div class="flex items-center justify-center mb-8">
        <div class="relative">
          <svg class="w-32 h-32">
            <circle
              class="text-gray-200"
              stroke-width="10"
              stroke="currentColor"
              fill="transparent"
              r="58"
              cx="64"
              cy="64"
            />
            <circle
              class="text-blue-500"
              stroke-width="10"
              :stroke-dasharray="circumference"
              :stroke-dashoffset="dashOffset"
              stroke-linecap="round"
              stroke="currentColor"
              fill="transparent"
              r="58"
              cx="64"
              cy="64"
            />
          </svg>
          <span class="absolute inset-0 flex items-center justify-center text-2xl font-bold">
            {{ Math.round(statusData.asset_health_score) }}점
          </span>
        </div>
      </div>
  
      <!-- 상세 정보 -->
      <div class="grid md:grid-cols-2 gap-6">
        <div class="space-y-4">
          <div class="bg-gray-50 p-4 rounded-lg">
            <h3 class="text-sm font-medium text-gray-500">연령대</h3>
            <p class="text-lg font-semibold">{{ statusData.age_group }}</p>
          </div>
          <div class="bg-gray-50 p-4 rounded-lg">
            <h3 class="text-sm font-medium text-gray-500">연 소득</h3>
            <p class="text-lg font-semibold">{{ formatCurrency(statusData.annual_income) }}</p>
          </div>
        </div>
        
        <div class="space-y-4">
          <div class="bg-gray-50 p-4 rounded-lg">
            <h3 class="text-sm font-medium text-gray-500">총 자산</h3>
            <p class="text-lg font-semibold">{{ formatCurrency(statusData.user_asset) }}</p>
          </div>
          <div class="bg-gray-50 p-4 rounded-lg">
            <h3 class="text-sm font-medium text-gray-500">추천 월 저축액</h3>
            <p class="text-lg font-semibold">{{ formatCurrency(statusData.recommended_monthly_saving) }}</p>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script setup>
  import { computed } from 'vue'
  
  const props = defineProps({
    statusData: {
      type: Object,
      required: true
    }
  })
  
  const circumference = computed(() => 2 * Math.PI * 58)
  const dashOffset = computed(() => 
    circumference.value - (props.statusData.asset_health_score / 100) * circumference.value
  )
  
  const formatCurrency = (value) => {
    return new Intl.NumberFormat('ko-KR', {
      style: 'currency',
      currency: 'KRW'
    }).format(value * 10000) // 만원 단위를 원 단위로 변환
  }
  </script>