```vue
<!-- components/DepositProducts.vue -->
<template>
  <div class="product-card">
    <div class="product-header">
      <h3>{{ deposit_product.fin_prdt_nm }}</h3>
      <p class="bank-name">{{ deposit_product.kor_co_nm }}</p>
      <p class="submission-date">공시 제출월: {{ deposit_product.dcls_month }}</p>
    </div>
    
    <button class="detail-btn" @click="showDetails">
      상세 보기
    </button>
  </div>
</template>

<script setup>
import { useDepositStore } from '@/stores/deposit'

const props = defineProps({
  deposit_product: {
    type: Object,
    required: true
  }
})

const emit = defineEmits(['show-detail'])

const showDetails = () => {
  emit('show-detail', { product: props.deposit_product, type: 'deposit' })
}
</script>

<style scoped>
.product-card {
  background: white;
  border-radius: 10px;
  padding: 20px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
}

.product-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.product-header {
  margin-bottom: 15px;
}

.product-header h3 {
  color: #2c662f;
  margin-bottom: 10px;
}

.bank-name {
  color: #666;
  font-size: 0.9em;
  margin-bottom: 5px;
}

.submission-date {
  color: #888;
  font-size: 0.8em;
}

.detail-btn {
  width: 100%;
  padding: 10px;
  background-color: #4caf50;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.detail-btn:hover {
  background-color: #45a049;
}
</style>
```