<template>
  <div class="edit-container">
    <div class="edit-card">
      <div class="form-header">
        <h1>게시글 수정</h1>
        <p class="subtitle">작성하신 게시글을 수정합니다</p>
      </div>

      <form @submit.prevent="updateArticle" class="edit-form">
        <div class="form-group">
          <label for="title">제목</label>
          <input 
            id="title" 
            v-model="title"
            class="form-input"
            placeholder="제목을 입력하세요"
            required
          />
        </div>

        <div class="form-group">
          <label for="content">내용</label>
          <textarea 
            id="content" 
            v-model="content"
            class="form-textarea"
            placeholder="내용을 입력하세요"
            rows="10"
            required
          ></textarea>
        </div>

        <div class="button-group">
          <button 
            type="button" 
            class="cancel-btn"
            @click="router.push({ 
              name: 'articleDetail', 
              params: { id: route.params.id } 
            })"
          >
            취소
          </button>
          <button type="submit" class="submit-btn">
            수정 완료
          </button>
        </div>
      </form>
    </div>
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
  axios.get(`http://127.0.0.1:8000/articles/articles/${route.params.id}/`)
    .then(response => {
      title.value = response.data.title;
      content.value = response.data.content;
    })
    .catch(error => {
      console.error('게시글 데이터를 가져오는 중 오류가 발생했습니다:', error);
    });
});

const updateArticle = () => {
  axios.put(`http://127.0.0.1:8000/articles/articles/${route.params.id}/`, {
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


<style scoped>
.edit-container {
  max-width: 800px;
  margin: 2rem auto;
  padding: 0 1rem;
}

.edit-card {
  background: white;
  border-radius: 12px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  overflow: hidden;
}

.form-header {
  background-color: #2c662f;
  color: white;
  padding: 1.5rem;
  text-align: center;
}

.form-header h1 {
  margin: 0;
  font-size: 1.8rem;
  font-weight: 600;
}

.subtitle {
  margin: 0.5rem 0 0 0;
  font-size: 0.9rem;
  opacity: 0.8;
}

.edit-form {
  padding: 2rem;
}

.form-group {
  margin-bottom: 1.5rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  color: #333;
  font-weight: 500;
}

.form-input,
.form-textarea {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #dee2e6;
  border-radius: 6px;
  font-size: 1rem;
  transition: border-color 0.2s;
}

.form-textarea {
  resize: vertical;
  min-height: 200px;
  line-height: 1.6;
}

.form-input:focus,
.form-textarea:focus {
  outline: none;
  border-color: #2c662f;
  box-shadow: 0 0 0 2px rgba(44, 102, 47, 0.1);
}

.button-group {
  display: flex;
  gap: 1rem;
  justify-content: flex-end;
  margin-top: 2rem;
}

.submit-btn,
.cancel-btn {
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 6px;
  font-size: 1rem;
  cursor: pointer;
  transition: all 0.2s;
}

.submit-btn {
  background-color: #2c662f;
  color: white;
}

.submit-btn:hover {
  background-color: #235024;
}

.cancel-btn {
  background-color: #e9ecef;
  color: #495057;
}

.cancel-btn:hover {
  background-color: #dee2e6;
}

@media (max-width: 640px) {
  .edit-container {
    margin: 1rem auto;
  }

  .edit-card {
    border-radius: 8px;
  }

  .form-header {
    padding: 1rem;
  }

  .form-header h1 {
    font-size: 1.5rem;
  }

  .edit-form {
    padding: 1rem;
  }

  .button-group {
    flex-direction: column-reverse;
  }

  .submit-btn,
  .cancel-btn {
    width: 100%;
  }
}
</style>