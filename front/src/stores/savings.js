import axios from 'axios'
import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useSavingsStore = defineStore('savings', () => {
  const savingsProducts = ref([])
  const BASE_URL = 'http://127.0.0.1:8000'

  const getSavings = function () {
    axios({
      method: 'get',
      url: `${BASE_URL}/savings/save_savings_products/`
    })
      .then((res) => {
        console.log('적금 데이터를 가져왔습니다.')
        console.log(res)
        savingsProducts.value = res.data.result.baseList
      })
      .catch((err) => {
        console.log('데이터를 가져오지 못했습니다.')
        console.log(err)
      })
  }

  const getSavingsDetails = async function (fin_prdt_cd) {
    try {
      const response = await axios.get(`${BASE_URL}/savings/savings_product_details/${fin_prdt_cd}/`)
      console.log('상세 정보를 가져왔습니다.', response.data)
      console.log(response)
      return response.data // 호출한 컴포넌트에서 데이터를 처리
    } catch (error) {
      console.error('상세 정보를 가져오는 중 오류가 발생했습니다.', error)
    }
  }

  return { savingsProducts, BASE_URL, getSavings, getSavingsDetails }
},
{
  persist: true,
},
)
