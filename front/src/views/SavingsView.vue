<template>
  <div>
    <h1>적금 상품 목록</h1>
    <SavingsProducts 
    v-for="savings_product in store.savingsProducts"
    :savings_product="savings_product"
    />
  </div>
</template>

<script setup>
  import SavingsProducts from '@/components/SavingsProducts.vue'
  import { useSavingsStore } from '@/stores/savings'
  const store = useSavingsStore()
  store.getSavings()

</script>

<style scoped>

</style>