<template>
  <div>
    <h1>예금 상품 목록</h1>
    <DepositProducts 
    v-for="deposit_product in store.depositProducts"
    :deposit_product="deposit_product"
    />
  </div>
</template>

<script setup>
  import DepositProducts from '@/components/DepositProducts.vue'
  import { useDepositStore } from '@/stores/deposit'
  const store = useDepositStore()
  store.getDeposits()

</script>

<style scoped>

</style>