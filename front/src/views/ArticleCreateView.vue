<template>
  <div>
    <h1>새 게시글 작성</h1>
    <form @submit.prevent="createArticle">
      <label for="title">제목:</label>
      <input id="title" v-model="title" required />
      <label for="content">내용:</label>
      <textarea id="content" v-model="content" required></textarea>
      <button type="submit">작성</button>
    </form>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import axios from 'axios';
import { useRouter } from 'vue-router';
import { useAuthStore } from '@/stores/auth';

const title = ref('');
const content = ref('');
const router = useRouter();
const store = useAuthStore();

const createArticle = () => {
  if (!store.isLogin) {
    window.alert('로그인이 필요합니다.');
    router.push({ name: 'signIn' });
    return;
  }

  axios({
    method: 'post',
    url: 'http://127.0.0.1:8000/articles/articles/',
    data: {
      title: title.value,
      content: content.value
    },
    headers: {
      Authorization: `Token ${store.token}`
    }
  })
    .then(() => {
      router.push({ name: 'articleList' });
    })
    .catch((error) => {
      if (error.response?.status === 401) {
        window.alert('로그인이 필요합니다.');
        router.push({ name: 'signIn' });
      } else {
        console.error('게시글 생성 중 오류가 발생했습니다:', error);
      }
    });
};
</script>