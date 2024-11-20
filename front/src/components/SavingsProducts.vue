<template>
  <div>
    <!-- 적금 상품 기본 정보 -->
    <p>금융 상품명: {{ savings_product.fin_prdt_nm }}</p>
    <p>금융 회사명: {{ savings_product.kor_co_nm }}</p>
    <p>공시 제출월: {{ savings_product.dcls_month }}</p>
    
    <!-- 상세 정보 보기 버튼 -->
    <button @click="toggleDetails(savings_product.fin_prdt_cd)">
      {{ details ? "닫기" : "상세 보기" }}
    </button>

    <!-- 상세 정보 토글 -->
    <div v-if="details">
      <h3>상세 정보</h3>
      <p>기타 유의사항: {{ details.product.etc_note }}</p>
      <p>가입 대상: {{ details.product.join_member }}</p>
      <p>가입 방법: {{ details.product.join_way }}</p>

      <h4>옵션 정보</h4>
      <ul>
        <li v-for="option in details.options" :key="option.id">
          <p>저축 금리 유형명: {{ option.intr_rate_type_nm }}</p>
          <p>저축 금리: {{ option.intr_rate }}%</p>
          <p>최고 우대금리: {{ option.intr_rate2 }}%</p>
          <p>저축 기간: {{ option.save_trm }}개월</p>
        </li>
      </ul>
    </div>
    
    <hr>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useSavingsStore } from '@/stores/savings'

defineProps({
  savings_product: Object, // 부모로부터 savings_product 객체를 받음
})

const store = useSavingsStore()
const details = ref(null) // 상세 정보를 저장할 변수

// 상세 정보 토글 함수
const toggleDetails = async (fin_prdt_cd) => {
  if (details.value) {
    // 상세 정보가 이미 표시 중이면 닫기
    details.value = null
  } else {
    // 상세 정보가 닫혀 있으면 가져오기
    details.value = await store.getSavingsDetails(fin_prdt_cd)
  }
}
</script>

<style scoped>
/* 버튼 스타일 */
button {
  margin: 10px 0;
  padding: 8px 12px;
  background-color: #4caf50;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

button:hover {
  background-color: #45a049;
}
</style>
