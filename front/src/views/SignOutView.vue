<template>
  <div>
    <h1>로그아웃</h1>
    <p>로그아웃 되었습니다. 메인 페이지로 이동합니다.</p>
  </div>
</template>

<script setup>
import { useAuthStore } from '@/stores/auth'
import { useRouter } from 'vue-router'
import { onMounted } from 'vue'

const authStore = useAuthStore()
const router = useRouter()

onMounted(() => {
  authStore.logout()
  setTimeout(() => {
    router.push({ name: 'home' })
  }, 1000) // 2초 후 홈으로 리다이렉트
})
</script>

<style scoped>
h1 {
  color: red;
}
</style>
