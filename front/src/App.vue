<script setup>
import { RouterLink, RouterView } from 'vue-router'
import AppNavBar from '@/components/Common/AppNavBar.vue'
import AppFooter from '@/components/Common/AppFooter.vue'
import ChatBot from '@/components/ChatBot/ChatBot.vue'
</script>

<template>
  <div class="app-wrapper">
    <AppNavBar />
    <main class="main-content">
      <RouterView />
    </main>
    <AppFooter />
    <ChatBot />
  </div>
</template>

<style>
html, body {
  height: 100%;
  margin: 0;
  padding: 0;
}

.app-wrapper {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.main-content {
  flex: 1 0 auto;  /* 이 부분이 중요합니다 - 내용이 적어도 footer가 아래에 위치하게 됩니다 */
}
</style>