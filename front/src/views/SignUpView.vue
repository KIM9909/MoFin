<template>
  <div>
    <h1>Sign Up Page</h1>
    <form @submit.prevent="signUp">
      <label for="username">아이디</label>
      <input type="text" id="username" v-model.trim="username">
      <br>
      <label for="password1">비밀번호</label>
      <input type="password" id="password1" v-model.trim="password1">
      <br>
      <label for="password2">비밀번호 확인</label>
      <input type="password" id="password2" v-model.trim="password2">
      <br>
      <label for="nickname">닉네임</label>
      <input type="text" id="nickname" v-model.trim="nickname">
      <br>
      <label for="birth">생년월일</label>
      <input type="date" id="birth" v-model="birth">
      <br>
      <label for="preference">관심사</label>
      <input type="text" id="preference" v-model.trim="preference">
      <br>
      <input type="submit" value="회원가입">
    </form>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useAuthStore } from '@/stores/auth'
const store = useAuthStore()

const username = ref('')
const password1 = ref('')
const password2 = ref('')
const nickname = ref('')
const birth = ref('')
const preference = ref([])

const signUp = () => {
  const payload = {
    username: username.value,
    password1: password1.value,
    password2: password2.value,
    nickname: nickname.value,
    birth: birth.value,
    preference: preference.value,  // 배열 그대로 전달
  }
  store.signUp(payload)
}
</script>

<style scoped>

</style>