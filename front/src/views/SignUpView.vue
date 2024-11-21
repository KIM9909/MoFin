<!-- SignUpView.vue -->
<template>
  <div class="container mt-5">
    <div class="row justify-content-center">
      <div class="col-md-8">
        <div class="card">
          <div class="card-header bg-primary text-white">
            <h3 class="mb-0">회원가입</h3>
          </div>
          <div class="card-body">
            <form @submit.prevent="signUp" class="needs-validation" novalidate>
              <!-- 사용자 이름 -->
              <div class="mb-3">
                <label for="username" class="form-label">사용자 이름 *</label>
                <input
                  v-model="credentials.username"
                  type="text"
                  class="form-control"
                  id="username"
                  required
                  placeholder="로그인에 사용할 아이디를 입력하세요"
                >
                <div class="invalid-feedback">
                  사용자 이름을 입력해주세요.
                </div>
              </div>

              <!-- 닉네임 -->
              <div class="mb-3">
                <label for="nickname" class="form-label">닉네임 *</label>
                <input
                  v-model="credentials.nickname"
                  type="text"
                  class="form-control"
                  id="nickname"
                  required
                  placeholder="사이트에서 사용할 닉네임을 입력하세요"
                >
                <div class="invalid-feedback">
                  닉네임을 입력해주세요.
                </div>
              </div>

              <!-- 이메일 -->
              <div class="mb-3">
                <label for="email" class="form-label">이메일 *</label>
                <input
                  v-model="credentials.email"
                  type="email"
                  class="form-control"
                  id="email"
                  required
                  placeholder="example@email.com"
                >
                <div class="invalid-feedback">
                  올바른 이메일 주소를 입력해주세요.
                </div>
              </div>

              <!-- 생년월일 -->
              <div class="mb-3">
                <label for="birth" class="form-label">생년월일</label>
                <input
                  v-model="credentials.birth"
                  type="date"
                  class="form-control"
                  id="birth"
                >
              </div>

              <!-- 선호도 -->
              <div class="mb-3">
                <label for="preference" class="form-label">선호도</label>
                <select 
                  v-model="credentials.preference"
                  class="form-select"
                  id="preference"
                >
                  <option value="">선택하세요</option>
                  <option value="안정형">안정형</option>
                  <option value="중립형">중립형</option>
                  <option value="수익형">수익형</option>
                </select>
              </div>

              <!-- 비밀번호 -->
              <div class="mb-3">
                <label for="password1" class="form-label">비밀번호 *</label>
                <input
                  v-model="credentials.password1"
                  type="password"
                  class="form-control"
                  id="password1"
                  required
                  placeholder="비밀번호를 입력하세요"
                >
                <div class="form-text">
                  최소 8자 이상, 영문/숫자/특수문자를 포함해야 합니다.
                </div>
                <div class="invalid-feedback">
                  비밀번호를 입력해주세요.
                </div>
              </div>

              <!-- 비밀번호 확인 -->
              <div class="mb-3">
                <label for="password2" class="form-label">비밀번호 확인 *</label>
                <input
                  v-model="credentials.password2"
                  type="password"
                  class="form-control"
                  id="password2"
                  required
                  placeholder="비밀번호를 다시 입력하세요"
                >
                <div class="invalid-feedback">
                  비밀번호가 일치하지 않습니다.
                </div>
              </div>

              <!-- 약관 동의 -->
              <div class="mb-3 form-check">
                <input
                  v-model="agreeToTerms"
                  type="checkbox"
                  class="form-check-input"
                  id="agreeToTerms"
                  required
                >
                <label class="form-check-label" for="agreeToTerms">
                  이용약관과 개인정보 처리방침에 동의합니다. *
                </label>
                <div class="invalid-feedback">
                  약관에 동의해주세요.
                </div>
              </div>

              <!-- 제출 버튼 -->
              <div class="d-grid gap-2">
                <button 
                  type="submit" 
                  class="btn btn-primary btn-lg"
                  :disabled="!isFormValid"
                >
                  가입하기
                </button>
                <button 
                  type="button" 
                  class="btn btn-secondary"
                  @click="$router.push({ name: 'signIn' })"
                >
                  이미 계정이 있으신가요? 로그인하기
                </button>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useRouter } from 'vue-router'

const router = useRouter()
const auth = useAuthStore()
const agreeToTerms = ref(false)

const credentials = ref({
  username: '',
  email: '',
  password1: '',
  password2: '',
  nickname: '',
  birth: '',
  preference: ''
})

// 폼 유효성 검사
const isFormValid = computed(() => {
  return (
    credentials.value.username &&
    credentials.value.email &&
    credentials.value.password1 &&
    credentials.value.password2 &&
    credentials.value.nickname &&
    credentials.value.password1 === credentials.value.password2 &&
    agreeToTerms.value
  )
})

// 비밀번호 유효성 검사
const isPasswordValid = (password) => {
  const regex = /^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$/
  return regex.test(password)
}

const signUp = async () => {
  // 기본 유효성 검사
  if (!isFormValid.value) {
    alert('모든 필수 항목을 입력해주세요.')
    return
  }

  // 비밀번호 일치 확인
  if (credentials.value.password1 !== credentials.value.password2) {
    alert('비밀번호가 일치하지 않습니다.')
    return
  }

  // 비밀번호 규칙 검사
  if (!isPasswordValid(credentials.value.password1)) {
    alert('비밀번호는 최소 8자 이상이며, 영문/숫자/특수문자를 포함해야 합니다.')
    return
  }

  try {
    await auth.signUp(credentials.value)
    // 성공 시 자동으로 로그인 페이지로 이동 (auth.js에서 처리)
  } catch (error) {
    console.error('회원가입 처리 중 오류 발생:', error)
  }
}
</script>

<style scoped>
.card {
  box-shadow: 0 0.5rem 1rem rgba(0, 0, 0, 0.15);
}

.form-label {
  font-weight: 500;
}

.invalid-feedback {
  display: block;
}
</style>