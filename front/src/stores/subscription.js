import axios from 'axios'
import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useSubscriptionStore = defineStore('subscription', () => {
  const subscribedDeposits = ref([])
  const subscribedSavings = ref([])
  const BASE_URL = 'http://127.0.0.1:8000'

  const fetchSubscriptions = async () => {
    try {
      const response = await axios.get(`${BASE_URL}/savings/subscriptions/`)
      subscribedDeposits.value = response.data.deposits
      subscribedSavings.value = response.data.savings
      return response.data
    } catch (error) {
      console.error('구독 정보를 가져오는데 실패했습니다:', error)
      throw error
    }
  }

  const toggleSubscription = async (productType, fin_prdt_cd) => {
    try {
      const response = await axios.post(`${BASE_URL}/savings/subscribe/${productType}/${fin_prdt_cd}/`)
      await fetchSubscriptions()
      return response.data
    } catch (error) {
      console.error('구독 토글 실패:', error)
      throw error
    }
  }

  const isSubscribed = (productType, fin_prdt_cd) => {
    const products = productType === 'deposit' ? subscribedDeposits.value : subscribedSavings.value
    return products.some(product => product.fin_prdt_cd === fin_prdt_cd)
  }

  return {
    subscribedDeposits,
    subscribedSavings,
    fetchSubscriptions,
    toggleSubscription,
    isSubscribed
  }
},
{
  persist: true,
})