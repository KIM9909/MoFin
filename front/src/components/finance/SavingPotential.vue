<template>
  <div class="analysis-container">
    <h2 class="main-title">저축 잠재력 분석</h2>

    <!-- 월 저축 목표 -->
    <div class="goals-grid">
      <div class="goal-card savings-card">
        <h3 class="goal-label">추천 월 저축액</h3>
        <p class="goal-value">
          {{ formatCurrency(statusData.recommended_monthly_saving) }}
        </p>
        <p class="goal-subtext">
          연간 {{ formatCurrency(statusData.recommended_monthly_saving * 12) }}
        </p>
      </div>

      <div class="goal-card future-card">
        <h3 class="goal-label">예상 10년 후 자산</h3>
        <p class="goal-value">
          {{ formatCurrency(calculateFutureAsset(10)) }}
        </p>
        <p class="goal-subtext">
          현재 대비 {{ calculateGrowthRate(10) }}% 성장
        </p>
      </div>
    </div>

    <!-- 저축 전략 제안 -->
    <div class="strategy-container">
      <h3 class="strategy-title">맞춤형 저축 전략</h3>
      
      <div class="strategy-goals">
        <!-- 단기 목표 -->
        <div class="goal-item">
          <h4 class="goal-period">단기 목표 (1년)</h4>
          <div class="progress-container">
            <div class="progress-bar">
              <div class="progress-fill short-term"></div>
            </div>
            <span class="progress-value">
              {{ formatCurrency(statusData.recommended_monthly_saving * 12) }}
            </span>
          </div>
        </div>

        <!-- 중기 목표 -->
        <div class="goal-item">
          <h4 class="goal-period">중기 목표 (5년)</h4>
          <div class="progress-container">
            <div class="progress-bar">
              <div class="progress-fill mid-term"></div>
            </div>
            <span class="progress-value">
              {{ formatCurrency(calculateFutureAsset(5)) }}
            </span>
          </div>
        </div>

        <!-- 장기 목표 -->
        <div class="goal-item">
          <h4 class="goal-period">장기 목표 (10년)</h4>
          <div class="progress-container">
            <div class="progress-bar">
              <div class="progress-fill long-term"></div>
            </div>
            <span class="progress-value">
              {{ formatCurrency(calculateFutureAsset(10)) }}
            </span>
          </div>
        </div>
      </div>

      <!-- 저축 조언 -->
      <div class="advice-section">
        <p class="advice-title">💡 추천 저축 전략:</p>
        <ul class="advice-list">
          <li>월 수입의 {{ calculateSavingRatio() }}%를 저축하는 것을 목표로 하세요.</li>
          <li>예금과 적금을 {{ getSavingDistributionTip() }}</li>
          <li>{{ getAgeBasedTip() }}</li>
        </ul>
      </div>
    </div>
  </div>
</template>
  
  <script setup>
  // import { defineProps } from 'vue'
  
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
  
  const calculateFutureAsset = (years = 10) => {
    const monthlyAmount = props.statusData.recommended_monthly_saving;
    const currentAsset = props.statusData.user_asset;
    const estimatedReturn = 0.038; // 연 3.8% 수익률 가정

    // 단리 계산
    const futureValue = currentAsset * (1 + estimatedReturn * years) + 
      monthlyAmount * 12 * years * (1 + (estimatedReturn * years) / 2);

    return Math.round(futureValue);
  };
  
  const calculateGrowthRate = (years = 10) => {
    const futureAsset = calculateFutureAsset(years);
    const currentAsset = props.statusData.user_asset;
    return Math.round((futureAsset / currentAsset - 1) * 100);
  }
  
  const calculateSavingRatio = () => {
    const monthlyIncome = props.statusData.annual_income / 12;
    const monthlySaving = props.statusData.recommended_monthly_saving;
    return Math.round((monthlySaving / monthlyIncome) * 100);
  }
  
  const getSavingDistributionTip = () => {
    const age = parseInt(props.statusData.age_group);
    if (age < 30) {
      return '6:4의 비율로 분산 투자하는 것을 추천드립니다.';
    } else if (age < 40) {
      return '7:3의 비율로 분산 투자하는 것을 추천드립니다.';
    } else if (age < 50) {
      return '5:5의 비율로 안정적으로 운용하는 것을 추천드립니다.';
    } else {
      return '8:2의 비율로 안정적으로 운용하는 것을 추천드립니다.';
    }
  }
  
  const getAgeBasedTip = () => {
    const age = parseInt(props.statusData.age_group);
    if (age < 30) {
      return '청년층의 경우, 정기적금을 통한 자산 형성이 중요합니다.';
    } else if (age < 40) {
      return '자산 형성기에는 고금리 상품을 적극 활용하세요.';
    } else if (age < 50) {
      return '자산 안정기에는 안정적인 수익률의 상품을 선택하세요.';
    } else {
      return '은퇴 준비를 위해 안정적인 예금 상품 비중을 높이세요.';
    }
  }
  </script>

<style scoped>
.analysis-container {
  background: white;
  border-radius: 12px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
  padding: 24px;
  transition: transform 0.3s ease;
}

.analysis-container:hover {
  transform: translateY(-2px);
}

.main-title {
  font-size: 24px;
  font-weight: 600;
  color: #1f2937;
  margin-bottom: 24px;
}

.goals-grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: 24px;
  margin-bottom: 32px;
}

@media (min-width: 768px) {
  .goals-grid {
    grid-template-columns: 1fr 1fr;
  }
}

.goal-card {
  border-radius: 12px;
  padding: 20px;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.goal-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.savings-card {
  background: linear-gradient(135deg, #eef6ff 0%, #dbeafe 100%);
}

.future-card {
  background: linear-gradient(135deg, #ecfdf5 0%, #d1fae5 100%);
}

.goal-label {
  font-size: 14px;
  font-weight: 500;
  color: #1f2937;
  margin-bottom: 8px;
}

.goal-value {
  font-size: 24px;
  font-weight: 700;
  margin-bottom: 4px;
}

.savings-card .goal-value {
  color: #2563eb;
}

.future-card .goal-value {
  color: #059669;
}

.goal-subtext {
  font-size: 14px;
  opacity: 0.8;
}

.savings-card .goal-subtext {
  color: #2563eb;
}

.future-card .goal-subtext {
  color: #059669;
}

.strategy-container {
  background: #f9fafb;
  border-radius: 12px;
  padding: 20px;
}

.strategy-title {
  font-size: 18px;
  font-weight: 500;
  color: #1f2937;
  margin-bottom: 20px;
}

.strategy-goals {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.goal-item {
  animation: slideIn 0.5s ease-out;
}

.goal-period {
  font-size: 14px;
  font-weight: 500;
  color: #4b5563;
  margin-bottom: 8px;
}

.progress-container {
  display: flex;
  align-items: center;
  gap: 16px;
}

.progress-bar {
  flex: 1;
  height: 8px;
  background: #e5e7eb;
  border-radius: 4px;
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  border-radius: 4px;
  transition: width 1s ease-in-out;
}

.short-term {
  background: #3b82f6;
  width: 25%;
}

.mid-term {
  background: #10b981;
  width: 50%;
}

.long-term {
  background: #8b5cf6;
  width: 75%;
}

.progress-value {
  font-size: 14px;
  font-weight: 500;
  color: #4b5563;
  min-width: 100px;
  text-align: right;
}

.advice-section {
  margin-top: 24px;
  padding-top: 20px;
  border-top: 1px solid #e5e7eb;
}

.advice-title {
  font-size: 14px;
  color: #4b5563;
  margin-bottom: 12px;
}

.advice-list {
  list-style-type: disc;
  padding-left: 20px;
  color: #6b7280;
  font-size: 14px;
  line-height: 1.6;
}

.advice-list li {
  margin-bottom: 8px;
  animation: fadeIn 0.5s ease-out;
}

@keyframes slideIn {
  from {
    opacity: 0;
    transform: translateX(-20px);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
}

@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}
</style>