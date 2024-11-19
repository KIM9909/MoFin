<script setup>
import { RouterLink, RouterView } from 'vue-router'
import AppNavBar from '@/components/Common/AppNavBar.vue'
import HomeView from '@/views/HomeView.vue'

</script>

<template>
  <AppNavBar />
  <div>
    <h1>MoFin MoFin MoFin</h1>
  </div>
  <RouterView />
</template>