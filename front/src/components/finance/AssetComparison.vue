<template>
    <div class="bg-white rounded-lg shadow-lg p-6">
      <h2 class="text-2xl font-semibold mb-6">연령대별 자산 비교</h2>
  
      <!-- 로딩 상태 -->
      <div v-if="!statusData" class="text-center py-8">
        <p>데이터를 불러오는 중...</p>
      </div>
  
      <!-- 차트 -->
      <div v-else class="mb-8 h-64">
        <Bar 
          :data="chartData" 
          :options="chartOptions" 
        />
      </div>
  
      <!-- 비교 분석 -->
      <div v-if="statusData" class="bg-gray-50 rounded-lg p-4">
        <h3 class="font-medium text-gray-800 mb-2">분석 결과</h3>
        <p class="text-gray-600">
          {{ getAnalysisMessage() }}
        </p>
        
        <!-- 자산 격차 표시 -->
        <div class="mt-4">
          <div class="flex items-center justify-between mb-2">
            <span class="text-sm text-gray-600">동년배 평균 대비</span>
            <span class="font-medium" :class="getComparisonColor()">
              {{ formatComparisonValue() }}
            </span>
          </div>
          <div class="h-2 bg-gray-200 rounded">
            <div
              class="h-2 rounded"
              :class="getComparisonColor('bg')"
              :style="{ width: getComparisonWidth() }"
            ></div>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script setup>
  import { computed, ref, watch } from 'vue'
  import { Bar } from 'vue-chartjs'
  import {
    Chart as ChartJS,
    CategoryScale,
    LinearScale,
    BarElement,
    Title,
    Tooltip,
    Legend
  } from 'chart.js'
  
  ChartJS.register(
    CategoryScale,
    LinearScale,
    BarElement,
    Title,
    Tooltip,
    Legend
  )
  
  const props = defineProps({
    statusData: {
      type: Object,
      required: true
    }
  })
  
  // 차트 데이터 계산
  const chartData = computed(() => {
    if (!props.statusData) {
      return {
        labels: [],
        datasets: [{
          label: '자산 비교 (만원)',
          data: [],
          backgroundColor: [],
          borderColor: [],
          borderWidth: 1
        }]
      }
    }
  
    return {
      labels: ['내 자산', '연령대 평균'],
      datasets: [
        {
          label: '자산 비교 (만원)',
          data: [
            props.statusData.user_asset,
            props.statusData.average_asset_for_age
          ],
          backgroundColor: [
            'rgba(59, 130, 246, 0.5)',
            'rgba(156, 163, 175, 0.5)'
          ],
          borderColor: [
            'rgb(59, 130, 246)',
            'rgb(156, 163, 175)'
          ],
          borderWidth: 1
        }
      ]
    }
  })
  
  // 차트 옵션
  const chartOptions = {
    responsive: true,
    maintainAspectRatio: false,
    scales: {
      y: {
        beginAtZero: true,
        ticks: {
          callback: value => `${value}만원`
        }
      }
    },
    plugins: {
      legend: {
        display: true
      },
      tooltip: {
        callbacks: {
          label: (context) => `${context.raw}만원`
        }
      }
    }
  }
  
  const formatCurrency = (value) => {
    return new Intl.NumberFormat('ko-KR', {
      style: 'currency',
      currency: 'KRW'
    }).format(value * 10000)
  }
  
  const getAnalysisMessage = () => {
    if (!props.statusData) return ''
    
    const difference = props.statusData.asset_comparison
    if (difference > 0) {
      return `현재 자산이 동년배 평균보다 ${formatCurrency(difference)} 많습니다. 현재의 자산관리 방식을 유지하면서 장기적인 자산 증식 전략을 고려해보세요.`
    } else if (difference < 0) {
      return `현재 자산이 동년배 평균보다 ${formatCurrency(Math.abs(difference))} 적습니다. 추천된 저축 전략을 참고하여 자산을 늘려나가는 것을 고려해보세요.`
    }
    return '동년배 평균과 비슷한 수준의 자산을 보유하고 있습니다.'
  }
  
  const getComparisonColor = (prefix = 'text') => {
    if (!props.statusData) return `${prefix}-gray-600`
    
    const difference = props.statusData.asset_comparison
    if (difference > 0) return `${prefix}-green-600`
    if (difference < 0) return `${prefix}-red-600`
    return `${prefix}-gray-600`
  }
  
  const formatComparisonValue = () => {
    if (!props.statusData) return ''
    
    const difference = props.statusData.asset_comparison
    const value = Math.abs(difference)
    return difference > 0 
      ? `+${formatCurrency(value)}`
      : `-${formatCurrency(value)}`
  }
  
  const getComparisonWidth = () => {
    if (!props.statusData) return '0%'
    
    const ratio = props.statusData.user_asset / props.statusData.average_asset_for_age
    const percentage = Math.min(Math.max(ratio * 100, 0), 100)
    return `${percentage}%`
  }
  </script>