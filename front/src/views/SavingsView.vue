<template>
  <div>
    <h1>적금 상품 목록</h1>
    <!-- 적금 상품 목록을 반복하여 표시 -->
    <SavingsProducts 
      v-for="savings_product in store.savingsProducts"
      :key="savings_product.fin_prdt_cd" 
      :savings_product="savings_product"
    />
  </div>
</template>

<script setup>
  import SavingsProducts from '@/components/SavingsProducts.vue' // 적금 상품 컴포넌트 임포트
  import { useSavingsStore } from '@/stores/savings' // Pinia store 임포트

  const store = useSavingsStore() // store 사용
  store.getSavings() // 적금 상품 데이터를 가져오는 함수 호출
</script>

<style scoped>
/* 스타일을 추가하고 싶으면 여기에 작성 */
</style>
