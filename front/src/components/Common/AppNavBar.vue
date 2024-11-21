<template>
  <nav class="navbar">
    <div class="nav-container">
      <!-- 로고 영역 -->
      <RouterLink :to="{ name: 'home' }" class="logo">
        MoFin
      </RouterLink>

      <!-- 메인 네비게이션 -->
      <div class="nav-links">
        <RouterLink :to="{ name: 'products' }" class="nav-link">상품 조회</RouterLink>
        <RouterLink :to="{ name: 'location' }" class="nav-link">근처 은행 찾기</RouterLink>
        <RouterLink :to="{ name: 'exchangeRate' }" class="nav-link">환율 계산</RouterLink>
        <RouterLink :to="{ name: 'articleList' }" class="nav-link">게시판</RouterLink>
      </div>

      <!-- 인증 관련 버튼 -->
      <div class="auth-buttons">
        <template v-if="!authStore.isLogin">
          <RouterLink :to="{ name: 'signIn' }" class="auth-btn login">로그인</RouterLink>
          <RouterLink :to="{ name: 'signUp' }" class="auth-btn signup">회원가입</RouterLink>
        </template>
        <template v-else>
          <RouterLink :to="{ name: 'profile' }" class="profile-link">
            <span class="profile-icon">👤</span>
            {{ authStore.nickname }}
          </RouterLink>
          <RouterLink :to="{ name: 'signOut' }" class="auth-btn logout">로그아웃</RouterLink>
        </template>
      </div>
    </div>
  </nav>
  <!-- 네비게이션 바 높이만큼 여백 추가 -->
  <div class="nav-spacer"></div>
</template>

<script setup>
import { RouterLink } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const authStore = useAuthStore()
</script>

<style scoped>
.navbar {
  background: white;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  padding: 0.5rem 2rem;  /* 패딩 줄임 */
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 1000;
  height: 60px;  /* 고정 높이 설정 */
}

.nav-spacer {
  height: 60px;  /* navbar의 높이와 동일하게 설정 */
}

.nav-container {
  max-width: 1200px;
  margin: 0 auto;
  display: flex;
  justify-content: space-between;
  align-items: center;
  height: 100%;
}

.logo {
  font-size: 2rem;  /* 폰트 크기 줄임 */
  font-weight: bold;
  color: #2c662f;
  text-decoration: none;
  padding: 0.25rem 0.75rem;  /* 패딩 줄임 */
  border-radius: 6px;
  transition: background-color 0.3s;
  margin-right: 40px;
}

.logo:hover {
  background-color: #f0f9f0;
}

.nav-links {
  display: flex;
  gap: 1.1rem;  /* gap 줄임 */
  align-items: center;
}

.nav-link {
  color: #333;
  text-decoration: none;
  padding: 0.25rem 0.75rem;  /* 패딩 줄임 */
  border-radius: 6px;
  transition: all 0.3s ease;
  font-size: 1.2rem;  /* 폰트 크기 줄임 */
}

.nav-link:hover {
  background-color: #f0f9f0;
  color: #2c662f;
}

.auth-buttons {
  display: flex;
  gap: 0.75rem;  /* gap 줄임 */
  align-items: center;
}

.auth-btn {
  padding: 0.25rem 1rem;  /* 패딩 줄임 */
  border-radius: 6px;
  text-decoration: none;
  font-weight: 500;
  transition: all 0.3s ease;
  font-size: 0.9rem;  /* 폰트 크기 줄임 */
}

.login {
  color: #2c662f;
  border: 1px solid #2c662f;
}

.login:hover {
  background-color: #f0f9f0;
}

.signup {
  background-color: #2c662f;
  color: white;
}

.signup:hover {
  background-color: #235024;
}

.logout {
  color: #666;
  border: 1px solid #ddd;
}

.logout:hover {
  background-color: #f5f5f5;
  border-color: #999;
}

.profile-link {
  display: flex;
  align-items: center;
  gap: 0.3rem;  /* gap 줄임 */
  color: #333;
  text-decoration: none;
  padding: 0.25rem 0.75rem;  /* 패딩 줄임 */
  border-radius: 6px;
  transition: all 0.3s ease;
  font-size: 0.9rem;  /* 폰트 크기 줄임 */
}

.profile-link:hover {
  background-color: #f0f9f0;
}

.profile-icon {
  font-size: 1rem;  /* 아이콘 크기 줄임 */
}

/* 반응형 디자인 */
@media (max-width: 768px) {
  .navbar {
    padding: 0.5rem;
    height: auto;  /* 모바일에서는 자동 높이 */
  }

  .nav-container {
    flex-direction: column;
    gap: 0.5rem;
  }

  .nav-links {
    flex-wrap: wrap;
    justify-content: center;
    gap: 0.3rem;
  }

  .auth-buttons {
    width: 100%;
    justify-content: center;
    padding-bottom: 0.5rem;
  }

  .nav-link, .auth-btn {
    padding: 0.25rem 0.5rem;
    font-size: 0.85rem;
  }

  .nav-spacer {
    height: 120px;  /* 모바일에서는 더 큰 여백 */
  }
}
</style>