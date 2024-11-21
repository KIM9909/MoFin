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
  };

  // 초기화 시 헤더 설정
  setAxiosAuthHeader();

  // 회원가입
  const signUp = async (payload) => {
    try {
      const response = await axios.post(`${BASE_URL}/accounts/signup/`, {
        username: payload.username,
        email: payload.email,
        password1: payload.password1,
        password2: payload.password2,
        nickname: payload.nickname, // 추가
        birth: payload.birth,      // 추가
        preference: payload.preference  // 추가
      });
      
      console.log('회원가입 성공:', response.data);
      alert('회원가입이 완료되었습니다. 로그인 화면으로 이동합니다.');
      router.push({ name: 'signIn' });
    } catch (error) {
      console.error('회원가입 실패:', error.response?.data);
      let errorMessage = '회원가입에 실패했습니다.';
      if (error.response?.data) {
        // 에러 메시지 처리
        Object.keys(error.response.data).forEach(key => {
          errorMessage = `${key}: ${error.response.data[key].join(' ')}`;
        });
      }
      alert(errorMessage);
      throw error;
    }
  };

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
        userId.value = res.data.pk;
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

  return { signUp, signIn, logout, fetchUserInfo, token, userId, nickname, isLogin };
});
