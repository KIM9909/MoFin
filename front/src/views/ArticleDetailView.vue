<template>
  <div>
    <h1>{{ article.title }}</h1>
    <p>{{ article.content }}</p>
    <RouterLink :to="{ name: 'articleList' }">뒤로가기</RouterLink>
    <div v-if="article.user && article.user.id === authStore.userId">
      <RouterLink :to="{ name: 'articleUpdate', params: { id: article.id } }">수정</RouterLink>
      <button @click="deleteArticle">삭제</button>
    </div>

    <h2>댓글</h2>
    <ul>
      <li v-for="comment in comments" :key="comment.id" class="comment-item">
        <!-- 수정 모드가 아닐 때 -->
        <div v-if="editingCommentId !== comment.id">
          <p>{{ comment.content }}</p>
          <div class="comment-meta">
            <span>{{ formatDate(comment.created_at) }}</span>
            <span>작성자: {{ comment.user.nickname }}</span>
            <!-- 자신이 작성한 댓글만 수정/삭제 버튼 표시 -->
            <div v-if="comment.user.id === authStore.userId" class="comment-actions">
              <button @click="startEdit(comment)">수정</button>
              <button @click="deleteComment(comment.id)">삭제</button>
            </div>
            <!-- <span>작성자: {{ comment.user.nickname }} (ID: {{ comment.user.id }})</span>
            <span>로그인 사용자 ID: {{ authStore.userId }}</span> -->
          </div>
        </div>
        <!-- 수정 모드일 때 -->
        <div v-else>
          <textarea 
            v-model="editingContent" 
            class="edit-textarea"
          ></textarea>
          <div class="edit-actions">
            <button @click="updateComment(comment.id)">저장</button>
            <button @click="cancelEdit">취소</button>
          </div>
        </div>
      </li>
    </ul>

    <textarea 
      v-model="newComment" 
      placeholder="댓글을 입력하세요"
      class="new-comment-textarea"
    ></textarea>
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
.comment-item {
  border-bottom: 1px solid #eee;
  padding: 1rem 0;
  list-style: none;
}

.comment-meta {
  display: flex;
  gap: 1rem;
  font-size: 0.9rem;
  color: #666;
  margin-top: 0.5rem;
}

.comment-actions {
  margin-left: auto;
}

.comment-actions button {
  margin-left: 0.5rem;
  padding: 0.25rem 0.5rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  background: #fff;
  cursor: pointer;
}

.edit-textarea, .new-comment-textarea {
  width: 100%;
  min-height: 60px;
  margin: 0.5rem 0;
  padding: 0.5rem;
  border: 1px solid #ddd;
  border-radius: 4px;
}

.edit-actions {
  display: flex;
  gap: 0.5rem;
  justify-content: flex-end;
  margin-top: 0.5rem;
}

button {
  padding: 0.5rem 1rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  background: #fff;
  cursor: pointer;
}

button:hover {
  background: #f5f5f5;
}
</style>