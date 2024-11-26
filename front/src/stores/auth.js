import axios from 'axios';
import { ref, computed } from 'vue';
import { defineStore } from 'pinia';
import { useRouter } from 'vue-router';

export const useAuthStore = defineStore('auth', () => {
  const router = useRouter();
  const BASE_URL = 'http://127.0.0.1:8000';
  const token = ref(null);  // 초기값을 null로 설정
  const userId = ref(null);
  const username = ref("");
  const nickname = ref("");
  const email = ref("");
  const profile_img_url = ref("");
  const userDetails = ref(null);

  const setAxiosAuthHeader = () => {
    axios.defaults.headers.common['Authorization'] = token.value
      ? `Token ${token.value}`
      : '';
  };

  // 토큰 유효성 검증 및 설정
  const validateAndSetToken = async () => {
    const savedToken = localStorage.getItem('token');
    if (!savedToken) return;
    
    try {
      // 토큰 유효성 검증 API 호출
      await axios.post(`${BASE_URL}/accounts/token/verify/`, {
        token: savedToken
      });
      token.value = savedToken;
      setAxiosAuthHeader();
      await fetchUserInfo();
    } catch (error) {
      console.error('토큰 검증 실패:', error);
      logout();  // 유효하지 않은 토큰이면 로그아웃
    }
  };

  // 초기화 시 토큰 검증
  validateAndSetToken().catch(error => {
    console.error('초기 토큰 검증 실패:', error);
  });

  // 회원가입
  const signUp = async (payload) => {
    try {
      const response = await axios.post(
        `${BASE_URL}/accounts/signup/`, 
        payload,
        {
          headers: {
            'Content-Type': payload instanceof FormData ? 
              'multipart/form-data' : 
              'application/json'
          }
        }
      );
      
      console.log('회원가입 성공:', response.data);
      alert('회원가입이 완료되었습니다. 로그인 화면으로 이동합니다.');
      router.push({ name: 'signIn' });
    } catch (error) {
      console.error('회원가입 실패:', error.response?.data);
      let errorMessage = '회원가입에 실패했습니다.';
      if (error.response?.data) {
        Object.keys(error.response.data).forEach(key => {
          errorMessage = `${key}: ${error.response.data[key].join(' ')}`;
        });
      }
      alert(errorMessage);
      throw error;
    }
  };

  // 로그인
  const signIn = async (payload) => {
    try {
      const res = await axios.post(`${BASE_URL}/accounts/login/`, payload);
      token.value = res.data.key;
      localStorage.setItem('token', res.data.key);
      setAxiosAuthHeader();
      
      // 로그인 후 사용자 정보 가져오기
      await fetchUserInfo();
      
      console.log('로그인이 완료되었습니다.');
      router.push({ name: 'home' });
    } catch (err) {
      console.error('로그인 중 오류:', err);
      throw err;
    }
  };

  // 사용자 정보 가져오기
  async function fetchUserInfo() {
    try {
      const res = await axios.get(`${BASE_URL}/accounts/user/`);
      userId.value = res.data.pk;
      username.value = res.data.username
      nickname.value = res.data.nickname;
      email.value = res.data.email;
      profile_img_url.value = res.data.profile_img;
      userDetails.value = {
        birth: res.data.birth,
        preference: res.data.preference,
        annual_income: res.data.annual_income,
        total_assets: res.data.total_assets
      };
      console.log('사용자 정보 로드 완료:', res.data);
    } catch (err) {
      console.error('사용자 정보를 가져오는 중 오류:', err);
      throw err;
    }
  };

  // 로그아웃
  const logout = () => {
    token.value = null;
    userId.value = null;
    username.value = "";
    nickname.value = "";
    email.value = "";
    profile_img_url.value = "";
    userDetails.value = null;
    localStorage.removeItem('token');
    setAxiosAuthHeader();
    console.log('로그아웃되었습니다.');
    router.push({ name: 'home' });  // 로그아웃 후 홈으로 이동
  };

  const isLogin = computed(() => token.value !== null);

  return { 
    signUp, 
    signIn, 
    logout, 
    fetchUserInfo, 
    token, 
    userId,
    username,
    nickname, 
    isLogin, 
    email, 
    profile_img_url, 
    userDetails 
  };
});