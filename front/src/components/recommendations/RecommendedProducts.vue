<template>
  <div class="product-container">
    <h2 class="main-title">{{ title }}</h2>

    <div class="table-container">
      <table class="product-table">
        <thead>
          <tr>
            <th class="th-company">금융사</th>
            <th class="th-product">상품명</th>
            <th class="th-rate">최고금리</th>
            <th class="th-method">가입방법</th>
            <th class="th-subscribe">구독</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="item in products" 
              :key="item.product.fin_prdt_cd"
              class="product-row">
            <td class="td-company">
              <div class="company-name">
                {{ item.product.kor_co_nm }}
              </div>
            </td>
            <td class="td-product">
              <div class="product-name">
                {{ item.product.fin_prdt_nm }}
              </div>
              <div class="product-description">
                {{ truncateText(item.product.etc_note) }}
              </div>
            </td>
            <td class="td-rate">
              <div class="rate-display">
                {{ formatRate(item.max_rate) }}%
              </div>
            </td>
            <td class="td-method">
              <div class="join-method">
                {{ item.product.join_way }}
              </div>
            </td>
            <td class="td-subscribe">
              <button 
                @click="toggleSubscribe(item.product.fin_prdt_cd)"
                :class="[
                  'subscribe-button',
                  isSubscribed(item.product.fin_prdt_cd) ? 'subscribed' : ''
                ]"
              >
                {{ isSubscribed(item.product.fin_prdt_cd) ? '가입 취소' : '가입하기' }}
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

<style scoped>
.product-container {
  background: white;
  border-radius: 16px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
  padding: 28px;
  margin-bottom: 24px;
  transition: all 0.3s ease;
}

.main-title {
  font-size: 24px;
  font-weight: 600;
  color: #1f2937;
  margin-bottom: 24px;
  position: relative;
  padding-left: 16px;
}

.main-title::before {
  content: '';
  position: absolute;
  left: 0;
  top: 50%;
  transform: translateY(-50%);
  width: 4px;
  height: 24px;
  background: linear-gradient(to bottom, #3b82f6, #60a5fa);
  border-radius: 2px;
}

.table-container {
  overflow-x: auto;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

.product-table {
  width: 100%;
  border-collapse: separate;
  border-spacing: 0;
  min-width: 800px;
}

/* 테이블 헤더 스타일 */
th {
  background: linear-gradient(to bottom, #f9fafb, #f3f4f6);
  padding: 16px;
  text-align: left;
  font-size: 13px;
  font-weight: 600;
  color: #4b5563;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  border-bottom: 1px solid #e5e7eb;
}

.th-company { width: 15%; }
.th-product { width: 35%; }
.th-rate { width: 15%; }
.th-method { width: 20%; }
.th-subscribe { width: 15%; }

/* 테이블 셀 스타일 */
td {
  padding: 16px;
  vertical-align: middle;
  border-bottom: 1px solid #e5e7eb;
  transition: background-color 0.2s ease;
}

.product-row {
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.product-row:hover {
  background-color: #f9fafb;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
}

.company-name {
  font-weight: 500;
  color: #1f2937;
}

.product-name {
  font-weight: 500;
  color: #1f2937;
  margin-bottom: 4px;
}

.product-description {
  font-size: 13px;
  color: #6b7280;
  line-height: 1.4;
}

.rate-display {
  font-weight: 600;
  color: #2563eb;
  font-size: 15px;
}

.join-method {
  color: #4b5563;
  font-size: 14px;
}

.subscribe-button {
  padding: 8px 16px;
  border-radius: 8px;
  font-weight: 500;
  font-size: 13px;
  transition: all 0.2s ease;
  cursor: pointer;
  border: 1px solid transparent;
}

.subscribe-button:not(.subscribed) {
  background-color: #f3f4f6;
  color: #4b5563;
}

.subscribe-button:not(.subscribed):hover {
  background-color: #e5e7eb;
  color: #1f2937;
}

.subscribe-button.subscribed {
  background-color: #fee2e2;
  color: #ef4444;
  border: 1px solid #fecaca;
}

.subscribe-button.subscribed:hover {
  background-color: #bfdbfe;
}

/* 반응형 디자인 */
@media (max-width: 768px) {
  .product-container {
    padding: 16px;
  }

  .main-title {
    font-size: 20px;
    margin-bottom: 16px;
  }

  .table-container {
    margin: 0 -16px;
    border-radius: 0;
  }
}

/* 애니메이션 */
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

.product-container {
  animation: fadeIn 0.5s ease-out;
}
</style>