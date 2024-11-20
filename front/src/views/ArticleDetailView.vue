<template>
  <div>
    <h1>{{ article.title }}</h1>
    <p>{{ article.content }}</p>
    <RouterLink :to="{ name: 'articleList' }">뒤로가기</RouterLink>
    <button @click="deleteArticle">삭제</button>
    <RouterLink :to="{ name: 'articleUpdate', params: { id: article.id } }">수정</RouterLink>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import axios from 'axios'

const route = useRoute()
const router = useRouter()
const article = ref({})

onMounted(() => {
  axios.get(`http://127.0.0.1:8000/articles/${route.params.id}/`).then(response => {
    article.value = response.data
  })
})

const deleteArticle = () => {
  if (confirm('정말 삭제하시겠습니까?')) {
    axios.delete(`http://127.0.0.1:8000/articles/${route.params.id}/`).then(() => {
      router.push({ name: 'articleList' })
    })
  }
}
</script>
