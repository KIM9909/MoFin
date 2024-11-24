```vue
<template>
  <div class="create-article-container">
    <div class="form-card">
      <div class="form-header">
        <h1>새 게시글 작성</h1>
        <p class="subtitle">MoFin 커뮤니티에 새로운 이야기를 공유해보세요</p>
      </div>

      <form @submit.prevent="createArticle" class="article-form">
        <div class="form-group">
          <label for="title">제목</label>
          <input 
            id="title" 
            v-model="title" 
            required
            class="form-input"
            placeholder="제목을 입력해주세요"
            maxlength="100"
          />
        </div>

        <div class="form-group">
          <label for="content">내용</label>
          <textarea 
            id="content" 
            v-model="content" 
            required
            class="form-input content-input"
            placeholder="내용을 입력해주세요"
            rows="10"
          ></textarea>
        </div>

        <div class="form-actions">
          <button 
            type="button" 
            class="cancel-btn"
            @click="router.push({ name: 'articleList' })"
          >
            취소
          </button>
          <button type="submit" class="submit-btn">
            게시글 등록
          </button>
        </div>
      </form>
    </div>
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

  if (!title.value.trim() || !content.value.trim()) {
    window.alert('제목과 내용을 모두 입력해주세요.');
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
        window.alert('게시글 작성 중 오류가 발생했습니다. 다시 시도해주세요.');
      }
    });
};
</script>

<style scoped>
.create-article-container {
  max-width: 800px;
  margin: 2rem auto;
  padding: 0 1rem;
}

.form-card {
  background: white;
  border-radius: 12px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  overflow: hidden;
}

.form-header {
  background-color: #2c3e50;
  padding: 2rem;
  text-align: center;
  color: white;
}

.form-header h1 {
  font-size: 2rem;
  margin: 0;
  font-weight: 600;
}

.subtitle {
  color: #b8c2cc;
  margin-top: 0.5rem;
  font-size: 0.9rem;
}

.article-form {
  padding: 2rem;
}

.form-group {
  margin-bottom: 1.5rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  color: #2c3e50;
  font-weight: 500;
}

.form-input {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  font-size: 1rem;
  transition: all 0.3s ease;
}

.form-input:focus {
  outline: none;
  border-color: #2c3e50;
  box-shadow: 0 0 0 2px rgba(44, 62, 80, 0.1);
}

.content-input {
  min-height: 200px;
  resize: vertical;
  line-height: 1.6;
}

.form-actions {
  display: flex;
  gap: 1rem;
  justify-content: flex-end;
  margin-top: 2rem;
}

.cancel-btn, .submit-btn {
  padding: 0.75rem 1.5rem;
  border-radius: 8px;
  font-size: 1rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
}

.cancel-btn {
  background-color: #e2e8f0;
  color: #2c3e50;
  border: none;
}

.cancel-btn:hover {
  background-color: #cbd5e1;
}

.submit-btn {
  background-color: #5c9c5f;
  color: white;
  border: none;
}

.submit-btn:hover {
  background-color: #518e54;
}

/* 입력 필드 플레이스홀더 스타일 */
.form-input::placeholder {
  color: #a0aec0;
}

/* 유효성 검사 스타일 */
.form-input:invalid {
  border-color: #e53e3e;
}

/* 반응형 디자인 */
@media (max-width: 640px) {
  .create-article-container {
    margin: 1rem auto;
  }

  .form-header {
    padding: 1.5rem;
  }

  .form-header h1 {
    font-size: 1.5rem;
  }

  .article-form {
    padding: 1.5rem;
  }

  .form-actions {
    flex-direction: column;
  }

  .cancel-btn, .submit-btn {
    width: 100%;
  }
}

/* 애니메이션 */
@keyframes slideUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.form-card {
  animation: slideUp 0.5s ease-out;
}
</style>
```