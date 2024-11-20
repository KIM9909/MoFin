<template>
  <div>
    <h1>상품 목록</h1>

    <!-- 예금 상품과 적금 상품을 조회하는 버튼 -->
    <div>
      <button @click="showDeposits" :class="{'active-btn': showDepositList}">예금 상품 조회</button>
      <button @click="showSavings" :class="{'active-btn': !showDepositList}">적금 상품 조회</button>
    </div>

    <!-- 예금 상품 컴포넌트 -->
    <div v-if="showDepositList">
      <h2>예금 상품 목록</h2>
      <DepositProducts
        v-for="deposit_product in store.depositProducts"
        :key="deposit_product.fin_prdt_cd"
        :deposit_product="deposit_product"
      />
    </div>

    <!-- 적금 상품 컴포넌트 -->
    <div v-if="!showDepositList">
      <h2>적금 상품 목록</h2>
      <SavingsProducts
        v-for="savings_product in savingsStore.savingsProducts"
        :key="savings_product.fin_prdt_cd"
        :savings_product="savings_product"
      />
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import DepositProducts from '@/components/DepositProducts.vue'
import SavingsProducts from '@/components/SavingsProducts.vue'
import { useDepositStore } from '@/stores/deposit'
import { useSavingsStore } from '@/stores/savings'

// Deposit Store와 Savings Store를 사용
const store = useDepositStore()
const savingsStore = useSavingsStore()

// 상품 목록을 표시할지 여부를 제어하는 변수
const showDepositList = ref(true)

// 예금 상품 조회 함수
const showDeposits = async () => {
  showDepositList.value = true
  await store.getDeposits() // 예금 상품 데이터 가져오기
}

// 적금 상품 조회 함수
const showSavings = async () => {
  showDepositList.value = false
  await savingsStore.getSavings() // 적금 상품 데이터 가져오기
}

// 페이지가 로드될 때 예금 상품을 가져옵니다
onMounted(() => {
  showDeposits() // 기본적으로 예금 상품 목록을 보여줌
})
</script>

<style scoped>
/* 버튼 스타일 */
button {
  padding: 10px;
  margin: 5px;
  background-color: #4caf50;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

button:hover {
  background-color: #45a049;
}

/* 활성화된 버튼 강조 */
.active-btn {
  background-color: #45a049;
}
</style>
