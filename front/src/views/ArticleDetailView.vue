<template>
  <div class="article-detail-container">
    <div class="article-card">
      <!-- 게시글 헤더 -->
      <div class="article-header">
        <h1>{{ article.title }}</h1>
        <div class="article-meta">
          <span class="author">작성자: {{ article.user?.nickname }}</span>
          <span class="separator">•</span>
          <span class="date">{{ formatDate(article.created_at) }}</span>
          <!-- <span class="separator">•</span> -->
          <button 
            @click="toggleLike"
            :class="['like-button', { 'liked': article.is_liked }]"
            :disabled="!authStore.isLogin"
          >
            <span class="heart-icon">{{ article.is_liked ? '❤️' : '🤍' }}</span>
            <span class="like-count">{{ article.like_count }}</span>
          </button>
        </div>
      </div>

      <!-- 게시글 내용 -->
      <div class="article-content">
        <p>{{ article.content }}</p>
      </div>

      <!-- 게시글 작성자 액션 버튼 -->
      <div class="article-actions">
        <RouterLink :to="{ name: 'articleList' }" class="back-btn">
          <span class="icon">←</span> 목록으로
        </RouterLink>
        
        <div v-if="article.user && article.user.id === authStore.userId" class="author-actions">
          <RouterLink :to="{ name: 'articleUpdate', params: { id: article.id } }" class="edit-btn">
            수정
          </RouterLink>
          <button @click="deleteArticle" class="delete-btn">삭제</button>
        </div>
      </div>

      <!-- 댓글 섹션 -->
      <div class="comments-section">
        <h4>댓글</h4>
        
        <!-- 새 댓글 작성 -->
        <div class="new-comment">
          <textarea 
            v-model="newComment" 
            placeholder="댓글을 입력하세요"
            class="comment-textarea"
          ></textarea>
          <button @click="addComment" class="submit-btn">댓글 작성</button>
        </div>

        <!-- 댓글 목록 -->
        <ul class="comment-list">
          <li v-for="comment in comments" :key="comment.id" class="comment-item">
            <!-- 일반 모드 -->
            <div v-if="editingCommentId !== comment.id" class="comment-content">
              <div class="comment-header">
                <span class="comment-author">{{ comment.user.nickname }}</span>
                <span class="comment-date">{{ formatDate(comment.created_at) }}</span>
              </div>
              <p class="comment-text">{{ comment.content }}</p>
              <div v-if="comment.user.id === authStore.userId" class="comment-actions">
                <button @click="startEdit(comment)" class="action-btn edit">수정</button>
                <button @click="deleteComment(comment.id)" class="action-btn delete">삭제</button>
              </div>
            </div>
            
            <!-- 수정 모드 -->
            <div v-else class="comment-edit">
              <textarea 
                v-model="editingContent" 
                class="edit-textarea"
              ></textarea>
              <div class="edit-actions">
                <button @click="updateComment(comment.id)" class="save-btn">저장</button>
                <button @click="cancelEdit" class="cancel-btn">취소</button>
              </div>
            </div>
          </li>
        </ul>
      </div>
    </div>
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
const authStore = useAuthStore();

// 댓글 수정 관련 상태
const editingCommentId = ref(null);
const editingContent = ref("");

onMounted(() => {
  fetchArticle();
  fetchComments();
});

const fetchArticle = () => {
  axios
    .get(`http://127.0.0.1:8000/articles/articles/${route.params.id}/`)
    .then((response) => {
      console.log(authStore.userId)
      article.value = response.data;
    })
    .catch((error) => {
      console.error('게시글 데이터를 가져오는 중 오류가 발생했습니다:', error);
    });
};

// 좋아요 토글 함수
const toggleLike = async () => {
  if (!authStore.isLogin) {
    alert('좋아요를 누르려면 로그인이 필요합니다.');
    return;
  }

  try {
    const response = await axios({
      method: 'post',
      url: `http://127.0.0.1:8000/articles/articles/${article.value.id}/like/`,
      headers: { Authorization: `Token ${authStore.token}` }
    });
    
    article.value.is_liked = response.data.is_liked;
    article.value.like_count = response.data.like_count;
  } catch (error) {
    console.error('좋아요 처리 중 오류가 발생했습니다:', error);
    alert('좋아요 처리 중 오류가 발생했습니다.');
  }
};

const fetchComments = () => {
  const url = `http://127.0.0.1:8000/articles/comments/article/${route.params.id}/`;
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
          router.push({ name: 'login' });
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

// 댓글 수정 시작
const startEdit = (comment) => {
  editingCommentId.value = comment.id;
  editingContent.value = comment.content;
};

// 댓글 수정 취소
const cancelEdit = () => {
  editingCommentId.value = null;
  editingContent.value = "";
};

// 댓글 수정 저장
const updateComment = (commentId) => {
  if (!editingContent.value.trim()) {
    alert("댓글 내용을 입력하세요.");
    return;
  }

  axios
    .put(
      `http://127.0.0.1:8000/articles/comments/${commentId}/`,
      { 
        content: editingContent.value,
        article: article.value.id
      },
      { 
        headers: { Authorization: `Token ${authStore.token}` } 
      }
    )
    .then(() => {
      fetchComments();
      cancelEdit();
    })
    .catch((error) => {
      console.error("댓글 수정 중 오류가 발생했습니다:", error);
      if (error.response && error.response.status === 401) {
        alert("로그인이 필요합니다.");
        router.push({ name: "login" });
      }
    });
};

// 댓글 삭제
const deleteComment = (commentId) => {
  if (!confirm("정말 이 댓글을 삭제하시겠습니까?")) {
    return;
  }

  axios
    .delete(
      `http://127.0.0.1:8000/articles/comments/${commentId}/`,
      { 
        headers: { Authorization: `Token ${authStore.token}` } 
      }
    )
    .then(() => {
      fetchComments();
    })
    .catch((error) => {
      console.error("댓글 삭제 중 오류가 발생했습니다:", error);
      if (error.response && error.response.status === 401) {
        alert("로그인이 필요합니다.");
        router.push({ name: "login" });
      }
    });
};

// 날짜 포맷팅 함수
const formatDate = (dateString) => {
  const date = new Date(dateString);
  return date.toLocaleDateString();
};
</script>

<style scoped>
.article-detail-container {
  max-width: 800px;
  margin: 2rem auto;
  padding: 0 1rem;
}

.article-card {
  background: white;
  border-radius: 12px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  overflow: hidden;
}

.article-header {
  padding: 2rem;
  background-color: #2c3e50;
  color: white;
}

.article-header h1 {
  margin: 0;
  font-size: 2rem;
  font-weight: 600;
}

.article-meta {
  margin-top: 1rem;
  font-size: 0.9rem;
  color: #b8c2cc;
}

.separator {
  margin: 0 0.5rem;
}

.article-content {
  padding: 2rem;
  line-height: 1.6;
  color: #2c3e50;
}

.article-actions {
  padding: 1rem 2rem;
  border-top: 1px solid #edf2f7;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.back-btn, .edit-btn, .delete-btn {
  padding: 0.5rem 1rem;
  border-radius: 6px;
  text-decoration: none;
  font-weight: 500;
  transition: all 0.3s ease;
}

.back-btn {
  color: #2c3e50;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.back-btn:hover {
  background-color: #edf2f7;
}

.edit-btn {
  background-color: #4a5568;
  color: white;
  margin-right: 0.5rem;
}

.delete-btn {
  background-color: #e53e3e;
  color: white;
  border: none;
  cursor: pointer;
}

.comments-section {
  padding: 2rem;
  background-color: #f8fafc;
}

.comments-section h2 {
  margin: 0 0 1.5rem 0;
  color: #2c3e50;
}

.new-comment {
  margin-bottom: 2rem;
}

.comment-textarea, .edit-textarea {
  width: 100%;
  min-height: 100px;
  padding: 1rem;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  margin-bottom: 1rem;
  font-size: 1rem;
  resize: vertical;
}

.submit-btn {
  background-color: #5c9c5f;
  color: white;
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-weight: 500;
}

.comment-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.comment-item {
  padding: 1.5rem;
  border-bottom: 1px solid #e2e8f0;
}

.comment-item:last-child {
  border-bottom: none;
}

.comment-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 0.5rem;
}

.comment-author {
  font-weight: 600;
  color: #2c3e50;
}

.comment-date {
  color: #718096;
  font-size: 0.9rem;
}

.comment-text {
  margin: 0.5rem 0;
  line-height: 1.6;
}

.comment-actions {
  display: flex;
  gap: 0.5rem;
  margin-top: 1rem;
}

.action-btn {
  padding: 0.4rem 0.8rem;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.9rem;
}

.action-btn.edit {
  background-color: #edf2f7;
  color: #2c3e50;
}

.action-btn.delete {
  background-color: #fed7d7;
  color: #c53030;
}

.edit-actions {
  display: flex;
  gap: 0.5rem;
  justify-content: flex-end;
  margin-top: 1rem;
}

.save-btn, .cancel-btn {
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.save-btn {
  background-color: #5c9c5f;
  color: white;
}

.cancel-btn {
  background-color: #e2e8f0;
  color: #2c3e50;
}

@media (max-width: 640px) {
  .article-detail-container {
    margin: 1rem auto;
  }

  .article-header {
    padding: 1.5rem;
  }

  .article-header h1 {
    font-size: 1.5rem;
  }

  .article-content, .comments-section {
    padding: 1.5rem;
  }

  .article-actions {
    flex-direction: column;
    gap: 1rem;
    align-items: stretch;
  }

  .author-actions {
    display: flex;
    gap: 0.5rem;
  }

  .edit-btn, .delete-btn {
    flex: 1;
    text-align: center;
  }
}

  .like-button {
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    padding: 0.5rem 1rem;
    border: 1px solid #dee2e6;
    border-radius: 20px;
    background: white;
    cursor: pointer;
    transition: all 0.2s;
    margin-left: 350px;
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