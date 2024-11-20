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
import { ref, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { useAuthStore } from '@/stores/auth';
import axios from 'axios';

const route = useRoute();
const router = useRouter();
const article = ref({});

// 인증 스토어 사용
const authStore = useAuthStore();

onMounted(() => {
  axios
    .get(`http://127.0.0.1:8000/articles/${route.params.id}/`)
    .then((response) => {
      article.value = response.data;
    })
    .catch((error) => {
      console.error('게시글 데이터를 가져오는 중 오류가 발생했습니다:', error);
    });
});

const deleteArticle = () => {
  if (confirm('정말 삭제하시겠습니까?')) {
    axios
      .delete(`http://127.0.0.1:8000/articles/${route.params.id}/`)
      .then(() => {
        router.push({ name: 'articleList' });
      })
      .catch((error) => {
        console.error('게시글 삭제 중 오류가 발생했습니다:', error);
        if (error.response && error.response.status === 401) {
          alert('로그인이 필요합니다.');
          router.push({ name: 'login' }); // 로그인 페이지로 이동
        }
      });
  }
};
</script>
