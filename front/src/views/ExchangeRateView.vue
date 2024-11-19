<template>
  <div>
    <h1>환율 계산기</h1>
    <form @submit.prevent="fetchExchangeRate">
      <div>
        <label for="target-currency">대상 통화:</label>
        <select v-model="targetCurrency">
          <option value="USD">미국 달러</option>
          <option value="EUR">유로</option>
          <option value="JPY(100)">일본 엔</option>
        </select>
      </div>
      <div>
        <label for="amount">금액 (KRW):</label>
        <input type="number" v-model="amount" />
      </div>
      <button type="submit">계산</button>
    </form>
    <div v-if="exchangeResult">
      <p>{{ amount }} KRW는 {{ exchangeResult }} {{ targetCurrency }}입니다.</p>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      targetCurrency: "USD", // 기본 통화
      amount: 1, // 원화(KRW) 금액
      exchangeResult: null, // 환율 결과
    };
  },
  methods: {
    async fetchExchangeRate() {
      try {
        const response = await axios.get("http://127.0.0.1:8000/api/exchange-rate/", {
          params: {
            target: this.targetCurrency,
            date: new Date().toISOString().split("T")[0].replace(/-/g, ""), // YYYYMMDD 형식
          },
        });

        let rate = parseFloat(response.data.rate.replace(",", "")); // 문자열 환율 값을 숫자로 변환
        if (this.targetCurrency === "JPY(100)") {
          rate = rate / 100; // JPY(100)의 경우 100으로 나눔
        }

        this.exchangeResult = (this.amount / rate).toFixed(2); // 계산된 결과
      } catch (error) {
        console.error("환율 정보를 가져오는데 실패했습니다.", error);
      }
    },
  },
};
</script>
