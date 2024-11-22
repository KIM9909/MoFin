<template>
  <div class="product-card">
    <div class="product-header">
      <h3>{{ savings_product.fin_prdt_nm }}</h3>
      <p class="bank-name">{{ savings_product.kor_co_nm }}</p>
      <p class="submission-date">공시 제출월: {{ savings_product.dcls_month }}</p>
    </div>
    
    <div class="button-group">
      <button class="detail-btn" @click="showDetails">
        상세 보기
      </button>
      <button 
        class="subscribe-btn" 
        :class="{ 'subscribed': isSubscribed }"
        @click="handleSubscribe"
      >
        {{ isSubscribed ? '가입 취소' : '가입하기' }}
      </button>
    </div>
  </div>
</template>

<script setup>
const props = defineProps({
  savings_product: {
    type: Object,
    required: true
  },
  isSubscribed: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['show-detail', 'toggle-subscription'])

const showDetails = () => {
  emit('show-detail', { product: props.savings_product, type: 'savings' })
}

const handleSubscribe = () => {
  emit('toggle-subscription', 'savings', props.savings_product.fin_prdt_cd)
}
</script>

<style scoped>
.product-card {
  border: 1px solid rgb(180, 180, 180);
  padding: 1.2rem;
  border-radius: 12px;
}

.button-group {
  display: flex;
  gap: 10px;
}

.detail-btn, .subscribe-btn {
  flex: 1;
  padding: 10px;
  border-radius: 5px;
  cursor: pointer;
  transition: all 0.3s;
}

.detail-btn {
  background-color: #f3f4f6;
  color: #374151;
  border: 1px solid #d1d5db;
}

.detail-btn:hover {
  opacity: 0.9;
}

.subscribe-btn {
  background-color: #5c9c5f;
  color: rgb(255, 255, 255);
  border: 1px solid rgb(93, 167, 93);
}

.subscribe-btn.subscribed {
  background-color: #fee2e2;
  color: #ef4444;
  border: 1px solid #fecaca;
}

.subscribe-btn:hover {
  opacity: 0.9;
}
</style>