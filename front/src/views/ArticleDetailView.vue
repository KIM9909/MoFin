<template>
  <div>
    <h1>{{ article.title }}</h1>
    <p>{{ article.content }}</p>
    <RouterLink :to="{ name: 'articleList' }">뒤로가기</RouterLink>
    <button @click="deleteArticle">삭제</button>
    <RouterLink :to="{ name: 'articleUpdate', params: { id: article.id } }">수정</RouterLink>

    <h2>댓글</h2>
    <ul>
      <li v-for="comment in comments" :key="comment.id">
        <p>{{ comment.content }}</p>
        <span>{{ comment.created_at }}</span>
      </li>
    </ul>

    <textarea v-model="newComment" placeholder="댓글을 입력하세요"></textarea>
    <button @click="addComment">댓글 작성</button>
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
const comments = ref([]);
const newComment = ref("");

// 인증 스토어 사용
const authStore = useAuthStore();

// 게시글 데이터 로드
onMounted(() => {
  fetchArticle();
  fetchComments();
});

const fetchArticle = () => {
  axios
    .get(`http://127.0.0.1:8000/articles/articles/${route.params.id}/`)
    .then((response) => {
      article.value = response.data;
    })
    .catch((error) => {
      console.error('게시글 데이터를 가져오는 중 오류가 발생했습니다:', error);
    });
};

const fetchComments = () => {
  // URL을 articles 앱 아래의 comments로 수정
  const url = `http://127.0.0.1:8000/articles/comments/article/${route.params.id}/`;
  console.log("댓글 요청 URL:", url);
  axios
    .get(url)
    .then((response) => {
      comments.value = response.data;
    })
    .catch((error) => {
      console.error("댓글 데이터를 가져오는 중 오류가 발생했습니다:", error);
    });
};

const deleteArticle = () => {
  if (confirm('정말 삭제하시겠습니까?')) {
    axios
      .delete(`http://127.0.0.1:8000/articles/articles/${route.params.id}/`)
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

const addComment = () => {
  if (!newComment.value.trim()) {
    alert("댓글 내용을 입력하세요.");
    return;
  }
  axios
    .post(
      "http://127.0.0.1:8000/articles/comments/",
      { 
        article: article.value.id, 
        content: newComment.value 
      },
      { 
        headers: { Authorization: `Token ${authStore.token}` } 
      }
    )
    .then(() => {
      newComment.value = "";
      fetchComments();
    })
    .catch((error) => {
      console.error("댓글 작성 중 오류가 발생했습니다:", error);
      if (error.response && error.response.status === 401) {
        alert("로그인이 필요합니다.");
        router.push({ name: "login" });
      }
    });
};
</script>
