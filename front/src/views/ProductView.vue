<template>
  <div class="product-list-container">
    <div class="page-header">
      <h1>금융 상품 목록</h1>
      <p class="subtitle">MoFin에서 제공하는 다양한 금융 상품을 확인하세요</p>
    </div>

    <div class="filter-section">
      <div class="filter-controls">
        <div class="button-group">
          <button 
            @click="showDeposits" 
            :class="{'active-btn': showDepositList}"
            class="filter-btn"
          >
            <span class="btn-icon">💰</span>
            예금 상품
          </button>
          <button 
            @click="showSavings" 
            :class="{'active-btn': !showDepositList}"
            class="filter-btn"
          >
            <span class="btn-icon">🎯</span>
            적금 상품
          </button>
        </div>

        <div class="search-bar">
          <input 
            type="text" 
            v-model="searchBank" 
            placeholder="은행명을 입력하세요" 
            class="bank-search"
          />
          <button 
            @click="clearSearch" 
            class="clear-search" 
            v-if="searchBank"
          >
            ✕
          </button>
        </div>
      </div>
    </div>

    <div v-if="loading" class="loading-container">
      <div class="loading-spinner"></div>
      <p>상품 정보를 불러오는 중...</p>
    </div>

    <div v-else-if="filteredProducts.length === 0" class="no-results">
      <p>검색 결과가 없습니다.</p>
    </div>

    <div v-else class="products-container">
      <div v-if="showDepositList" class="products-grid">
        <DepositProducts
          v-for="deposit_product in paginatedProducts"
          :key="deposit_product.fin_prdt_cd"
          :deposit_product="deposit_product"
          :is-subscribed="subscriptionStore.isSubscribed('deposit', deposit_product.fin_prdt_cd)"
          @show-detail="showProductDetail"
          @toggle-subscription="handleSubscription"
        />
      </div>

      <div v-else class="products-grid">
        <SavingsProducts
          v-for="savings_product in paginatedProducts"
          :key="savings_product.fin_prdt_cd"
          :savings_product="savings_product"
          :is-subscribed="subscriptionStore.isSubscribed('savings', savings_product.fin_prdt_cd)"
          @show-detail="showProductDetail"
          @toggle-subscription="handleSubscription"
        />
      </div>
    </div>

    <!-- Pagination Controls -->
    <div class="pagination-controls" v-if="totalPages > 1">
      <button @click="prevPage" :disabled="currentPage === 1" class="pagination-btn">이전</button>
      <span>{{ currentPage }} / {{ totalPages }}</span>
      <button @click="nextPage" :disabled="currentPage === totalPages" class="pagination-btn">다음</button>
    </div>

    <ProductDetailModal
      :is-open="!!selectedProduct"
      :product="selectedProduct"
      :details="productDetails"
      :is-subscribed="selectedProduct ? subscriptionStore.isSubscribed(
        selectedProduct.type, 
        selectedProduct.fin_prdt_cd
      ) : false"
      @close="closeModal"
      @toggle-subscription="handleSubscription"
    />
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import DepositProducts from '@/components/DepositProducts.vue'
import SavingsProducts from '@/components/SavingsProducts.vue'
import ProductDetailModal from '@/components/ProductDetailModal.vue'
import { useDepositStore } from '@/stores/deposit'
import { useSavingsStore } from '@/stores/savings'
import { useSubscriptionStore } from '@/stores/subscription'
import { useAuthStore } from '@/stores/auth'

const store = useDepositStore()
const savingsStore = useSavingsStore()
const subscriptionStore = useSubscriptionStore()
const authStore = useAuthStore()
const loading = ref(false)
const searchBank = ref('')

const showDepositList = ref(true)
const selectedProduct = ref(null)
const productDetails = ref(null)

const currentPage = ref(1)
const itemsPerPage = 12

// 검색어에 따른 필터링된 상품 목록
const filteredProducts = computed(() => {
  const products = showDepositList.value ? store.depositProducts : savingsStore.savingsProducts
  if (!searchBank.value) return products

  const searchTerm = searchBank.value.toLowerCase()
  return products.filter(product => 
    product.kor_co_nm.toLowerCase().includes(searchTerm)
  )
})

// 페이지네이션된 필터링 상품 목록
const paginatedProducts = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage
  const end = start + itemsPerPage
  return filteredProducts.value.slice(start, end)
})

const totalPages = computed(() => {
  return Math.ceil(filteredProducts.value.length / itemsPerPage)
})

// 검색어가 변경될 때마다 첫 페이지로 이동
watch(searchBank, () => {
  currentPage.value = 1
})

const clearSearch = () => {
  searchBank.value = ''
}

const showDeposits = async () => {
  try {
    loading.value = true
    showDepositList.value = true
    currentPage.value = 1
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
    showDepositList.value = false
    currentPage.value = 1
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
    selectedProduct.value = { ...product, type }
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

const handleSubscription = async (productType, productId) => {
  if (!authStore.isLogin) {
    alert('로그인이 필요한 서비스입니다.')
    return
  }

  try {
    const result = await subscriptionStore.toggleSubscription(productType, productId)
    alert(result.message)
  } catch (error) {
    console.error('가입 처리 중 오류:', error)
    alert('가입 처리 중 오류가 발생했습니다.')
  }
}

const closeModal = () => {
  selectedProduct.value = null
  productDetails.value = null
}

const prevPage = () => {
  if (currentPage.value > 1) {
    currentPage.value--
  }
}

const nextPage = () => {
  if (currentPage.value < totalPages.value) {
    currentPage.value++
  }
}

onMounted(async () => {
  if (authStore.isLogin) {
    try {
      await subscriptionStore.fetchSubscriptions()
    } catch (error) {
      console.error('가입 정보 로딩 실패:', error)
    }
  }
  await showDeposits()
})
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

.filter-controls {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 2rem;
}

.button-group {
  display: flex;
  gap: 1rem;
}

.search-bar {
  position: relative;
  flex: 1;
  max-width: 300px;
}

.bank-search {
  width: 100%;
  padding: 0.75rem;
  border: 2px solid #e9ecef;
  border-radius: 8px;
  font-size: 1rem;
  transition: all 0.3s ease;
}

.bank-search:focus {
  outline: none;
  border-color: #2c662f;
  box-shadow: 0 0 0 3px rgba(44, 102, 47, 0.1);
}

.clear-search {
  position: absolute;
  right: 10px;
  top: 50%;
  transform: translateY(-50%);
  background: none;
  border: none;
  color: #666;
  cursor: pointer;
  padding: 5px;
}

.clear-search:hover {
  color: #333;
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
  white-space: nowrap;
}

.filter-btn:hover {
  background-color: #e9ecef;
  transform: translateY(-2px);
}

.filter-btn.active-btn {
  background-color: #5c9c5f;
  color: white;
  border-color: #5c9c5f;
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
  grid-template-columns: repeat(3, 1fr);
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

.no-results {
  text-align: center;
  padding: 2rem;
  color: #666;
  background: #f8f9fa;
  border-radius: 8px;
  margin: 1rem 0;
}

.pagination-controls {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 1rem;
  margin-top: 2rem;
  padding: 1rem 0;
}

.pagination-btn {
  padding: 0.5rem 1rem;
  border: none;
  background-color: #2c3e50;
  color: white;
  border-radius: 8px;
  cursor: pointer;
  transition: background-color 0.3s;
  font-size: 0.9rem;
}

.pagination-btn:hover:not(:disabled) {
  background-color: #1e2a37;
}

.pagination-btn:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}

.pagination-controls span {
  color: #2c3e50;
  font-weight: 500;
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

@media (max-width: 1024px) {
  .products-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 768px) {
  .product-list-container {
    padding: 1rem;
  }

  .page-header h1 {
    font-size: 2rem;
  }

  .filter-controls {
    flex-direction: column;
    gap: 1rem;
  }

  .search-bar {
    width: 100%;
    max-width: none;
  }

  .button-group {
    width: 100%;
  }

  .filter-btn {
    flex: 1;
    justify-content: center;
    padding: 0.75rem 1rem;
    font-size: 0.95rem;
  }

  .products-grid {
    grid-template-columns: 1fr;
    gap: 1rem;
  }

  .pagination-controls {
    gap: 0.5rem;
  }

  .pagination-btn {
    padding: 0.5rem 0.75rem;
    font-size: 0.85rem;
  }
}

@media (max-width: 480px) {
  .page-header h1 {
    font-size: 1.75rem;
  }

  .subtitle {
    font-size: 1rem;
  }

  .filter-section {
    padding: 1rem;
  }

  .bank-search {
    padding: 0.6rem;
    font-size: 0.95rem;
  }
}
</style>