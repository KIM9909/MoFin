<template>
  <div>
    <h1>환율 계산기</h1>
    <form @submit.prevent="fetchExchangeRate">
      <div>
        <label for="conversion-direction">변환 방향:</label>
        <select v-model="selectedDirection">
          <option value="toForeign">원화 → 외국 통화</option>
          <option value="toKrw">외국 통화 → 원화</option>
        </select>
      </div>
      <div>
        <label for="target-currency">대상 통화:</label>
        <select v-model="selectedCurrency">
          <option value="USD">미국 달러 (USD)</option>
          <option value="EUR">유로 (EUR)</option>
          <option value="JPY(100)">일본 엔 (JPY)</option>
          <option value="CNH">중국 위안 (CNY)</option>
          <option value="GBP">영국 파운드 (GBP)</option>
          <option value="AUD">호주 달러 (AUD)</option>
          <option value="CAD">캐나다 달러 (CAD)</option>
          <option value="CHF">스위스 프랑 (CHF)</option>
          <option value="HKD">홍콩 달러 (HKD)</option>
          <option value="SEK">스웨덴 크로나 (SEK)</option>
          <option value="SGD">싱가포르 달러 (SGD)</option>
          <option value="THB">태국 바트 (THB)</option>
        </select>
      </div>
      <div>
        <label :for="amountLabel">금액:</label>
        <input type="number" v-model.number="inputAmount" />
      </div>
      <button type="submit">계산</button>
    </form>
    <div v-if="exchangeResult !== null">
      <p v-if="conversionDirection === 'toForeign'">
        {{ formatNumber(calculationAmount) }} KRW는 {{ formatNumber(exchangeResult) }} {{ targetCurrency }}입니다.
      </p>
      <p v-if="conversionDirection === 'toKrw'">
        {{ formatNumber(calculationAmount) }} {{ targetCurrency }}는 {{ formatNumber(exchangeResult) }} KRW입니다.
      </p>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      selectedDirection: "toForeign", // 사용자가 선택한 변환 방향
      conversionDirection: "toForeign", // 계산 버튼을 눌렀을 때 업데이트되는 변환 방향
      selectedCurrency: "USD", // 사용자가 선택한 통화
      targetCurrency: "USD", // 계산 버튼을 눌렀을 때 업데이트되는 대상 통화
      inputAmount: 1, // 사용자가 입력한 금액
      calculationAmount: 1, // 계산 버튼을 눌렀을 때 업데이트되는 금액
      exchangeResult: null, // 계산 결과 (숫자)
    };
  },
  computed: {
    amountLabel() {
      return this.selectedDirection === "toForeign" ? "금액 (KRW)" : "금액 (대상 통화)";
    },
  },
  methods: {
    async fetchExchangeRate() {
      // 사용자가 입력한 값으로 업데이트
      this.conversionDirection = this.selectedDirection;
      this.targetCurrency = this.selectedCurrency;
      this.calculationAmount = this.inputAmount;

      try {
        const response = await axios.get("http://127.0.0.1:8000/api/exchange-rate/", {
          params: {
            target: this.targetCurrency,
            date: new Date().toISOString().split("T")[0].replace(/-/g, ""), // YYYYMMDD 형식
          },
        });

        let rate = parseFloat(response.data.rate.replace(",", ""));
        if (this.targetCurrency === "JPY(100)") {
          rate = rate / 100;
        }

        if (this.conversionDirection === "toForeign") {
          // 원화 → 외국 통화
          this.exchangeResult = (this.calculationAmount / rate).toFixed(2);
        } else if (this.conversionDirection === "toKrw") {
          // 외국 통화 → 원화
          this.exchangeResult = (this.calculationAmount * rate).toFixed(2);
        }
        this.exchangeResult = parseFloat(this.exchangeResult); // 문자열을 숫자로 변환
      } catch (error) {
        console.error("환율 정보를 가져오는데 실패했습니다.", error);
        this.exchangeResult = null;
      }
    },
    formatNumber(value) {
      if (value === null || isNaN(value)) return "0"; // NaN 방지
      return new Intl.NumberFormat().format(value);
    },
  },
};
</script>
