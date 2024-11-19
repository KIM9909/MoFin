<template>
  <div>
    <h1>LogIn Page</h1>
    <form @submit.prevent="signIn">
      <label for="username">username</label>
      <input type="text" id="username" v-model.trim="username">
      <br>
      <label for="password">password</label>
      <input type="password" id="password" v-model.trim="password">
      <br>
      <input type="submit" value="LogIn">
    </form>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useAuthStore } from '@/stores/auth'
const username = ref(null)
const password = ref(null)

const store = useAuthStore()

const signIn = function () {
  const payload = {
    username: username.value,
    password: password.value,
  }
  store.signIn(payload)
}
</script>

<style scoped>

</style>
