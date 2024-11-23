<template>
  <div class="dashboard-container">
    <h2 class="dashboard-title">
      <span class="title-icon">📊</span> 
      연령대별 자산 비교
    </h2>

    <!-- 로딩 상태 -->
    <div v-if="!statusData" class="loading-container">
      <div class="loading-spinner"></div>
      <p>데이터를 불러오는 중...</p>
    </div>

    <div v-else class="content-wrapper">
      <!-- 상단 통계 카드 -->
      <div class="stats-grid">
        <div class="stat-card">
          <div class="stat-label">내 자산</div>
          <div class="stat-value stat-primary">
            {{ formatCurrency(statusData.user_asset) }}
          </div>
        </div>
        
        <div class="stat-card">
          <div class="stat-label">연령대 평균</div>
          <div class="stat-value">
            {{ formatCurrency(statusData.average_asset_for_age) }}
          </div>
        </div>

        <div class="stat-card">
          <div class="stat-label">평균 대비</div>
          <div class="stat-value" :class="getComparisonColor()">
            {{ formatComparisonValue() }}
          </div>
        </div>
      </div>

      <!-- 차트 -->
      <div class="chart-container">
        <h3 class="chart-title">자산 비교</h3>
        <div class="chart-wrapper">
          <Bar 
            :data="chartData" 
            :options="chartOptions" 
          />
        </div>
      </div>

      <!-- 비교 분석 -->
      <div class="analysis-container">
        <div class="analysis-content">
          <h3 class="analysis-title">분석 결과</h3>
          <p class="analysis-text">
            {{ getAnalysisMessage() }}
          </p>
          
          <!-- 자산 격차 표시 -->
          <div class="comparison-container">
            <div class="comparison-header">
              <span>동년배 평균 대비</span>
              <span :class="getComparisonColor()">
                {{ formatComparisonValue() }}
              </span>
            </div>
            <div class="progress-bar-bg">
              <div
                class="progress-bar"
                :class="getComparisonColor('bg')"
                :style="{ width: getComparisonWidth() }"
              ></div>
            </div>
          </div>
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
          'rgba(59, 130, 246, 0.7)',  // 더 진한 블루
          'rgba(209, 213, 219, 0.7)'  // 더 진한 그레이
        ],
        borderColor: [
          'rgb(37, 99, 235)',  // 더 진한 테두리
          'rgb(156, 163, 175)'
        ],
        borderWidth: 2,
        borderRadius: 8,
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
      grid: {
        color: 'rgba(0, 0, 0, 0.1)'
      },
      ticks: {
        callback: value => `${value.toLocaleString()}만원`,
        font: {
          family: "'Pretendard', sans-serif"
        }
      }
    },
    x: {
      grid: {
        display: false
      },
      ticks: {
        font: {
          family: "'Pretendard', sans-serif"
        }
      }
    }
  },
  plugins: {
    legend: {
      display: false
    },
    tooltip: {
      backgroundColor: 'rgba(255, 255, 255, 0.9)',
      titleColor: '#1f2937',
      bodyColor: '#1f2937',
      bodyFont: {
        family: "'Pretendard', sans-serif"
      },
      titleFont: {
        family: "'Pretendard', sans-serif"
      },
      padding: 12,
      borderColor: 'rgba(0, 0, 0, 0.1)',
      borderWidth: 1,
      callbacks: {
        label: (context) => `${context.raw.toLocaleString()}만원`
      }
    }
  }
}

const formatCurrency = (value) => {
  return new Intl.NumberFormat('ko-KR', {
    style: 'currency',
    currency: 'KRW',
    maximumFractionDigits: 0
  }).format(value * 10000)
}

const getAnalysisMessage = () => {
  if (!props.statusData) return ''
  
  const difference = props.statusData.asset_comparison
  if (difference > 0) {
    return `현재 자산이 동년배 평균보다 ${formatCurrency(difference)} 많습니다. 현재의 자산관리 방식을 잘 유지하고 계시네요! 장기적인 자산 증식 전략을 함께 고려해보시면 좋을 것 같습니다.`
  } else if (difference < 0) {
    return `현재 자산이 동년배 평균보다 ${formatCurrency(Math.abs(difference))} 적습니다. 걱정하지 마세요. 아래 추천된 맞춤형 저축 전략을 참고하여 함께 자산을 늘려나가보아요.`
  }
  return '동년배 평균과 비슷한 수준의 자산을 보유하고 있습니다. 앞으로도 꾸준한 관리가 중요합니다.'
}

const getComparisonColor = (prefix = 'text') => {
  if (!props.statusData) return `${prefix}-gray-600`
  
  const difference = props.statusData.asset_comparison
  if (difference > 0) return `${prefix}-emerald-500`  // 더 밝은 초록색
  if (difference < 0) return `${prefix}-rose-500`    // 더 밝은 빨간색
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

<style scoped>
.dashboard-container {
  background: linear-gradient(135deg, #f0f7ff 0%, #ffffff 100%);
  border-radius: 12px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
  padding: 32px;
  animation: fadeIn 0.5s ease-out;
}

.dashboard-title {
  font-size: 24px;
  font-weight: 700;
  color: #1f2937;
  margin-bottom: 32px;
  display: flex;
  align-items: center;
  gap: 8px;
}

.title-icon {
  color: #3b82f6;
}

.loading-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 48px 0;
}

.loading-spinner {
  width: 48px;
  height: 48px;
  border: 2px solid #e5e7eb;
  border-bottom-color: #3b82f6;
  border-radius: 50%;
  margin-bottom: 16px;
  animation: spin 1s linear infinite;
}

.content-wrapper {
  display: flex;
  flex-direction: column;
  gap: 32px;
}

.stats-grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: 24px;
  margin-bottom: 32px;
}

@media (min-width: 768px) {
  .stats-grid {
    grid-template-columns: repeat(3, 1fr);
  }
}

.stat-card {
  background: white;
  border-radius: 12px;
  padding: 24px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
  transition: transform 0.3s ease;
}

.stat-card:hover {
  transform: translateY(-4px);
}

.stat-label {
  font-size: 14px;
  color: #6b7280;
  margin-bottom: 8px;
}

.stat-value {
  font-size: 24px;
  font-weight: 700;
  color: #1f2937;
}

.stat-primary {
  color: #3b82f6;
}

.chart-container {
  background: white;
  border-radius: 12px;
  padding: 24px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
  transition: box-shadow 0.3s ease;
}

.chart-container:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.chart-title {
  font-size: 18px;
  font-weight: 600;
  color: #1f2937;
  margin-bottom: 16px;
}

.chart-wrapper {
  height: 288px;
  width: 100%;
}

.analysis-container {
  background: white;
  border-radius: 12px;
  padding: 24px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

.analysis-title {
  font-size: 18px;
  font-weight: 600;
  color: #1f2937;
  margin-bottom: 12px;
}

.analysis-text {
  color: #4b5563;
  line-height: 1.6;
  margin-bottom: 24px;
}

.comparison-container {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.comparison-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 14px;
  color: #6b7280;
}

.progress-bar-bg {
  width: 100%;
  height: 12px;
  background: #f3f4f6;
  border-radius: 6px;
  overflow: hidden;
}

.progress-bar {
  height: 100%;
  border-radius: 6px;
  transition: width 0.5s ease-in-out;
}

/* 상태별 색상 클래스 */
.text-green-600 {
  color: #059669;
}

.text-red-600 {
  color: #dc2626;
}

.text-gray-600 {
  color: #4b5563;
}

.bg-green-600 {
  background-color: #059669;
}

.bg-red-600 {
  background-color: #dc2626;
}

.bg-gray-600 {
  background-color: #4b5563;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}
</style>