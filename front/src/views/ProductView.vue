```vue
<!-- views/ProductList.vue -->
<template>
  <div>
    <h1>상품 목록</h1>

    <!-- 상품 조회 버튼들 -->
    <div class="button-group">
      <button @click="showAll" :class="{'active-btn': showAllProducts}">
        전체 상품 조회
      </button>
      <button @click="showDeposits" :class="{'active-btn': showDepositList && !showAllProducts}">
        예금 상품 조회
      </button>
      <button @click="showSavings" :class="{'active-btn': !showDepositList && !showAllProducts}">
        적금 상품 조회
      </button>
    </div>

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

const showDepositList = ref(true)
const showAllProducts = ref(true)
const selectedProduct = ref(null)
const productDetails = ref(null)

const showAll = async () => {
  showAllProducts.value = true
  await Promise.all([
    store.getDeposits(),
    savingsStore.getSavings()
  ])
}

const showDeposits = async () => {
  showAllProducts.value = false
  showDepositList.value = true
  await store.getDeposits()
}

const showSavings = async () => {
  showAllProducts.value = false
  showDepositList.value = false
  await savingsStore.getSavings()
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
.button-group {
  margin: 20px 0;
  display: flex;
  gap: 10px;
  justify-content: center;
}

button {
  padding: 12px 20px;
  background-color: #4caf50;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-size: 1rem;
  transition: all 0.3s ease;
}

button:hover {
  background-color: #45a049;
  transform: translateY(-2px);
}

.active-btn {
  background-color: #2c662f;
  box-shadow: 0 2px 4px rgba(0,0,0,0.2);
}

h1 {
  text-align: center;
  color: #333;
  margin-bottom: 30px;
}

.products-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
  padding: 20px;
}

@media (max-width: 768px) {
  .button-group {
    flex-direction: column;
    padding: 0 20px;
  }

  button {
    width: 100%;
  }
}
</style>
```