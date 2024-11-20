<template>
  <div>
    <h1>새 게시글 작성</h1>
    <form @submit.prevent="createArticle">
      <label for="title">제목:</label>
      <input id="title" v-model="title" />
      <label for="content">내용:</label>
      <textarea id="content" v-model="content"></textarea>
      <button type="submit">작성</button>
    </form>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import axios from 'axios';
import { useRouter } from 'vue-router';

axios.defaults.baseURL = 'http://127.0.0.1:8000'; // Django 서버 주소

const title = ref('');
const content = ref('');
const router = useRouter();

const createArticle = () => {
  axios.post('/articles/', { title: title.value, content: content.value })
    .then(() => {
      router.push({ name: 'articleList' });
    })
    .catch(error => {
      console.error('게시글 생성 중 오류가 발생했습니다:', error);
    });
};
</script>

