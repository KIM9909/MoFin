<template>
    <div class="bg-white rounded-lg shadow-lg p-6 mb-6">
      <h2 class="text-2xl font-semibold mb-4">{{ title }}</h2>
  
      <div class="overflow-x-auto">
        <table class="min-w-full divide-y divide-gray-200">
          <thead class="bg-gray-50">
            <tr>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                금융사
              </th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                상품명
              </th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                최고금리
              </th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                가입방법
              </th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                구독
              </th>
            </tr>
          </thead>
          <tbody class="bg-white divide-y divide-gray-200">
            <tr v-for="item in products" :key="item.product.fin_prdt_cd">
              <td class="px-6 py-4 whitespace-nowrap">
                <div class="text-sm font-medium text-gray-900">
                  {{ item.product.kor_co_nm }}
                </div>
              </td>
              <td class="px-6 py-4">
                <div class="text-sm text-gray-900">
                  {{ item.product.fin_prdt_nm }}
                </div>
                <div class="text-xs text-gray-500">
                  {{ truncateText(item.product.etc_note) }}
                </div>
              </td>
              <td class="px-6 py-4 whitespace-nowrap">
                <div class="text-sm text-blue-600 font-semibold">
                  {{ formatRate(item.max_rate) }}%
                </div>
              </td>
              <td class="px-6 py-4">
                <div class="text-sm text-gray-900">
                  {{ item.product.join_way }}
                </div>
              </td>
              <td class="px-6 py-4 whitespace-nowrap">
                <button 
                  @click="toggleSubscribe(item.product.fin_prdt_cd)"
                  :class="[
                    'px-3 py-1 rounded text-sm font-semibold',
                    isSubscribed(item.product.fin_prdt_cd) 
                      ? 'bg-blue-100 text-blue-800 hover:bg-blue-200'
                      : 'bg-gray-100 text-gray-800 hover:bg-gray-200'
                  ]"
                >
                  {{ isSubscribed(item.product.fin_prdt_cd) ? '구독중' : '구독하기' }}
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </template>
  
  <script setup>
  import { defineProps } from 'vue'
  import { useSubscriptionStore } from '@/stores/subscription'
  
  const props = defineProps({
    title: {
      type: String,
      required: true
    },
    products: {
      type: Array,
      required: true
    },
    productType: {
      type: String,
      required: true,
      validator: (value) => ['deposit', 'savings'].includes(value)
    }
  })
  
  const subscriptionStore = useSubscriptionStore()
  
  const formatRate = (rate) => {
    return rate?.toFixed(2) || '0.00'
  }
  
  const truncateText = (text, length = 50) => {
    if (!text) return ''
    return text.length > length ? text.slice(0, length) + '...' : text
  }
  
  const isSubscribed = (productCode) => {
    return subscriptionStore.isSubscribed(props.productType, productCode)
  }
  
  const toggleSubscribe = async (productCode) => {
    try {
      await subscriptionStore.toggleSubscription(props.productType, productCode)
    } catch (error) {
      console.error('구독 토글 실패:', error)
    }
  }
  </script>