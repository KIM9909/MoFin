<template>
  <div class="profile-container">
    <!-- 사이드바 -->
    <aside class="sidebar">
      <div class="user-info">
        <div class="user-avatar">{{ auth.nickname?.charAt(0) }}</div>
        <h2 class="user-name">{{ auth.nickname }}</h2>
      </div>

      <nav class="menu-list">
        <button 
          class="menu-item"
          :class="{ 'active': activeMenu === 'info' }"
          @click="activeMenu = 'info'"
        >
          <span class="icon">👤</span>
          회원정보
        </button>
        <button 
          class="menu-item"
          :class="{ 'active': activeMenu === 'security' }"
          @click="activeMenu = 'security'"
        >
          <span class="icon">🔒</span>
          보안설정
        </button>
        <button 
          class="menu-item"
          :class="{ 'active': activeMenu === 'delete' }"
          @click="activeMenu = 'delete'"
        >
          <span class="icon">⚠️</span>
          탈퇴하기
        </button>
      </nav>
    </aside>

    <!-- 메인 컨텐츠 -->
    <main class="main-content">
      <!-- 회원정보 섹션 -->
      <div v-if="activeMenu === 'info'" class="content-section">
        <div class="section-header">
          <h1>회원정보</h1>
        </div>

        <div class="content-card">
          <div v-if="!isEditing">
            <div class="info-row">
              <label>사용자 이름</label>
              <p>{{ auth.nickname }}</p>
            </div>
            <div class="info-row">
              <label>이메일</label>
              <p>{{ auth.email }}</p>
            </div>
            <button @click="startEditing" class="primary-btn">
              정보 수정
            </button>
          </div>

          <form v-else @submit.prevent="updateProfile" class="edit-form">
            <div class="form-group">
              <label>사용자 이름</label>
              <input
                v-model="editForm.username"
                type="text"
                required
              >
            </div>
            <div class="button-group">
              <button type="submit" class="primary-btn">저장</button>
              <button type="button" @click="cancelEditing" class="secondary-btn">
                취소
              </button>
            </div>
          </form>
        </div>
      </div>

      <!-- 보안설정 섹션 -->
      <div v-if="activeMenu === 'security'" class="content-section">
        <div class="section-header">
          <h1>보안설정</h1>
        </div>

        <div class="content-card">
          <form @submit.prevent="updatePassword" class="password-form">
            <div class="form-group">
              <label>현재 비밀번호</label>
              <input
                v-model="passwordForm.old_password"
                type="password"
                required
              >
            </div>
            <div class="form-group">
              <label>새 비밀번호</label>
              <input
                v-model="passwordForm.new_password1"
                type="password"
                required
              >
            </div>
            <div class="form-group">
              <label>새 비밀번호 확인</label>
              <input
                v-model="passwordForm.new_password2"
                type="password"
                required
              >
            </div>
            <button type="submit" class="primary-btn">
              비밀번호 변경
            </button>
          </form>
        </div>
      </div>

      <!-- 탈퇴하기 섹션 -->
      <div v-if="activeMenu === 'delete'" class="content-section">
        <div class="section-header">
          <h1>회원 탈퇴</h1>
        </div>

        <div class="content-card warning">
          <div class="warning-icon">⚠️</div>
          <h2>회원 탈퇴 전 꼭 확인해주세요</h2>
          <p>
            탈퇴 시 모든 데이터가 삭제되며 복구할 수 없습니다.
            신중하게 결정해 주세요.
          </p>
          <button @click="confirmDelete" class="danger-btn">
            회원 탈퇴
          </button>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useAuthStore } from '@/stores/auth';
import { useRouter } from 'vue-router';
import axios from 'axios';

const router = useRouter();
const auth = useAuthStore();
const isEditing = ref(false);
const activeMenu = ref('info');

const editForm = ref({
  username: '',
});

const passwordForm = ref({
  old_password: '',
  new_password1: '',
  new_password2: ''
});

// 컴포넌트 마운트 시 사용자 정보 불러오기
onMounted(async () => {
  try {
    await auth.fetchUserInfo();
  } catch (error) {
    console.error('사용자 정보 로딩 실패:', error);
    alert('사용자 정보를 불러오는데 실패했습니다.');
  }
});

// 수정 모드 시작
const startEditing = () => {
  isEditing.value = true;
  editForm.value.username = auth.nickname;
};

// 수정 취소
const cancelEditing = () => {
  isEditing.value = false;
};

// 프로필 업데이트
const updateProfile = async () => {
  try {
    await axios.put('http://127.0.0.1:8000/accounts/user/', {
      username: editForm.value.username
    }, {
      headers: {
        Authorization: `Token ${auth.token}`
      }
    });
    
    await auth.fetchUserInfo();
    isEditing.value = false;
    alert('프로필이 성공적으로 업데이트되었습니다.');
  } catch (error) {
    console.error('프로필 업데이트 실패:', error);
    alert('프로필 업데이트에 실패했습니다.');
  }
};

// 비밀번호 변경
const updatePassword = async () => {
  if (passwordForm.value.new_password1 !== passwordForm.value.new_password2) {
    alert('새 비밀번호가 일치하지 않습니다.');
    return;
  }

  try {
    await axios.post('http://127.0.0.1:8000/accounts/password/change/', {
      old_password: passwordForm.value.old_password,
      new_password1: passwordForm.value.new_password1,
      new_password2: passwordForm.value.new_password2
    }, {
      headers: {
        Authorization: `Token ${auth.token}`
      }
    });
    
    passwordForm.value = {
      old_password: '',
      new_password1: '',
      new_password2: ''
    };
    
    alert('비밀번호가 성공적으로 변경되었습니다.');
    activeMenu.value = 'info';
  } catch (error) {
    console.error('비밀번호 변경 실패:', error);
    alert('비밀번호 변경에 실패했습니다.');
  }
};

// 계정 삭제
const confirmDelete = async () => {
  if (confirm('정말로 계정을 삭제하시겠습니까? 이 작업은 되돌릴 수 없습니다.')) {
    try {
      await axios.delete('http://127.0.0.1:8000/accounts/delete/', {
        headers: {
          Authorization: `Token ${auth.token}`
        }
      });
      
      auth.logout();
      router.push({ name: 'home' });
      alert('계정이 성공적으로 삭제되었습니다.');
    } catch (error) {
      console.error('계정 삭제 실패:', error.response?.data);
      if (error.response?.data) {
        alert(`계정 삭제 실패: ${JSON.stringify(error.response.data)}`);
      } else {
        alert('계정 삭제에 실패했습니다.');
      }
    }
  }
};
</script>


<style scoped>
.profile-container {
  display: flex;
  min-height: 100vh;
  background-color: #f8f9fa;
}

.sidebar {
  width: 280px;
  background-color: white;
  padding: 2rem;
  border-right: 1px solid #e9ecef;
  display: flex;
  flex-direction: column;
}

.user-info {
  text-align: center;
  margin-bottom: 2rem;
}

.user-avatar {
  width: 80px;
  height: 80px;
  background-color: #2c662f;
  color: white;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 2rem;
  margin: 0 auto 1rem;
}

.user-name {
  font-size: 1.2rem;
  color: #2c3e50;
  margin: 0;
}

.menu-list {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.menu-item {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.75rem 1rem;
  border: none;
  background: none;
  border-radius: 8px;
  color: #495057;
  font-size: 1rem;
  cursor: pointer;
  transition: all 0.2s;
}

.menu-item:hover {
  background-color: #f8f9fa;
}

.menu-item.active {
  background-color: #e8f5e9;
  color: #2c662f;
  font-weight: 500;
}

.main-content {
  flex: 1;
  padding: 2rem;
  max-width: 800px;
  margin: 0 auto;
}

.section-header {
  margin-bottom: 2rem;
}

.section-header h1 {
  font-size: 1.8rem;
  color: #2c3e50;
  margin: 0;
}

.content-card {
  background: white;
  border-radius: 12px;
  padding: 2rem;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}

.info-row {
  margin-bottom: 1.5rem;
}

.info-row label {
  display: block;
  font-weight: 500;
  color: #6c757d;
  margin-bottom: 0.5rem;
}

.info-row p {
  margin: 0;
  font-size: 1rem;
  color: #2c3e50;
}

.form-group {
  margin-bottom: 1.5rem;
}

.form-group label {
  display: block;
  font-weight: 500;
  color: #6c757d;
  margin-bottom: 0.5rem;
}

.form-group input {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #dee2e6;
  border-radius: 6px;
  font-size: 1rem;
}

.form-group input:focus {
  outline: none;
  border-color: #2c662f;
}

.button-group {
  display: flex;
  gap: 1rem;
}

.primary-btn {
  padding: 0.75rem 1.5rem;
  background-color: #2c662f;
  color: white;
  border: none;
  border-radius: 6px;
  font-size: 1rem;
  cursor: pointer;
  transition: background-color 0.2s;
}

.primary-btn:hover {
  background-color: #235024;
}

.secondary-btn {
  padding: 0.75rem 1.5rem;
  background-color: #e9ecef;
  color: #495057;
  border: none;
  border-radius: 6px;
  font-size: 1rem;
  cursor: pointer;
}

.secondary-btn:hover {
  background-color: #dee2e6;
}

.danger-btn {
  padding: 0.75rem 1.5rem;
  background-color: #dc3545;
  color: white;
  border: none;
  border-radius: 6px;
  font-size: 1rem;
  cursor: pointer;
}

.danger-btn:hover {
  background-color: #c82333;
}

.warning {
  text-align: center;
}

.warning-icon {
  font-size: 3rem;
  margin-bottom: 1rem;
}

.warning h2 {
  color: #dc3545;
  font-size: 1.4rem;
  margin-bottom: 1rem;
}

.warning p {
  color: #6c757d;
  margin-bottom: 2rem;
}

@media (max-width: 768px) {
  .profile-container {
    flex-direction: column;
  }

  .sidebar {
    width: 100%;
    border-right: none;
    border-bottom: 1px solid #e9ecef;
    padding: 1rem;
  }

  .main-content {
    padding: 1rem;
  }

  .content-card {
    padding: 1rem;
  }

  .button-group {
    flex-direction: column;
  }
}
</style>