<template>
  <div>
    <h1>예금 상품 목록</h1>
    <DepositProducts 
      v-for="deposit_product in store.depositProducts" 
      :key="deposit_product.fin_prdt_cd" 
      :deposit_product="deposit_product"
    />
  </div>
</template>

<script setup>
  import DepositProducts from '@/components/DepositProducts.vue'
  import { useDepositStore } from '@/stores/deposit'
  const store = useDepositStore()

  // 비동기 데이터 가져오기
  const fetchDeposits = async () => {
    await store.getDeposits()
  }

  // 페이지가 로드될 때 데이터 가져오기
  fetchDeposits()
</script>

<style scoped>

</style>
