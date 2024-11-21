<!-- ProfilePageView.vue -->
<template>
  <div class="container-fluid">
    <div class="row">
      <!-- 왼쪽 사이드바 -->
      <div class="col-md-3 bg-light min-vh-100 p-4 border-end">
        <h3 class="text-primary mb-4">프로필 메뉴</h3>
        <div class="list-group">
          <button 
            class="list-group-item list-group-item-action"
            :class="{ 'active': activeMenu === 'info' }"
            @click="activeMenu = 'info'"
          >
            <i class="bi bi-person-fill me-2"></i>회원정보
          </button>
          <button 
            class="list-group-item list-group-item-action"
            :class="{ 'active': activeMenu === 'security' }"
            @click="activeMenu = 'security'"
          >
            <i class="bi bi-shield-lock-fill me-2"></i>보안설정
          </button>
          <button 
            class="list-group-item list-group-item-action"
            :class="{ 'active': activeMenu === 'delete' }"
            @click="activeMenu = 'delete'"
          >
            <i class="bi bi-person-x-fill me-2"></i>탈퇴하기
          </button>
        </div>
      </div>

      <!-- 오른쪽 컨텐츠 영역 -->
      <div class="col-md-9 p-4">
        <!-- 회원정보 섹션 -->
        <div v-if="activeMenu === 'info'">
          <h2 class="mb-4">회원정보</h2>
          <div class="card">
            <div class="card-body">
              <div v-if="!isEditing">
                <div class="mb-3">
                  <label class="form-label fw-bold">사용자 이름</label>
                  <p class="form-control-plaintext">{{ auth.nickname }}</p>
                </div>
                <div class="mb-3">
                  <label class="form-label fw-bold">이메일</label>
                  <p class="form-control-plaintext">{{ auth.email }}</p>
                </div>
                <button 
                  @click="startEditing" 
                  class="btn btn-primary"
                >
                  정보 수정
                </button>
              </div>

              <form v-else @submit.prevent="updateProfile">
                <div class="mb-3">
                  <label class="form-label">사용자 이름</label>
                  <input
                    v-model="editForm.username"
                    type="text"
                    class="form-control"
                    required
                  >
                </div>
                <div class="d-flex gap-2">
                  <button type="submit" class="btn btn-success">저장</button>
                  <button 
                    type="button" 
                    @click="cancelEditing" 
                    class="btn btn-secondary"
                  >
                    취소
                  </button>
                </div>
              </form>
            </div>
          </div>
        </div>

        <!-- 보안설정 섹션 -->
        <div v-if="activeMenu === 'security'">
          <h2 class="mb-4">보안설정</h2>
          <div class="card">
            <div class="card-body">
              <form @submit.prevent="updatePassword">
                <div class="mb-3">
                  <label class="form-label">현재 비밀번호</label>
                  <input
                    v-model="passwordForm.old_password"
                    type="password"
                    class="form-control"
                    required
                  >
                </div>
                <div class="mb-3">
                  <label class="form-label">새 비밀번호</label>
                  <input
                    v-model="passwordForm.new_password1"
                    type="password"
                    class="form-control"
                    required
                  >
                </div>
                <div class="mb-3">
                  <label class="form-label">새 비밀번호 확인</label>
                  <input
                    v-model="passwordForm.new_password2"
                    type="password"
                    class="form-control"
                    required
                  >
                </div>
                <button type="submit" class="btn btn-primary">
                  비밀번호 변경
                </button>
              </form>
            </div>
          </div>
        </div>

        <!-- 탈퇴하기 섹션 -->
        <div v-if="activeMenu === 'delete'">
          <h2 class="mb-4">회원 탈퇴</h2>
          <div class="card border-danger">
            <div class="card-body">
              <h5 class="card-title text-danger">주의사항</h5>
              <p class="card-text">
                탈퇴 시 모든 데이터가 삭제되며 복구할 수 없습니다.
                신중하게 결정해 주세요.
              </p>
              <button 
                @click="confirmDelete" 
                class="btn btn-danger"
              >
                회원 탈퇴
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
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
.min-vh-100 {
  min-height: 100vh;
}

.form-control-plaintext {
  margin-bottom: 0;
  font-size: 1rem;
  color: #212529;
}
</style>