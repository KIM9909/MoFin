<template>
  <div class="signup-container">
    <div class="signup-card">
      <div class="form-header">
        <h1>회원가입</h1>
        <p class="subtitle">MoFin과 함께 스마트한 금융생활을 시작하세요</p>
      </div>

      <form @submit.prevent="signUp" class="signup-form" novalidate>
        <!-- 기본 정보 섹션 -->
        <div class="form-section">
          <h2 class="section-title">기본 정보</h2>
          <div class="form-group">
            <label>프로필 이미지</label>
            <div class="profile-upload">
              <div class="profile-preview">
                <img
                  v-if="previewImage"
                  :src="previewImage"
                  alt="Preview"
                  class="preview-img"
                >
                <div v-else class="preview-placeholder">
                  <span class="upload-icon">📷</span>
                </div>
              </div>
              <div class="upload-controls">
                <input
                  type="file"
                  ref="fileInput"
                  @change="handleImageChange"
                  accept="image/*"
                  class="file-input"
                  hidden
                >
                <button
                  type="button"
                  @click="$refs.fileInput.click()"
                  class="upload-btn"
                >
                  이미지 선택
                </button>
                <button
                  v-if="previewImage"
                  type="button"
                  @click="removeImage"
                  class="remove-btn"
                >
                  제거
                </button>
              </div>
            </div>
          </div>

          <div class="form-group">
            <label for="username">아이디 <span class="required">*</span></label>
            <div class="input-wrapper">
              <span class="input-icon">👤</span>
              <input
                v-model="credentials.username"
                type="text"
                id="username"
                required
                placeholder="로그인에 사용할 아이디"
                class="form-input"
              >
            </div>
          </div>

          <div class="form-group">
            <label for="nickname">닉네임 <span class="required">*</span></label>
            <div class="input-wrapper">
              <span class="input-icon">📝</span>
              <input
                v-model="credentials.nickname"
                type="text"
                id="nickname"
                required
                placeholder="커뮤니티에서 사용할 닉네임"
                class="form-input"
              >
            </div>
          </div>

          <div class="form-group">
            <label for="email">이메일 <span class="required">*</span></label>
            <div class="input-wrapper">
              <span class="input-icon">📧</span>
              <input
                v-model="credentials.email"
                type="email"
                id="email"
                required
                placeholder="example@email.com"
                class="form-input"
              >
            </div>
          </div>
        </div>

        <!-- 추가 정보 섹션 -->
        <div class="form-section">
          <h2 class="section-title">추가 정보</h2>

          <div class="form-group">
            <label for="birth">생년월일</label>
            <div class="input-wrapper">
              <span class="input-icon">🎂</span>
              <input
                v-model="credentials.birth"
                type="date"
                id="birth"
                class="form-input"
              >
            </div>
          </div>

          <div class="form-group">
            <label for="preference">선호도</label>
            <div class="input-wrapper">
              <span class="input-icon">👛</span>
              <select
                v-model="credentials.preference"
                id="preference"
                class="form-input"
              >
                <option value="">선택하세요</option>
                <option value="안정형">안정형</option>
                <option value="위험회피형">위험회피형</option>
                <option value="수익추구형">수익추구형</option>
              </select>
            </div>
          </div>

          <!-- 연 소득 필드 추가 -->
          <div class="form-group">
            <label for="annual_income">연 소득 (만원)</label>
            <div class="input-wrapper">
              <span class="input-icon">💰</span>
              <input
                v-model.number="credentials.annual_income"
                type="number"
                id="annual_income"
                placeholder="0"
                min="0"
                class="form-input"
              >
            </div>
          </div>

          <!-- 총 자산 필드 추가 -->
          <div class="form-group">
            <label for="total_assets">총 자산 (만원)</label>
            <div class="input-wrapper">
              <span class="input-icon">💎</span>
              <input
                v-model.number="credentials.total_assets"
                type="number"
                id="total_assets"
                placeholder="0"
                min="0"
                class="form-input"
              >
            </div>
          </div>
        </div>

        <!-- 보안 정보 섹션 -->
        <div class="form-section">
          <h2 class="section-title">보안 정보</h2>

          <div class="form-group">
            <label for="password1">비밀번호 <span class="required">*</span></label>
            <div class="input-wrapper">
              <span class="input-icon">🔒</span>
              <input
                v-model="credentials.password1"
                type="password"
                id="password1"
                required
                placeholder="비밀번호 입력"
                class="form-input"
              >
            </div>
            <p class="input-hint">최소 8자 이상, 영문/숫자/특수문자 포함</p>
          </div>

          <div class="form-group">
            <label for="password2">비밀번호 확인 <span class="required">*</span></label>
            <div class="input-wrapper">
              <span class="input-icon">🔒</span>
              <input
                v-model="credentials.password2"
                type="password"
                id="password2"
                required
                placeholder="비밀번호 재입력"
                class="form-input"
              >
            </div>
          </div>
        </div>

        <!-- 약관 동의 -->
        <div class="terms-section">
          <label class="terms-label">
            <input
              v-model="agreeToTerms"
              type="checkbox"
              required
              class="terms-checkbox"
            >
            <span>이용약관과 개인정보 처리방침에 동의합니다. <span class="required">*</span></span>
          </label>
        </div>

        <!-- 버튼 영역 -->
        <div class="button-group">
          <button 
            type="submit" 
            class="submit-btn"
            :disabled="!isFormValid"
          >
            가입하기
          </button>
        </div>
      </form>

      <div class="button-group">
        <button 
          type="button" 
          class="login-link"
          @click="$router.push({ name: 'signIn' })"
        >
          이미 계정이 있으신가요? 로그인하기
        </button>
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
const previewImage = ref(null)
const selectedFile = ref(null)
const credentials = ref({
  username: '',
  email: '',
  password1: '',
  password2: '',
  nickname: '',
  birth: '',
  preference: '',
  annual_income: null,
  total_assets: null,
  profile_img: null
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
const handleImageChange = (event) => {
  const file = event.target.files[0]
  if (!file) return
  
  // 파일 크기 체크 (5MB)
  if (file.size > 5 * 1024 * 1024) {
    alert('파일 크기는 5MB를 초과할 수 없습니다.')
    return
  }
  
  // 이미지 미리보기
  const reader = new FileReader()
  reader.onload = e => {
    previewImage.value = e.target.result
  }
  reader.readAsDataURL(file)
  
  selectedFile.value = file
  credentials.value.profile_img = file
}

const removeImage = () => {
  previewImage.value = null
  selectedFile.value = null
  credentials.value.profile_img = null
  if (fileInput.value) {
    fileInput.value.value = ''
  }
}

const signUp = async () => {
  if (!isFormValid.value) {
    alert('모든 필수 항목을 입력해주세요.')
    return
  }

  if (credentials.value.password1 !== credentials.value.password2) {
    alert('비밀번호가 일치하지 않습니다.')
    return
  }

  if (!isPasswordValid(credentials.value.password1)) {
    alert('비밀번호는 최소 8자 이상이며, 영문/숫자/특수문자를 포함해야 합니다.')
    return
  }

  try {
    const formData = new FormData()
    
    // 일반 필드들 추가
    Object.keys(credentials.value).forEach(key => {
      if (credentials.value[key] !== null && credentials.value[key] !== '') {
        formData.append(key, credentials.value[key])
      }
    })
    
    // 이미지 파일 추가
    if (selectedFile.value) {
      formData.append('profile_img', selectedFile.value)
    }
    
    await auth.signUp(formData)
  } catch (error) {
    console.error('회원가입 처리 중 오류 발생:', error)
  }
}
</script>

<style scoped>
.signup-container {
  min-height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  background-color: #f8f9fa;
  padding: 2rem;
}

.signup-card {
  background: white;
  border-radius: 16px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  width: 100%;
  max-width: 600px;
  overflow: hidden;
  animation: slideUp 0.5s ease-out;
}

.form-header {
  background-color: #2c3e50;
  color: white;
  padding: 2rem;
  text-align: center;
}

.form-header h1 {
  margin: 0;
  font-size: 2rem;
  font-weight: 600;
}

.subtitle {
  margin-top: 0.5rem;
  color: rgba(255, 255, 255, 0.8);
  font-size: 0.9rem;
}

.signup-form {
  padding: 2rem;
}

.form-section {
  margin-bottom: 2rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid #e2e8f0;
}

.section-title {
  font-size: 1.2rem;
  color: #2c3e50;
  margin-bottom: 1.5rem;
  font-weight: 600;
}

.form-group {
  margin-bottom: 1.5rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  color: #2c3e50;
  font-weight: 500;
  font-size: 0.9rem;
}

.required {
  color: #e53e3e;
  margin-left: 0.25rem;
}

.input-wrapper {
  position: relative;
}

.input-icon {
  position: absolute;
  left: 1rem;
  top: 50%;
  transform: translateY(-50%);
  font-size: 1.2rem;
}

.form-input {
  width: 100%;
  padding: 0.75rem 1rem 0.75rem 3rem;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  font-size: 1rem;
  transition: all 0.3s ease;
}

.form-input:focus {
  outline: none;
  border-color: #2c3e50;
  box-shadow: 0 0 0 3px rgba(44, 62, 80, 0.1);
}

.input-hint {
  margin-top: 0.5rem;
  font-size: 0.8rem;
  color: #718096;
}

.terms-section {
  margin: 2rem 0;
}

.terms-label {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  cursor: pointer;
}

.terms-checkbox {
  width: 1.2rem;
  height: 1.2rem;
}

.button-group {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.submit-btn {
  padding: 1rem;
  background-color: #2c662f;
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 1rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
}

.submit-btn:hover:not(:disabled) {
  background-color: #235024;
}

.submit-btn:disabled {
  background-color: #a0aec0;
  cursor: not-allowed;
}

.login-link {
  padding: 0.75rem;
  background: none;
  border: none;
  color: #2c662f;
  font-size: 0.9rem;
  cursor: pointer;
  transition: color 0.3s ease;
}

.login-link:hover {
  color: #235024;
  text-decoration: underline;
}

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

@media (max-width: 640px) {
  .signup-container {
    padding: 1rem;
  }

  .signup-card {
    border-radius: 12px;
  }

  .form-header {
    padding: 1.5rem;
  }

  .signup-form {
    padding: 1.5rem;
  }

  .form-input {
    font-size: 0.9rem;
  }
}
.profile-upload {
  display: flex;
  gap: 1.5rem;
  align-items: center;
  margin-top: 0.5rem;
}

.profile-preview {
  width: 100px;
  height: 100px;
  border-radius: 50%;
  overflow: hidden;
  background-color: #f8f9fa;
  display: flex;
  align-items: center;
  justify-content: center;
  border: 2px dashed #e2e8f0;
}

.preview-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.preview-placeholder {
  color: #a0aec0;
  font-size: 2rem;
}

.upload-controls {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.upload-btn, .remove-btn {
  padding: 0.5rem 1rem;
  border-radius: 6px;
  font-size: 0.9rem;
  cursor: pointer;
  border: none;
  transition: all 0.3s ease;
}

.upload-btn {
  background-color: #2c662f;
  color: white;
}

.upload-btn:hover {
  background-color: #235024;
}

.remove-btn {
  background-color: #e53e3e;
  color: white;
}

.remove-btn:hover {
  background-color: #c53030;
}

/* 숫자 입력 필드의 화살표 제거 */
input[type="number"]::-webkit-inner-spin-button,
input[type="number"]::-webkit-outer-spin-button {
  -webkit-appearance: none;
  margin: 0;
}
</style>