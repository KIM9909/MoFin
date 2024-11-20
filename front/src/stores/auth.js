import axios from 'axios'
import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import { useRouter } from 'vue-router'
export const useAuthStore = defineStore('auth', () => {
  const router = useRouter()
  const BASE_URL = 'http://127.0.0.1:8000'
  const token = ref(null)

  const signUp = function (payload) {
    const { username, password1, password2, nickname, birth, preference } = payload

    axios({
      method: 'post',
      url: `${BASE_URL}/accounts/signup/`,
      data: {
        username, password1, password2, nickname, birth, preference
      }
    })
      .then((res) => {
        console.log('회원가입이 완료되었습니다.')
      })
      .catch((err) => {
        console.log(err)
      })
  }

  const signIn = function (payload) {
    const { username, password } = payload

    axios({
      method: 'post',
      url: `${BASE_URL}/accounts/login/`,
      data: {
        username, password
      }
    })
      .then((res) => {
        console.log('로그인이 완료되었습니다.')
        token.value = res.data.key
        router.push({ name: 'home' })
      })
      .catch((err) => {
        console.log(err)
      })
    }

    const isLogin = computed(() => {
      if (token.value === null) {
        return false
      } else {
        return true
      }
    })
    
  return { signIn, signUp, token, isLogin }
})