<template>
  <div class="lifecycle-container">
    <h2 class="main-title">{{ title }}</h2>
    
    <!-- 생애주기 정보 카드 -->
    <div class="lifecycle-card">
      <div class="lifecycle-header">
        <span class="lifecycle-stage">
          현재 생애주기: {{ cycleInfo.cycle }}
        </span>
      </div>
      <p class="lifecycle-description">{{ description }}</p>
    </div>

    <!-- 추천 전략 -->
    <div class="strategies-grid">
      <!-- 예금 추천 전략 -->
      <div class="strategy-card">
        <div class="strategy-header">
          <h3 class="strategy-title">예금 상품 전략</h3>
        </div>
        <ul class="strategy-list">
          <li v-for="(priority, index) in cycleInfo.deposit_priority" 
              :key="`deposit-${index}`"
              class="strategy-item"
              :style="{ animationDelay: `${index * 0.1}s` }">
            {{ priority }}
          </li>
        </ul>
      </div>

      <!-- 적금 추천 전략 -->
      <div class="strategy-card">
        <div class="strategy-header">
          <h3 class="strategy-title">적금 상품 전략</h3>
        </div>
        <ul class="strategy-list">
          <li v-for="(priority, index) in cycleInfo.savings_priority" 
              :key="`savings-${index}`"
              class="strategy-item"
              :style="{ animationDelay: `${index * 0.1}s` }">
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

<style scoped>
.lifecycle-container {
  background: white;
  border-radius: 16px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
  padding: 28px;
  margin-bottom: 24px;
  transition: all 0.3s ease;
}

.lifecycle-container:hover {
  transform: translateY(-2px);
}

.main-title {
  font-size: 24px;
  font-weight: 600;
  color: #1f2937;
  margin-bottom: 24px;
  padding-bottom: 12px;
  border-bottom: 2px solid #e5e7eb;
  position: relative;
}

.main-title::after {
  content: '';
  position: absolute;
  bottom: -2px;
  left: 0;
  width: 100px;
  height: 2px;
  background: linear-gradient(to right, #3b82f6, #60a5fa);
}

.lifecycle-card {
  background: linear-gradient(135deg, #eff6ff 0%, #dbeafe 100%);
  border-radius: 12px;
  padding: 24px;
  margin-bottom: 28px;
  transition: all 0.3s ease;
}

.lifecycle-card:hover {
  box-shadow: 0 4px 12px rgba(59, 130, 246, 0.1);
}

.lifecycle-header {
  margin-bottom: 12px;
}

.lifecycle-stage {
  font-size: 18px;
  font-weight: 600;
  color: #1e40af;
  display: block;
  padding-left: 12px;
  border-left: 4px solid #3b82f6;
}

.lifecycle-description {
  color: #1f2937;
  line-height: 1.6;
  font-size: 15px;
}

.strategies-grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: 24px;
}

@media (min-width: 768px) {
  .strategies-grid {
    grid-template-columns: 1fr 1fr;
  }
}

.strategy-card {
  background: #f9fafb;
  border-radius: 12px;
  padding: 24px;
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
}

.strategy-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 4px;
  height: 100%;
  background: linear-gradient(to bottom, #3b82f6, #60a5fa);
  opacity: 0;
  transition: opacity 0.3s ease;
}

.strategy-card:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
}

.strategy-card:hover::before {
  opacity: 1;
}

.strategy-header {
  margin-bottom: 16px;
}

.strategy-title {
  font-size: 18px;
  font-weight: 600;
  color: #374151;
}

.strategy-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.strategy-item {
  position: relative;
  padding-left: 24px;
  margin-bottom: 12px;
  color: #4b5563;
  font-size: 15px;
  line-height: 1.5;
  animation: slideIn 0.5s ease-out backwards;
}

.strategy-item::before {
  content: '';
  position: absolute;
  left: 0;
  top: 8px;
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: #3b82f6;
  opacity: 0.7;
}

.strategy-item:hover::before {
  background: #2563eb;
  opacity: 1;
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

/* 반응형 조정 */
@media (max-width: 640px) {
  .lifecycle-container {
    padding: 20px;
  }
  
  .main-title {
    font-size: 20px;
  }
  
  .lifecycle-stage {
    font-size: 16px;
  }
  
  .strategy-title {
    font-size: 16px;
  }
  
  .strategy-item {
    font-size: 14px;
  }
}
</style>