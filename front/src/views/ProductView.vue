<template>
  <div class="product-list-container">
    <div class="page-header">
      <h1>금융 상품 목록</h1>
      <p class="subtitle">MoFin에서 제공하는 다양한 금융 상품을 확인하세요</p>
    </div>

    <!-- 상품 조회 버튼들 -->
    <div class="filter-section">
      <div class="button-group">
        <button 
          @click="showAll" 
          :class="{'active-btn': showAllProducts}"
          class="filter-btn"
        >
          <span class="btn-icon">🏦</span>
          전체 상품
        </button>
        <button 
          @click="showDeposits" 
          :class="{'active-btn': showDepositList && !showAllProducts}"
          class="filter-btn"
        >
          <span class="btn-icon">💰</span>
          예금 상품
        </button>
        <button 
          @click="showSavings" 
          :class="{'active-btn': !showDepositList && !showAllProducts}"
          class="filter-btn"
        >
          <span class="btn-icon">🎯</span>
          적금 상품
        </button>
      </div>
    </div>

    <!-- 로딩 인디케이터 -->
    <div v-if="loading" class="loading-container">
      <div class="loading-spinner"></div>
      <p>상품 정보를 불러오는 중...</p>
    </div>

    <!-- 상품 그리드 -->
    <div v-else class="products-container">
      <!-- 전체 상품 표시 -->
      <div v-if="showAllProducts" class="products-grid">
        <DepositProducts
          v-for="deposit_product in store.depositProducts"
          :key="`deposit-${deposit_product.fin_prdt_cd}`"
          :deposit_product="deposit_product"
          @show-detail="showProductDetail"
        />
        <SavingsProducts
          v-for="savings_product in savingsStore.savingsProducts"
          :key="`savings-${savings_product.fin_prdt_cd}`"
          :savings_product="savings_product"
          @show-detail="showProductDetail"
        />
      </div>

      <!-- 예금 상품만 표시 -->
      <div v-else-if="showDepositList" class="products-grid">
        <DepositProducts
          v-for="deposit_product in store.depositProducts"
          :key="deposit_product.fin_prdt_cd"
          :deposit_product="deposit_product"
          @show-detail="showProductDetail"
        />
      </div>

      <!-- 적금 상품만 표시 -->
      <div v-else class="products-grid">
        <SavingsProducts
          v-for="savings_product in savingsStore.savingsProducts"
          :key="savings_product.fin_prdt_cd"
          :savings_product="savings_product"
          @show-detail="showProductDetail"
        />
      </div>
    </div>

    <!-- 상세 정보 모달 -->
    <ProductDetailModal
      :is-open="!!selectedProduct"
      :product="selectedProduct"
      :details="productDetails"
      @close="closeModal"
    />
  </div>
</template>

<script setup>
import { ref } from 'vue'
import DepositProducts from '@/components/DepositProducts.vue'
import SavingsProducts from '@/components/SavingsProducts.vue'
import ProductDetailModal from '@/components/ProductDetailModal.vue'
import { useDepositStore } from '@/stores/deposit'
import { useSavingsStore } from '@/stores/savings'

const store = useDepositStore()
const savingsStore = useSavingsStore()
const loading = ref(false)

const showDepositList = ref(true)
const showAllProducts = ref(true)
const selectedProduct = ref(null)
const productDetails = ref(null)

const showAll = async () => {
  try {
    loading.value = true
    showAllProducts.value = true
    await Promise.all([
      store.getDeposits(),
      savingsStore.getSavings()
    ])
  } catch (error) {
    console.error('상품 데이터 로딩 실패:', error)
    alert('상품 정보를 불러오는데 실패했습니다.')
  } finally {
    loading.value = false
  }
}

const showDeposits = async () => {
  try {
    loading.value = true
    showAllProducts.value = false
    showDepositList.value = true
    await store.getDeposits()
  } catch (error) {
    console.error('예금 상품 로딩 실패:', error)
    alert('예금 상품 정보를 불러오는데 실패했습니다.')
  } finally {
    loading.value = false
  }
}

const showSavings = async () => {
  try {
    loading.value = true
    showAllProducts.value = false
    showDepositList.value = false
    await savingsStore.getSavings()
  } catch (error) {
    console.error('적금 상품 로딩 실패:', error)
    alert('적금 상품 정보를 불러오는데 실패했습니다.')
  } finally {
    loading.value = false
  }
}

const showProductDetail = async ({ product, type }) => {
  try {
    selectedProduct.value = product
    if (type === 'deposit') {
      productDetails.value = await store.getDepositDetails(product.fin_prdt_cd)
    } else {
      productDetails.value = await savingsStore.getSavingsDetails(product.fin_prdt_cd)
    }
  } catch (error) {
    console.error('상품 상세 정보를 가져오는데 실패했습니다:', error)
    selectedProduct.value = null
    productDetails.value = null
    alert('상품 정보를 불러오는데 실패했습니다. 다시 시도해주세요.')
  }
}

const closeModal = () => {
  selectedProduct.value = null
  productDetails.value = null
}
</script>

<style scoped>
.product-list-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem;
}

.page-header {
  text-align: center;
  margin-bottom: 3rem;
  animation: fadeIn 0.5s ease-out;
}

.page-header h1 {
  color: #2c3e50;
  font-size: 2.5rem;
  font-weight: 700;
  margin-bottom: 0.5rem;
}

.subtitle {
  color: #666;
  font-size: 1.1rem;
}

.filter-section {
  background: white;
  padding: 1.5rem;
  border-radius: 12px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  margin-bottom: 2rem;
}

.button-group {
  display: flex;
  gap: 1rem;
  justify-content: center;
}

.filter-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1.5rem;
  background-color: #f8f9fa;
  color: #2c3e50;
  border: 2px solid #e9ecef;
  border-radius: 8px;
  font-size: 1rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
}

.filter-btn:hover {
  background-color: #e9ecef;
  transform: translateY(-2px);
}

.filter-btn.active-btn {
  background-color: #2c662f;
  color: white;
  border-color: #2c662f;
  box-shadow: 0 2px 4px rgba(44, 102, 47, 0.2);
}

.btn-icon {
  font-size: 1.2rem;
}

.products-container {
  animation: fadeIn 0.5s ease-out;
}

.products-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 1.5rem;
  padding: 0.5rem;
}

.loading-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 3rem;
  text-align: center;
  color: #666;
}

.loading-spinner {
  width: 40px;
  height: 40px;
  border: 4px solid #f3f3f3;
  border-top: 4px solid #2c662f;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin-bottom: 1rem;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
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

/* 반응형 디자인 */
@media (max-width: 768px) {
  .product-list-container {
    padding: 1rem;
  }

  .page-header h1 {
    font-size: 2rem;
  }

  .button-group {
    flex-direction: column;
  }

  .filter-btn {
    width: 100%;
    justify-content: center;
  }

  .products-grid {
    grid-template-columns: 1fr;
    gap: 1rem;
  }
}
</style>