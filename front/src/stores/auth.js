import axios from 'axios';
import { ref, computed } from 'vue';
import { defineStore } from 'pinia';
import { useRouter } from 'vue-router';

export const useAuthStore = defineStore('auth', () => {
  const router = useRouter();
  const BASE_URL = 'http://127.0.0.1:8000';
  const token = ref(localStorage.getItem('token') || null); // 새로고침 시 토큰 복구
  const userId = ref(null); // 현재 로그인한 사용자 ID
  const nickname = ref(""); // 사용자 닉네임

  const setAxiosAuthHeader = () => {
    axios.defaults.headers.common['Authorization'] = token.value
      ? `Token ${token.value}`
      : '';
      // console.log('Authorization 헤더:', axios.defaults.headers.common['Authorization']);

  };

  // 초기화 시 헤더 설정
  setAxiosAuthHeader();

  // 로그인
  const signIn = (payload) => {
    axios
      .post(`${BASE_URL}/accounts/login/`, payload)
      .then((res) => {
        token.value = res.data.key;
        localStorage.setItem('token', res.data.key); // 토큰 저장
        setAxiosAuthHeader();

        // 로그인 후 사용자 정보 가져오기
        fetchUserInfo();

        console.log('로그인이 완료되었습니다.');
        router.push({ name: 'home' });
      })
      .catch((err) => {
        console.error('로그인 중 오류:', err);
      });
  };

  // 사용자 정보 가져오기
  const fetchUserInfo = () => {
    axios
      .get(`${BASE_URL}/accounts/user/`)
      .then((res) => {
        // console.log('사용자 정보:', res.data);
        userId.value = res.data.pk;
        // console.log(userId.value)
        nickname.value = res.data.username;
      })
      .catch((err) => {
        console.error('사용자 정보를 가져오는 중 오류:', err);
      });
   };

  // 로그아웃
  const logout = () => {
    token.value = null;
    userId.value = null;
    nickname.value = "";
    localStorage.removeItem('token');
    setAxiosAuthHeader();
    console.log('로그아웃되었습니다.');
  };

  const isLogin = computed(() => token.value !== null);

  return { signIn, logout, token, userId, nickname, isLogin };
});
