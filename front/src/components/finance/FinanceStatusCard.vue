<template>
  <div class="status-container">
    <h2 class="status-title">
      <span class="title-icon">💰</span>
      재무상태 분석
    </h2>
    
    <!-- 점수 표시 -->
    <div class="score-container">
      <div class="score-circle">
        <svg class="score-svg">
          <!-- 배경 서클 -->
          <circle
            class="score-background"
            stroke-width="12"
            stroke="currentColor"
            fill="transparent"
            r="70"
            cx="96"
            cy="96"
          />
          <!-- 점수 표시 서클 -->
          <circle
            :class="['score-indicator', getScoreColorClass]"
            stroke-width="12"
            :stroke-dasharray="circumference"
            :stroke-dashoffset="dashOffset"
            stroke-linecap="round"
            stroke="currentColor"
            fill="transparent"
            r="70"
            cx="96"
            cy="96"
          />
        </svg>
        <div class="score-value">
          <span class="score-number">{{ Math.round(statusData.asset_health_score) }}</span>
          <span class="score-label">점</span>
        </div>
      </div>
    </div>
  
    <!-- 상세 정보 -->
    <div class="details-grid">
      <div class="details-column">
        <div class="detail-card">
          <h3 class="detail-label">연령대</h3>
          <p class="detail-value">{{ statusData.age_group }}</p>
        </div>
        <div class="detail-card">
          <h3 class="detail-label">연 소득</h3>
          <p class="detail-value">{{ formatCurrency(statusData.annual_income) }}</p>
        </div>
      </div>
      
      <div class="details-column">
        <div class="detail-card">
          <h3 class="detail-label">총 자산</h3>
          <p class="detail-value">{{ formatCurrency(statusData.user_asset) }}</p>
        </div>
        <div class="detail-card">
          <h3 class="detail-label">추천 월 저축액</h3>
          <p class="detail-value">{{ formatCurrency(statusData.recommended_monthly_saving) }}</p>
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

const circumference = computed(() => 2 * Math.PI * 70)
const dashOffset = computed(() => 
  circumference.value - (props.statusData.asset_health_score / 100) * circumference.value
)

const getScoreColorClass = computed(() => {
  const score = props.statusData.asset_health_score
  if (score >= 80) return 'score-excellent'
  if (score >= 60) return 'score-good'
  if (score >= 40) return 'score-fair'
  return 'score-poor'
})

const formatCurrency = (value) => {
  return new Intl.NumberFormat('ko-KR', {
    style: 'currency',
    currency: 'KRW'
  }).format(value * 10000)
}
</script>

<style scoped>
.status-container {
  background: linear-gradient(135deg, #f0f7ff 0%, #ffffff 50%, #f0f7ff 100%);
  border-radius: 16px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
  padding: 32px;
  animation: fadeIn 0.5s ease-out;
}

.status-title {
  font-size: 24px;
  font-weight: 700;
  color: #1f2937;
  margin-bottom: 32px;
  display: flex;
  align-items: center;
  gap: 12px;
}

.title-icon {
  color: #3b82f6;
}

.score-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  margin-bottom: 48px;
  position: relative;
}

.score-circle {
  position: relative;
}

.score-svg {
  width: 192px;
  height: 192px;
  transform: rotate(-90deg);
  animation: rotateIn 1.5s ease-out;
}

.score-background {
  color: #e5e7eb;
}

.score-indicator {
  transition: stroke-dashoffset 1.5s ease-in-out;
}

.score-value {
  position: absolute;
  inset: 0;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  animation: fadeIn 0.5s ease-out 0.5s backwards;
}

.score-number {
  font-size: 32px;
  font-weight: 700;
  color: #1f2937;
}

.score-label {
  color: #6b7280;
  font-size: 18px;
}

.details-grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: 24px;
  animation: slideUp 0.5s ease-out 0.3s backwards;
}

@media (min-width: 768px) {
  .details-grid {
    grid-template-columns: 1fr 1fr;
  }
}

.details-column {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.detail-card {
  background: white;
  padding: 24px;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
  transition: all 0.3s ease;
}

.detail-card:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  transform: translateY(-2px);
}

.detail-label {
  font-size: 14px;
  font-weight: 500;
  color: #6b7280;
  margin-bottom: 4px;
}

.detail-value {
  font-size: 18px;
  font-weight: 600;
  color: #1f2937;
}

.score-excellent {
  color: #10b981;
}

.score-good {
  color: #3b82f6;
}

.score-fair {
  color: #f59e0b;
}

.score-poor {
  color: #ef4444;
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

@keyframes rotateIn {
  from {
    transform: rotate(-180deg);
  }
  to {
    transform: rotate(-90deg);
  }
}

@keyframes slideUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
</style>