<template>
  <div>
    <h1>게시글 수정</h1>
    <form @submit.prevent="updateArticle">
      <label for="title">제목:</label>
      <input id="title" v-model="title" />
      <label for="content">내용:</label>
      <textarea id="content" v-model="content"></textarea>
      <button type="submit">수정</button>
    </form>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import axios from 'axios'

const route = useRoute()
const router = useRouter()
const title = ref('')
const content = ref('')

onMounted(() => {
  axios.get(`http://127.0.0.1:8000/articles/${route.params.id}/`)
    .then(response => {
      title.value = response.data.title;
      content.value = response.data.content;
    })
    .catch(error => {
      console.error('게시글 데이터를 가져오는 중 오류가 발생했습니다:', error);
    });
});

const updateArticle = () => {
  axios.put(`http://127.0.0.1:8000/articles/${route.params.id}/`, {
    title: title.value,
    content: content.value,
  })
  .then(() => {
    router.push({ name: 'articleDetail', params: { id: route.params.id } });
  })
  .catch(error => {
    console.error('게시글 수정 중 오류가 발생했습니다:', error);
  });
};

</script>
