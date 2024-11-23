<template>
  <div class="recommendation-container">
    <h2 class="main-title">소득 기반 맞춤 추천</h2>

    <!-- 소득 수준 정보 -->
    <div class="income-status">
      <div class="income-header">
        <span class="income-level">
          소득 수준: {{ incomeInfo.level }}
        </span>
      </div>
    </div>

    <!-- 투자 제안 -->
    <div class="suggestions-grid">
      <!-- 월 저축 추천 -->
      <div class="suggestion-card savings-card">
        <h3 class="suggestion-title">월 저축 추천 금액</h3>
        <div class="amount-display">
          {{ formatCurrency(investmentSuggestion.monthly_savings) }}
        </div>
        <p class="amount-subtitle">
          연간 추천 저축액: {{ formatCurrency(investmentSuggestion.monthly_savings * 12) }}
        </p>
      </div>

      <!-- 자산 배분 추천 -->
      <div class="suggestion-card allocation-card">
        <h3 class="suggestion-title">추천 자산 배분</h3>
        <div class="allocation-container">
          <div class="allocation-bar-container">
            <div class="allocation-bar">
              <div 
                class="allocation-progress"
                :style="{ width: `${investmentSuggestion.deposit_ratio * 100}%` }"
              ></div>
            </div>
            <div class="allocation-labels">
              <span class="label-deposit">예금: {{ (investmentSuggestion.deposit_ratio * 100).toFixed(0) }}%</span>
              <span class="label-savings">적금: {{ (investmentSuggestion.savings_ratio * 100).toFixed(0) }}%</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
// import { defineProps } from 'vue'

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
  }).format(value * 10000)
}
</script>

<style scoped>
.recommendation-container {
  background: white;
  border-radius: 16px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
  padding: 28px;
  margin-bottom: 24px;
  transition: transform 0.3s ease;
}

.recommendation-container:hover {
  transform: translateY(-2px);
}

.main-title {
  font-size: 24px;
  font-weight: 600;
  color: #1f2937;
  margin-bottom: 20px;
  position: relative;
  padding-left: 12px;
}

.main-title::before {
  content: '';
  position: absolute;
  left: 0;
  top: 50%;
  transform: translateY(-50%);
  width: 4px;
  height: 24px;
  background: linear-gradient(to bottom, #34d399, #10b981);
  border-radius: 2px;
}

.income-status {
  background: linear-gradient(135deg, #ecfdf5 0%, #d1fae5 100%);
  border-radius: 12px;
  padding: 20px;
  margin-bottom: 24px;
  transition: all 0.3s ease;
}

.income-status:hover {
  box-shadow: 0 4px 12px rgba(16, 185, 129, 0.1);
}

.income-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.income-level {
  font-size: 18px;
  font-weight: 500;
  color: #065f46;
}

.suggestions-grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: 20px;
}

@media (min-width: 768px) {
  .suggestions-grid {
    grid-template-columns: 1fr 1fr;
  }
}

.suggestion-card {
  background: #f9fafb;
  border-radius: 12px;
  padding: 24px;
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
}

.suggestion-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 4px;
  background: linear-gradient(to right, #60a5fa, #3b82f6);
  opacity: 0;
  transition: opacity 0.3s ease;
}

.suggestion-card:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
  transform: translateY(-2px);
}

.suggestion-card:hover::before {
  opacity: 1;
}

.suggestion-title {
  font-size: 16px;
  font-weight: 500;
  color: #374151;
  margin-bottom: 12px;
}

.amount-display {
  font-size: 24px;
  font-weight: 700;
  color: #059669;
  margin-bottom: 4px;
}

.amount-subtitle {
  font-size: 14px;
  color: #6b7280;
  margin-top: 4px;
}

.allocation-container {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.allocation-bar-container {
  width: 100%;
}

.allocation-bar {
  height: 16px;
  background: #e5e7eb;
  border-radius: 8px;
  overflow: hidden;
  position: relative;
}

.allocation-progress {
  height: 100%;
  background: linear-gradient(to right, #60a5fa, #3b82f6);
  border-radius: 8px;
  transition: width 1s ease-in-out;
}

.allocation-labels {
  display: flex;
  justify-content: space-between;
  margin-top: 8px;
  font-size: 14px;
}

.label-deposit {
  color: #3b82f6;
  font-weight: 500;
}

.label-savings {
  color: #6b7280;
  font-weight: 500;
}

@keyframes slideIn {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.recommendation-container {
  animation: slideIn 0.5s ease-out;
}
</style>