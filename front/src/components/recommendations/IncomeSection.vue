<template>
    <div class="bg-white rounded-lg shadow-lg p-6 mb-6">
      <h2 class="text-2xl font-semibold mb-4">소득 기반 맞춤 추천</h2>
  
      <!-- 소득 수준 정보 -->
      <div class="bg-green-50 rounded-lg p-4 mb-4">
        <div class="flex items-center justify-between mb-4">
          <span class="text-lg font-medium text-green-800">
            소득 수준: {{ incomeInfo.level }}
          </span>
        </div>
      </div>
  
      <!-- 투자 제안 -->
      <div class="grid md:grid-cols-2 gap-4">
        <!-- 월 저축 추천 -->
        <div class="bg-gray-50 rounded-lg p-4">
          <h3 class="font-medium text-gray-800 mb-2">월 저축 추천 금액</h3>
          <div class="text-2xl font-bold text-green-600">
            {{ formatCurrency(investmentSuggestion.monthly_savings) }}
          </div>
          <p class="text-sm text-gray-600 mt-1">
            연간 추천 저축액: {{ formatCurrency(investmentSuggestion.monthly_savings * 12) }}
          </p>
        </div>
  
        <!-- 자산 배분 추천 -->
        <div class="bg-gray-50 rounded-lg p-4">
          <h3 class="font-medium text-gray-800 mb-2">추천 자산 배분</h3>
          <div class="flex items-center space-x-4">
            <div class="flex-1">
              <div class="h-4 bg-gray-200 rounded">
                <div 
                  class="h-4 bg-blue-500 rounded"
                  :style="{ width: `${investmentSuggestion.deposit_ratio * 100}%` }"
                ></div>
              </div>
              <div class="flex justify-between mt-1 text-sm">
                <span>예금: {{ (investmentSuggestion.deposit_ratio * 100).toFixed(0) }}%</span>
                <span>적금: {{ (investmentSuggestion.savings_ratio * 100).toFixed(0) }}%</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script setup>
  import { defineProps } from 'vue'
  
  const props = defineProps({
    incomeInfo: {
      type: Object,
      required: true
    },
    investmentSuggestion: {
      type: Object,
      required: true
    }
  })
  
  const formatCurrency = (value) => {
    return new Intl.NumberFormat('ko-KR', {
      style: 'currency',
      currency: 'KRW'
    }).format(value * 10000) // 만원 단위를 원 단위로 변환
  }
  </script>