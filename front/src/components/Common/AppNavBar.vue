<template>
  <div>
    <RouterLink :to="{ name: 'home' }">MoFin</RouterLink>
    <span> | </span>
    <RouterLink :to="{ name: 'signIn' }">로그인</RouterLink>
    <span> | </span>
    <RouterLink :to="{ name: 'signUp' }">회원가입</RouterLink>
    <span> | </span>
    <RouterLink :to="{ name: 'location' }">근처 은행 찾기</RouterLink>
    <span> | </span>
    <RouterLink :to="{ name: 'exchangeRate' }">환율 계산</RouterLink>
    <span> | </span>
    <RouterLink :to="{ name: 'products' }">상품 조회</RouterLink>
  </div>
</template>

<script setup>
import { RouterLink } from 'vue-router'

</script>

<style scoped>

</style>