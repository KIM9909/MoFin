```vue
<!-- components/ProductDetailModal.vue -->
<template>
  <div v-if="isOpen" class="modal-overlay" @click="closeModal">
    <div class="modal-content" @click.stop>
      <div class="modal-header">
        <h3>{{ product?.fin_prdt_nm }}</h3>
        <button class="close-btn" @click="closeModal">&times;</button>
      </div>

      <div class="modal-body">
        <div class="detail-section">
          <h4>상품 정보</h4>
          <p><strong>기타 유의사항:</strong> {{ details?.product?.etc_note }}</p>
          <p><strong>가입 대상:</strong> {{ details?.product?.join_member }}</p>
          <p><strong>가입 방법:</strong> {{ details?.product?.join_way }}</p>
        </div>

        <div class="options-section">
          <h4>금리 정보</h4>
          <div class="options-grid">
            <div v-for="option in details?.options" :key="option.id" class="option-card">
              <p><strong>저축 금리 유형:</strong> {{ option.intr_rate_type_nm }}</p>
              <p><strong>저축 금리:</strong> {{ option.intr_rate }}%</p>
              <p><strong>최고 우대금리:</strong> {{ option.intr_rate2 }}%</p>
              <p><strong>저축 기간:</strong> {{ option.save_trm }}개월</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
defineProps({
  isOpen: Boolean,
  product: Object,
  details: Object
})

const emit = defineEmits(['close'])

const closeModal = () => {
  emit('close')
}
</script>

<style scoped>
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  backdrop-filter: blur(5px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal-content {
  background: white;
  width: 90%;
  max-width: 800px;
  max-height: 90vh;
  border-radius: 12px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
  overflow: hidden;
  animation: modal-appear 0.3s ease-out;
}

.modal-header {
  padding: 20px;
  background-color: #f8f9fa;
  border-bottom: 1px solid #eee;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.modal-header h3 {
  margin: 0;
  color: #2c662f;
}

.close-btn {
  background: none;
  border: none;
  font-size: 24px;
  cursor: pointer;
  color: #666;
  padding: 0 8px;
}

.modal-body {
  padding: 20px;
  overflow-y: auto;
  max-height: calc(90vh - 80px);
}

.detail-section {
  margin-bottom: 30px;
}

.detail-section p {
  margin: 10px 0;
  line-height: 1.6;
}

.options-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 20px;
  margin-top: 15px;
}

.option-card {
  background-color: #f8f9fa;
  border-radius: 8px;
  padding: 15px;
}

.option-card p {
  margin: 8px 0;
}

@keyframes modal-appear {
  from {
    opacity: 0;
    transform: translateY(-20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@media (max-width: 768px) {
  .modal-content {
    width: 95%;
    max-height: 95vh;
  }
  
  .options-grid {
    grid-template-columns: 1fr;
  }
}
</style>
```