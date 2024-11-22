<template>
  <div class="article-container">
    <div class="article-header">
      <h1>커뮤니티</h1>
      <p class="subtitle">MoFin 회원들과 정보를 공유해보세요</p>
    </div>

    <div class="action-bar">
      <RouterLink 
        v-if="store.isLogin"
        :to="{ name: 'articleCreate' }"
        class="create-btn"
      >
        <span class="btn-icon">+</span>
        새 게시글 작성
      </RouterLink>
      <div v-else class="login-prompt">
        <span class="lock-icon">🔒</span>
        게시글을 작성하려면 로그인해주세요.
      </div>
    </div>

    <div class="articles-grid">
      <div v-if="articles.length === 0" class="no-articles">
        <div class="empty-state">
          <span class="empty-icon">📝</span>
          <p>아직 게시글이 없습니다.</p>
          <p class="empty-subtitle">첫 게시글의 주인공이 되어보세요!</p>
        </div>
      </div>
      
      <div v-else class="article-cards">
        <div v-for="article in articles" :key="article.id" class="article-card">
          <div class="card-content">
            <RouterLink
              v-if="article.id"
              :to="{ name: 'articleDetail', params: { id: article.id } }"
              class="card-link"
            >
              <h3 class="article-title">{{ article.title }}</h3>
              <p class="article-preview">{{ article.content || '내용이 없습니다.' }}</p>
            </RouterLink>
            <div class="card-footer">
              <button 
                @click="toggleLike(article)"
                :class="['like-button', { 'liked': article.is_liked }]"
                :disabled="!store.isLogin"
              >
                <span class="heart-icon">{{ article.is_liked ? '❤️' : '🤍' }}</span>
                <span class="like-count">{{ article.like_count }}</span>
              </button>
              <RouterLink
                v-if="article.id"
                :to="{ name: 'articleDetail', params: { id: article.id } }"
                class="read-more"
              >
                자세히 보기 →
              </RouterLink>
            </div>
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
import { RouterLink } from 'vue-router';

const articles = ref([]);
const store = useAuthStore();

const fetchArticles = async () => {
  try {
    const response = await axios({
      method: 'get',
      url: 'http://127.0.0.1:8000/articles/articles/',
      headers: store.token ? { Authorization: `Token ${store.token}` } : {}
    });
    
    if (Array.isArray(response.data)) {
      articles.value = response.data;
    } else if (response.data.results) {
      articles.value = response.data.results;
    }
  } catch (error) {
    console.error('게시글 데이터를 가져오는 중 오류가 발생했습니다:', error);
  }
};

const toggleLike = async (article) => {
  if (!store.isLogin) {
    alert('좋아요를 누르려면 로그인이 필요합니다.');
    return;
  }

  try {
    const response = await axios({
      method: 'post',
      url: `http://127.0.0.1:8000/articles/articles/${article.id}/like/`,
      headers: { Authorization: `Token ${store.token}` }
    });
    
    article.is_liked = response.data.is_liked;
    article.like_count = response.data.like_count;
  } catch (error) {
    console.error('좋아요 처리 중 오류가 발생했습니다:', error);
    alert('좋아요 처리 중 오류가 발생했습니다.');
  }
};

onMounted(() => {
  fetchArticles();
});
</script>

<style scoped>
.article-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem;
}

.article-header {
  text-align: center;
  margin-bottom: 3rem;
}

.article-header h1 {
  color: #2c3e50;
  font-size: 2.5rem;
  font-weight: 700;
  margin-bottom: 0.5rem;
}

.subtitle {
  color: #666;
  font-size: 1.1rem;
}

.action-bar {
  display: flex;
  justify-content: flex-end;
  margin-bottom: 2rem;
}

.create-btn {
  background-color: #2c662f;
  color: white;
  padding: 0.8rem 1.5rem;
  border-radius: 8px;
  text-decoration: none;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  transition: all 0.3s ease;
}

.create-btn:hover {
  background-color: #235024;
  transform: translateY(-2px);
}

.btn-icon {
  font-size: 1.2rem;
  font-weight: bold;
}

.login-prompt {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: #666;
  padding: 0.8rem 1.5rem;
  background-color: #f8f9fa;
  border-radius: 8px;
}

.lock-icon {
  font-size: 1.2rem;
}

.articles-grid {
  margin-top: 2rem;
}

.article-cards {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 1.5rem;
}

.article-card {
  background: white;
  border-radius: 12px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
  transition: all 0.3s ease;
  height: 100%;
  border: 1px solid rgb(180, 180, 180);
}

.article-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 15px rgba(0, 0, 0, 0.1);
}

.card-link {
  text-decoration: none;
  color: inherit;
  display: block;
  height: 100%;
}

.card-content {
  padding: 1.5rem;
  height: 100%;
  display: flex;
  flex-direction: column;
}

.article-title {
  font-size: 1.25rem;
  color: #2c3e50;
  margin-bottom: 1rem;
  font-weight: 600;
}

.article-preview {
  color: #666;
  line-height: 1.6;
  margin-bottom: 1.5rem;
  flex-grow: 1;
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.card-footer {
  padding-top: 1rem;
  border-top: 1px solid #eee;
}

.read-more {
  color: #2c662f;
  font-weight: 500;
  font-size: 0.9rem;
}

.no-articles {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 300px;
}

.empty-state {
  text-align: center;
}

.empty-icon {
  font-size: 3rem;
  margin-bottom: 1rem;
  display: block;
}

.empty-subtitle {
  color: #666;
  margin-top: 0.5rem;
}

@media (max-width: 768px) {
  .article-container {
    padding: 1rem;
  }

  .article-header h1 {
    font-size: 2rem;
  }

  .article-cards {
    grid-template-columns: 1fr;
  }

  .action-bar {
    padding: 0 1rem;
  }
}
  .card-footer {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-top: 1rem;
    padding-top: 1rem;
    border-top: 1px solid #e9ecef;
  }

  .like-button {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    padding: 0.5rem 1rem;
    border: 1px solid #dee2e6;
    border-radius: 20px;
    background: white;
    cursor: pointer;
    transition: all 0.2s;
  }

  .like-button:hover:not(:disabled) {
    background-color: #fff5f5;
    border-color: #ff8787;
  }

  .like-button:disabled {
    cursor: not-allowed;
    opacity: 0.6;
  }

  .like-button.liked {
    background-color: #fff5f5;
    border-color: #ff8787;
  }

  .heart-icon {
    font-size: 1.2rem;
  }

  .like-count {
    font-size: 0.9rem;
    color: #495057;
  }
</style>