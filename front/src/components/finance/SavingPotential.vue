<template>
    <div class="bg-white rounded-lg shadow-lg p-6">
      <h2 class="text-2xl font-semibold mb-6">저축 잠재력 분석</h2>
  
      <!-- 월 저축 목표 -->
      <div class="grid md:grid-cols-2 gap-6 mb-8">
        <div class="bg-blue-50 rounded-lg p-4">
          <h3 class="text-sm font-medium text-blue-800 mb-2">추천 월 저축액</h3>
          <p class="text-2xl font-bold text-blue-600">
            {{ formatCurrency(statusData.recommended_monthly_saving) }}
          </p>
          <p class="text-sm text-blue-600 mt-1">
            연간 {{ formatCurrency(statusData.recommended_monthly_saving * 12) }}
          </p>
        </div>
  
        <div class="bg-green-50 rounded-lg p-4">
          <h3 class="text-sm font-medium text-green-800 mb-2">예상 10년 후 자산</h3>
          <p class="text-2xl font-bold text-green-600">
            {{ formatCurrency(calculateFutureAsset()) }}
          </p>
          <p class="text-sm text-green-600 mt-1">
            현재 대비 {{ calculateGrowthRate() }}% 성장
          </p>
        </div>
      </div>
  
      <!-- 저축 전략 제안 -->
      <div class="bg-gray-50 rounded-lg p-4">
        <h3 class="font-medium text-gray-800 mb-4">맞춤형 저축 전략</h3>
        
        <div class="space-y-4">
          <!-- 단기 목표 -->
          <div>
            <h4 class="text-sm font-medium text-gray-600 mb-2">단기 목표 (1년)</h4>
            <div class="flex items-center">
              <div class="flex-1">
                <div class="h-2 bg-gray-200 rounded">
                  <div
                    class="h-2 bg-blue-500 rounded"
                    :style="{ width: '25%' }"
                  ></div>
                </div>
              </div>
              <span class="ml-4 text-sm font-medium">
                {{ formatCurrency(statusData.recommended_monthly_saving * 12) }}
              </span>
            </div>
          </div>
  
          <!-- 중기 목표 -->
          <div>
            <h4 class="text-sm font-medium text-gray-600 mb-2">중기 목표 (5년)</h4>
            <div class="flex items-center">
              <div class="flex-1">
                <div class="h-2 bg-gray-200 rounded">
                  <div
                    class="h-2 bg-green-500 rounded"
                    :style="{ width: '50%' }"
                  ></div>
                </div>
              </div>
              <span class="ml-4 text-sm font-medium">
                {{ formatCurrency(statusData.recommended_monthly_saving * 12 * 5) }}
              </span>
            </div>
          </div>
  
          <!-- 장기 목표 -->
          <div>
            <h4 class="text-sm font-medium text-gray-600 mb-2">장기 목표 (10년)</h4>
            <div class="flex items-center">
              <div class="flex-1">
                <div class="h-2 bg-gray-200 rounded">
                  <div
                    class="h-2 bg-purple-500 rounded"
                    :style="{ width: '75%' }"
                  ></div>
                </div>
              </div>
              <span class="ml-4 text-sm font-medium">
                {{ formatCurrency(calculateFutureAsset()) }}
              </span>
            </div>
          </div>
        </div>
  
        <!-- 저축 조언 -->
        <div class="mt-6 text-sm text-gray-600">
          <p class="mb-2">💡 추천 저축 전략:</p>
          <ul class="list-disc list-inside space-y-1">
            <li>월 수입의 {{ calculateSavingRatio() }}%를 저축하는 것을 목표로 하세요.</li>
            <li>예금과 적금을 {{ getSavingDistributionTip() }}</li>
            <li>{{ getAgeBasedTip() }}</li>
          </ul>
        </div>
      </div>
    </div>
  </template>
  
  <script setup>
  import { defineProps } from 'vue'
  
  const props = defineProps({
    statusData: {
      type: Object,
      required: true
    }
  })
  
  const formatCurrency = (value) => {
    return new Intl.NumberFormat('ko-KR', {
      style: 'currency',
      currency: 'KRW'
    }).format(value * 10000)
  }
  
  const calculateFutureAsset = () => {
    const monthlyAmount = props.statusData.recommended_monthly_saving
    const currentAsset = props.statusData.user_asset
    const years = 10
    const estimatedReturn = 0.05 // 연 5% 수익률 가정
    
    // 복리 계산
    const futureValue = currentAsset * Math.pow(1 + estimatedReturn, years) +
      monthlyAmount * 12 * ((Math.pow(1 + estimatedReturn, years) - 1) / estimatedReturn)
    
    return Math.round(futureValue)
  }
  
  const calculateGrowthRate = () => {
    const futureAsset = calculateFutureAsset()
    const currentAsset = props.statusData.user_asset
    return Math.round((futureAsset / currentAsset - 1) * 100)
  }
  
  const calculateSavingRatio = () => {
    const monthlyIncome = props.statusData.annual_income / 12
    const monthlySaving = props.statusData.recommended_monthly_saving
    return Math.round((monthlySaving / monthlyIncome) * 100)
  }
  
  const getSavingDistributionTip = () => {
    const age = parseInt(props.statusData.age_group)
    if (age < 30) {
      return '6:4의 비율로 분산 투자하는 것을 추천드립니다.'
    } else if (age < 40) {
      return '7:3의 비율로 분산 투자하는 것을 추천드립니다.'
    } else if (age < 50) {
      return '5:5의 비율로 안정적으로 운용하는 것을 추천드립니다.'
    } else {
      return '8:2의 비율로 안정적으로 운용하는 것을 추천드립니다.'
    }
  }
  
  const getAgeBasedTip = () => {
    const age = parseInt(props.statusData.age_group)
    if (age < 30) {
      return '청년층의 경우, 정기적금을 통한 자산 형성이 중요합니다.'
    } else if (age < 40) {
      return '자산 형성기에는 고금리 상품을 적극 활용하세요.'
    } else if (age < 50) {
      return '자산 안정기에는 안정적인 수익률의 상품을 선택하세요.'
    } else {
      return '은퇴 준비를 위해 안정적인 예금 상품 비중을 높이세요.'
    }
  }
  </script>