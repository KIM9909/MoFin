<template>
  <nav class="navbar">
    <div class="nav-container">
      <!-- 로고 영역 -->
      <div class="nav-top">
        <RouterLink :to="{ name: 'home' }" class="logo">
          MoFin
        </RouterLink>
        
        <!-- 햄버거 메뉴 버튼 -->
        <button class="menu-toggle" @click="isMenuOpen = !isMenuOpen">
          <span class="hamburger" :class="{ 'active': isMenuOpen }"></span>
        </button>
      </div>
 
      <!-- 메인 네비게이션 -->
      <div class="nav-content" :class="{ 'active': isMenuOpen }">
        <div class="nav-links">
          <RouterLink :to="{ name: 'products' }" class="nav-link" exact @click="isMenuOpen = false">상품 조회</RouterLink>
          <RouterLink :to="{ name: 'location' }" class="nav-link" exact @click="isMenuOpen = false">근처 은행 찾기</RouterLink>
          <RouterLink :to="{ name: 'exchangeRate' }" class="nav-link" exact @click="isMenuOpen = false">환율 계산</RouterLink>
          <RouterLink :to="{ name: 'articleList' }" class="nav-link" exact @click="isMenuOpen = false">게시판</RouterLink>
          <RouterLink :to="{ name: 'recommendations' }" class="nav-link" exact @click="isMenuOpen = false">상품 추천</RouterLink>
          <RouterLink :to="{ name: 'financeStatus' }" class="nav-link" exact @click="isMenuOpen = false">재무 상태</RouterLink>
        </div>
 
        <!-- 인증 관련 버튼 -->
        <div class="auth-buttons">
          <template v-if="!authStore.isLogin">
            <RouterLink :to="{ name: 'signIn' }" class="auth-btn login" exact @click="isMenuOpen = false">로그인</RouterLink>
            <RouterLink :to="{ name: 'signUp' }" class="auth-btn signup" exact @click="isMenuOpen = false">회원가입</RouterLink>
          </template>
          <template v-else>
            <RouterLink :to="{ name: 'profile' }" class="profile-link" exact @click="isMenuOpen = false">
              <span class="profile-icon">👤</span>
              {{ authStore.nickname }}
            </RouterLink>
            <RouterLink 
            :to="{ name: 'signOut' }" 
            class="auth-btn logout" 
            exact 
            @click="handleLogout"
          >
            로그아웃
          </RouterLink>
          </template>
        </div>
      </div>
    </div>
  </nav>
  <!-- 네비게이션 바 높이만큼 여백 추가 -->
  <div class="nav-spacer"></div>
 </template>
 
 <script setup>
 import { RouterLink } from 'vue-router'
 import { useAuthStore } from '@/stores/auth'
 import { useSubscriptionStore } from '@/stores/subscription'  // 추가
 import { ref, onBeforeUnmount, onMounted } from 'vue'
 
 const authStore = useAuthStore()
 const subscriptionStore = useSubscriptionStore()  // 추가
 const isMenuOpen = ref(false)
 
 // 로그아웃 핸들러 추가
 const handleLogout = () => {
   isMenuOpen.value = false
   subscriptionStore.resetSubscriptions()  // 구독 상태 초기화
 }
 
 const handleResize = () => {
   if (window.innerWidth > 1024) {
     isMenuOpen.value = false
   }
 }
 
 onMounted(() => {
   window.addEventListener('resize', handleResize)
 })
 
 onBeforeUnmount(() => {
   window.removeEventListener('resize', handleResize)
 })
 </script>
 
 <style scoped>
 .navbar {
  background: white;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  padding: 0 2rem;
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 1000;
  height: 60px;
 }
 
 .nav-container {
  max-width: 1200px;
  margin: 0 auto;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: space-between;
 }
 
 .nav-top {
  display: flex;
  align-items: center;
  gap: 2rem;
 }
 
 .logo {
  font-size: 1.8rem;
  font-weight: bold;
  color: #2c662f;
  text-decoration: none;
  padding: 0.25rem 0.75rem;
  border-radius: 6px;
  transition: background-color 0.3s;
 }
 
 .logo:hover {
  background-color: #f0f9f0;
 }
 
 .menu-toggle {
  display: none;
  background: none;
  border: none;
  cursor: pointer;
  padding: 0.5rem;
 }
 
 .hamburger {
  display: block;
  width: 24px;
  height: 2px;
  background: #2c662f;
  position: relative;
  transition: all 0.3s ease;
 }
 
 .hamburger::before,
 .hamburger::after {
  content: '';
  position: absolute;
  width: 24px;
  height: 2px;
  background: #2c662f;
  transition: all 0.3s ease;
 }
 
 .hamburger::before {
  top: -6px;
 }
 
 .hamburger::after {
  bottom: -6px;
 }
 
 .hamburger.active {
  background: transparent;
 }
 
 .hamburger.active::before {
  transform: rotate(45deg);
  top: 0;
 }
 
 .hamburger.active::after {
  transform: rotate(-45deg);
  bottom: 0;
 }
 
 .nav-content {
  display: flex;
  align-items: center;
  gap: 2rem;
 }
 
 .nav-links {
  display: flex;
  gap: 1rem;
  align-items: center;
 }
 
 .nav-link {
  color: #333;
  text-decoration: none;
  padding: 0.25rem 0.75rem;
  border-radius: 6px;
  transition: all 0.3s ease;
  font-size: 1rem;
  white-space: nowrap;
 }
 
 .nav-link:hover {
  background-color: #f0f9f0;
  color: #2c662f;
 }
 
 .nav-link.router-link-active {
  background-color: #f0f9f0;
  color: #2c662f;
  font-weight: 600;
 }
 
 .auth-buttons {
  display: flex;
  gap: 0.75rem;
  align-items: center;
 }
 
 .auth-btn {
  padding: 0.25rem 1rem;
  border-radius: 6px;
  text-decoration: none;
  font-weight: 500;
  transition: all 0.3s ease;
  font-size: 0.9rem;
  white-space: nowrap;
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
  gap: 0.3rem;
  color: #333;
  text-decoration: none;
  padding: 0.25rem 0.75rem;
  border-radius: 6px;
  transition: all 0.3s ease;
  font-size: 0.9rem;
  white-space: nowrap;
 }
 
 .profile-link:hover {
  background-color: #f0f9f0;
 }
 
 .profile-link.router-link-active {
  background-color: #f0f9f0;
  font-weight: 600;
 }
 
 .profile-icon {
  font-size: 1rem;
 }
 
 /* 인증 버튼 active 상태 스타일 재정의 */
 .auth-btn.router-link-active {
  font-weight: inherit;
  background-color: inherit;
 }
 
 .signup.router-link-active {
  background-color: #2c662f;
  color: white;
 }
 
 .login.router-link-active {
  background-color: transparent;
  color: #2c662f;
 }
 
 /* Large screens (1024px 이상) */
 @media (min-width: 1025px) {
  .nav-content {
    display: flex !important;
  }
 }
 
 /* Medium screens (768px - 1024px) */
 @media (max-width: 1024px) {
  .navbar {
    height: auto;
    min-height: 60px;
  }
 
  .nav-container {
    flex-direction: column;
    align-items: stretch;
    padding: 0.5rem 0;
  }
 
  .nav-top {
    padding: 0 1rem;
    justify-content: space-between;
  }
 
  .menu-toggle {
    display: block;
  }
 
  .nav-content {
    display: none;
    flex-direction: column;
    padding: 1rem;
    gap: 1rem;
    background: white;
    border-top: 1px solid #eee;
  }
 
  .nav-content.active {
    display: flex;
  }
 
  .nav-links {
    flex-direction: column;
    width: 100%;
    gap: 0.5rem;
  }
 
  .nav-link {
    width: 100%;
    text-align: center;
    padding: 0.5rem;
  }
 
  .auth-buttons {
    flex-direction: column;
    width: 100%;
    gap: 0.5rem;
  }
 
  .auth-btn, .profile-link {
    width: 100%;
    text-align: center;
    justify-content: center;
  }
 }
 
 /* Small screens (768px 이하) */
 @media (max-width: 768px) {
  .navbar {
    padding: 0;
  }
 
  .logo {
    font-size: 1.5rem;
  }
 
  .nav-link {
    font-size: 0.9rem;
  }
 
  .auth-btn {
    font-size: 0.85rem;
  }
 }
 
 .nav-spacer {
  height: 60px;
 }
 
 @media (max-width: 1024px) {
  .nav-spacer {
    height: 60px;
  }
 }
 </style>