<template>
    <div class="bg-white rounded-lg shadow-lg p-6 mb-6">
      <h2 class="text-2xl font-semibold mb-4">{{ title }}</h2>
      
      <!-- 생애주기 정보 카드 -->
      <div class="bg-blue-50 rounded-lg p-4 mb-4">
        <div class="flex items-center mb-2">
          <span class="text-lg font-medium text-blue-800">
            현재 생애주기: {{ cycleInfo.cycle }}
          </span>
        </div>
        <p class="text-gray-700 mb-4">{{ description }}</p>
      </div>
  
      <!-- 추천 전략 -->
      <div class="grid md:grid-cols-2 gap-4">
        <!-- 예금 추천 전략 -->
        <div class="bg-gray-50 rounded-lg p-4">
          <h3 class="font-medium text-gray-800 mb-2">예금 상품 전략</h3>
          <ul class="list-disc list-inside text-gray-600">
            <li v-for="(priority, index) in cycleInfo.deposit_priority" 
                :key="`deposit-${index}`"
                class="mb-1">
              {{ priority }}
            </li>
          </ul>
        </div>
  
        <!-- 적금 추천 전략 -->
        <div class="bg-gray-50 rounded-lg p-4">
          <h3 class="font-medium text-gray-800 mb-2">적금 상품 전략</h3>
          <ul class="list-disc list-inside text-gray-600">
            <li v-for="(priority, index) in cycleInfo.savings_priority" 
                :key="`savings-${index}`"
                class="mb-1">
              {{ priority }}
            </li>
          </ul>
        </div>
      </div>
    </div>
  </template>
  
  <script setup>
  defineProps({
    title: {
      type: String,
      required: true
    },
    description: {
      type: String,
      required: true
    },
    cycleInfo: {
      type: Object,
      required: true
    }
  })
  </script>