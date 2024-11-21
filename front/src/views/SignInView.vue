```vue
<template>
  <div class="login-container">
    <div class="login-card">
      <!-- 로고 섹션 -->
      <div class="logo-section">
        <h1>MoFin</h1>
        <p class="subtitle">금융의 모든 것, MoFin과 함께하세요</p>
      </div>

      <!-- 로그인 폼 -->
      <form @submit.prevent="signIn" class="login-form">
        <div class="form-group">
          <label for="username">아이디</label>
          <div class="input-wrapper">
            <span class="input-icon">👤</span>
            <input 
              type="text" 
              id="username" 
              v-model.trim="username"
              placeholder="아이디를 입력하세요"
              required
              autocomplete="username"
            >
          </div>
        </div>

        <div class="form-group">
          <label for="password">비밀번호</label>
          <div class="input-wrapper">
            <span class="input-icon">🔒</span>
            <input 
              type="password" 
              id="password" 
              v-model.trim="password"
              placeholder="비밀번호를 입력하세요"
              required
              autocomplete="current-password"
            >
          </div>
        </div>

        <button type="submit" class="login-btn">
          로그인
        </button>

        <!-- 추가 링크 -->
        <div class="additional-links">
          <RouterLink to="/signup" class="signup-link">
            회원가입
          </RouterLink>
          <span class="divider">|</span>
          <a href="#" class="forgot-link">비밀번호 찾기</a>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useAuthStore } from '@/stores/auth'

const username = ref(null)
const password = ref(null)
const store = useAuthStore()

const signIn = function () {
  if (!username.value || !password.value) {
    alert('아이디와 비밀번호를 모두 입력해주세요.');
    return;
  }

  const payload = {
    username: username.value,
    password: password.value,
  }
  store.signIn(payload)
}
</script>

<style scoped>
.login-container {
  min-height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  background-color: #f8f9fa;
  padding: 1rem;
}

.login-card {
  background: white;
  border-radius: 16px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  width: 100%;
  max-width: 400px;
  overflow: hidden;
  animation: slideUp 0.5s ease-out;
}

.logo-section {
  background-color: #2c662f;
  padding: 2rem;
  text-align: center;
  color: white;
}

.logo-section h1 {
  font-size: 2.5rem;
  margin: 0;
  font-weight: 700;
}

.subtitle {
  color: rgba(255, 255, 255, 0.8);
  margin-top: 0.5rem;
  font-size: 0.9rem;
}

.login-form {
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
  font-size: 0.9rem;
}

.input-wrapper {
  position: relative;
}

.input-icon {
  position: absolute;
  left: 1rem;
  top: 50%;
  transform: translateY(-50%);
  color: #a0aec0;
}

.input-wrapper input {
  width: 100%;
  padding: 0.75rem 1rem 0.75rem 2.5rem;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  font-size: 1rem;
  transition: all 0.3s ease;
}

.input-wrapper input:focus {
  outline: none;
  border-color: #2c662f;
  box-shadow: 0 0 0 3px rgba(44, 102, 47, 0.1);
}

.input-wrapper input::placeholder {
  color: #a0aec0;
}

.login-btn {
  width: 100%;
  padding: 0.75rem;
  background-color: #2c662f;
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 1rem;
  font-weight: 500;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.login-btn:hover {
  background-color: #235024;
}

.additional-links {
  margin-top: 1.5rem;
  text-align: center;
  font-size: 0.9rem;
}

.signup-link, .forgot-link {
  color: #2c662f;
  text-decoration: none;
  transition: color 0.3s ease;
}

.signup-link:hover, .forgot-link:hover {
  color: #235024;
  text-decoration: underline;
}

.divider {
  margin: 0 0.5rem;
  color: #e2e8f0;
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

/* 반응형 디자인 */
@media (max-width: 480px) {
  .login-card {
    border-radius: 0;
  }

  .logo-section {
    padding: 1.5rem;
  }

  .logo-section h1 {
    font-size: 2rem;
  }

  .login-form {
    padding: 1.5rem;
  }
}
</style>
```