import { defineStore } from 'pinia'
import { ref } from 'vue'
import axios from 'axios'
import { useAuthStore } from '@/stores/auth'  // auth store import 추가

export const useRecommendationStore = defineStore('recommendation', () => {
  const BASE_URL = 'http://127.0.0.1:8000'
  const recommendations = ref(null)
  const financeStatus = ref(null)
  const loading = ref(false)
  const error = ref(null)

  const fetchRecommendations = async () => {
    const authStore = useAuthStore()  // auth store 인스턴스 가져오기
    loading.value = true
    error.value = null
    try {
      const response = await axios.get(`${BASE_URL}/recommendations/get-recommendations/`, {
        headers: {
          'Authorization': `Token ${authStore.token}`
        }
      })
      console.log('추천 데이터:', response.data)
      recommendations.value = response.data
      return response.data
    } catch (err) {
      console.error('API 오류:', err.response || err)
      error.value = err.response?.data?.error || '추천 정보를 가져오는데 실패했습니다.'
      throw error.value
    } finally {
      loading.value = false
    }
  }

  const fetchFinanceStatus = async () => {
    const authStore = useAuthStore()  // auth store 인스턴스 가져오기
    loading.value = true
    error.value = null
    try {
      const response = await axios.get(`${BASE_URL}/recommendations/finance-status/`, {
        headers: {
          'Authorization': `Token ${authStore.token}`
        }
      })
      console.log('재무상태 데이터:', response.data)
      financeStatus.value = response.data
      return response.data
    } catch (err) {
      console.error('API 오류:', err.response || err)
      error.value = err.response?.data?.error || '재무상태 정보를 가져오는데 실패했습니다.'
      throw error.value
    } finally {
      loading.value = false
    }
  }

  return {
    recommendations,
    financeStatus,
    loading,
    error,
    fetchRecommendations,
    fetchFinanceStatus
  }
}, {
  persist: true
})