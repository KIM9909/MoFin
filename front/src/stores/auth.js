import axios from 'axios';
import { ref, computed } from 'vue';
import { defineStore } from 'pinia';
import { useRouter } from 'vue-router';

export const useAuthStore = defineStore('auth', () => {
  const router = useRouter();
  const BASE_URL = 'http://127.0.0.1:8000';
  const token = ref(localStorage.getItem('token') || null); // 새로고침 시 토큰 복구

  // Axios 기본 인증 헤더 설정
  const setAxiosAuthHeader = () => {
    axios.defaults.headers.common['Authorization'] = token.value
      ? `Token ${token.value}`
      : '';
  };

  // 초기화 시 헤더 설정
  setAxiosAuthHeader();

  // 회원가입
  const signUp = (payload) => {
    axios
      .post(`${BASE_URL}/accounts/signup/`, payload)
      .then(() => {
        console.log('회원가입이 완료되었습니다.');
      })
      .catch((err) => {
        console.error('회원가입 중 오류:', err);
      });
  };

  // 로그인
  const signIn = (payload) => {
    axios
      .post(`${BASE_URL}/accounts/login/`, payload)
      .then((res) => {
        token.value = res.data.key;
        localStorage.setItem('token', res.data.key); // 토큰 저장
        setAxiosAuthHeader();
        console.log('로그인이 완료되었습니다.');
        router.push({ name: 'home' });
      })
      .catch((err) => {
        console.error('로그인 중 오류:', err);
      });
  };

  // 로그아웃
  const logout = () => {
    token.value = null;
    localStorage.removeItem('token'); // 토큰 삭제
    setAxiosAuthHeader();
    console.log('로그아웃되었습니다.');
  };

  // 로그인 여부 확인
  const isLogin = computed(() => token.value !== null);

  return { signIn, signUp, logout, token, isLogin };
});
