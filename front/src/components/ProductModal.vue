<template>
  <div v-if="isOpen" class="modal-overlay" @click="closeModal">
    <div class="modal-content" @click.stop>
      <div class="modal-header">
        <h2>{{ product?.fin_prdt_nm }}</h2>
        <button class="close-btn" @click="closeModal">×</button>
      </div>

      <div class="modal-body">
        <div class="section">
          <h3>상품 정보</h3>
          <div class="info-grid">
            <div class="info-item">
              <label>기타 유의사항:</label>
              <p>{{ details?.product?.etc_note }}</p>
            </div>
            <div class="info-item">
              <label>가입 대상:</label>
              <p>{{ details?.product?.join_member }}</p>
            </div>
            <div class="info-item">
              <label>가입 방법:</label>
              <p>{{ details?.product?.join_way }}</p>
            </div>
          </div>
        </div>

        <div class="section">
          <h3>금리 정보</h3>
          <div class="rates-grid">
            <div v-for="option in details?.options" :key="option.id" class="rate-card">
              <div class="rate-info">
                <div class="rate-type">
                  <span class="label">저축 금리 유형:</span>
                  <span class="value">{{ option.intr_rate_type_nm }}</span>
                </div>
                <div class="rate-details">
                  <div class="rate">
                    <span class="label">저축 금리:</span>
                    <span class="value">{{ option.intr_rate }}%</span>
                  </div>
                  <div class="rate">
                    <span class="label">우대금리:</span>
                    <span class="value">{{ option.intr_rate2 }}%</span>
                  </div>
                  <div class="term">
                    <span class="label">저축 기간:</span>
                    <span class="value">{{ option.save_trm }}개월</span>
                  </div>
                </div>
              </div>
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
  background: rgba(0, 0, 0, 0.5);
  backdrop-filter: blur(4px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal-content {
  background: white;
  width: 90%;
  max-width: 800px;
  border-radius: 12px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
  max-height: 90vh;
  overflow: hidden;
}

.modal-header {
  padding: 1rem 1.5rem;
  border-bottom: 1px solid #eef0f2;
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: #f8f9fa;
}

.modal-header h2 {
  margin: 0;
  font-size: 1.5rem;
  color: #2c662f;
}

.close-btn {
  background: none;
  border: none;
  font-size: 1.8rem;
  color: #666;
  cursor: pointer;
  padding: 0.5rem;
}

.modal-body {
  padding: 1.5rem;
  overflow-y: auto;
  max-height: calc(90vh - 70px);
}

.section {
  margin-bottom: 2rem;
}

.section h3 {
  color: #2c662f;
  margin-bottom: 1rem;
  font-size: 1.2rem;
}

.info-grid {
  display: grid;
  gap: 1rem;
}

.info-item {
  background: #f8f9fa;
  padding: 1rem;
  border-radius: 8px;
}

.info-item label {
  font-weight: 600;
  display: block;
  margin-bottom: 0.5rem;
  color: #495057;
}

.info-item p {
  margin: 0;
  color: #2c3e50;
  line-height: 1.5;
}

.rates-grid {
  display: grid;
  gap: 1rem;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
}

.rate-card {
  background: #f8f9fa;
  padding: 1rem;
  border-radius: 8px;
}

.rate-type {
  margin-bottom: 1rem;
  padding-bottom: 0.5rem;
  border-bottom: 1px solid #dee2e6;
}

.rate-details {
  display: grid;
  gap: 0.5rem;
}

.label {
  font-weight: 600;
  color: #495057;
  margin-right: 0.5rem;
}

.value {
  color: #2c3e50;
}

@media (max-width: 768px) {
  .modal-content {
    width: 95%;
    margin: 1rem;
  }

  .rates-grid {
    grid-template-columns: 1fr;
  }
}
</style>

