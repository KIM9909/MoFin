import axios from 'axios'
import { defineStore } from 'pinia'
import { ref } from 'vue'


export const useDepositStore = defineStore('deposit', () => {
  const depositProducts = ref([])
  const BASE_URL = 'http://127.0.0.1:8000'

  const getDeposits = function () {
    axios({
      method: 'get',
      url: `${BASE_URL}/interests/save_deposit_products/`
    })
      .then((res) => {
        console.log('예금 데이터를 가져왔습니다.')
        console.log(res)
        depositProducts.value = res.data.result.baseList
      })
      .catch((err) => {
        console.log('데이터를 가져오지 못했습니다.')
        console.log(err)
      })
  }
  
  const getDepositDetails = async function (fin_prdt_cd) {
    try {
      const response = await axios.get(`${BASE_URL}/interests/deposit_product_details/${fin_prdt_cd}/`);
      console.log('상세 정보를 가져왔습니다.', response.data);
      return response.data; // 호출한 컴포넌트에서 데이터를 처리
    } catch (error) {
      console.error('상세 정보를 가져오는 중 오류가 발생했습니다.', error);
    }
  }
  return { depositProducts, BASE_URL, getDeposits, getDepositDetails }
})