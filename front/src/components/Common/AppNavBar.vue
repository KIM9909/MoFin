<template>
  <div>
    <RouterLink :to="{ name: 'home' }">Home</RouterLink>
    <span> | </span>
    <RouterLink :to="{ name: 'signIn' }">SignIn</RouterLink>
    <span> | </span>
    <RouterLink :to="{ name: 'signUp' }">SignUp</RouterLink>
  </div>
</template>

<script setup>
import { RouterLink } from 'vue-router'

</script>

<style scoped>

</style>