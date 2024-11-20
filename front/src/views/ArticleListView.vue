<template>
  <div class="container my-4">
    <h1 class="mb-4">게시글 리스트</h1>

    <div class="mb-3">
      <RouterLink 
        v-if="store.isLogin"
        :to="{ name: 'articleCreate' }"
        class="btn btn-primary"
      >
        새 게시글 작성
      </RouterLink>
      <p v-else class="text-muted">게시글을 작성하려면 로그인해주세요.</p>
    </div>

    <div class="row">
      <div v-if="articles.length === 0" class="col-12">
        <p class="text-center text-muted">게시글이 없습니다.</p>
      </div>
      <div v-else v-for="article in articles" :key="article.id" class="col-md-4 mb-4">
        <div class="card h-100">
          <div class="card-body">
            <h5 class="card-title">
              <RouterLink
                v-if="article.id"
                :to="{ name: 'articleDetail', params: { id: article.id } }"
                class="text-decoration-none text-dark"
              >
                {{ article.title }}
              </RouterLink>
              <span v-else>잘못된 데이터</span>
            </h5>
            <p class="card-text text-truncate">
              {{ article.content || '내용이 없습니다.' }}
            </p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';
import { useAuthStore } from '@/stores/auth';

const articles = ref([]);
const store = useAuthStore();

onMounted(() => {
  axios({
    method: 'get',
    url: 'http://127.0.0.1:8000/articles/articles/',
    headers: store.token ? { Authorization: `Token ${store.token}` } : {}
  })
    .then((response) => {
      if (Array.isArray(response.data)) {
        articles.value = response.data;
      } else if (response.data.results) {
        articles.value = response.data.results;
      } else {
        console.error('올바르지 않은 API 데이터 구조:', response.data);
        articles.value = [];
      }
    })
    .catch((error) => {
      console.error('게시글 데이터를 가져오는 중 오류가 발생했습니다:', error);
    });
});
</script>
