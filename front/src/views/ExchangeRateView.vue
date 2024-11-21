<template>
  <div class="calculator-container">
    <div class="calculator-wrapper">
      <!-- 메인 카드 -->
      <div class="main-card">
        <!-- 헤더 섹션 -->
        <div class="header-section">

          <h1>환율 계산기</h1>
          <p class="subtitle">실시간 시장 환율 기준</p>
        </div>

        <!-- 계산기 폼 -->
        <form @submit.prevent="fetchExchangeRate" class="calculator-form">
          <div class="form-grid">
            <!-- 변환 방향 선택 -->
            <div class="form-group">
              <label>
                <span class="label-text">변환 방향</span>
                <div class="custom-select">
                  <span class="select-icon">🔄</span>
                  <select v-model="selectedDirection">
                    <option value="toForeign">KRW → 외화</option>
                    <option value="toKrw">외화 → KRW</option>
                  </select>
                </div>
              </label>
            </div>

            <!-- 통화 선택 -->
            <div class="form-group">
              <label>
                <span class="label-text">대상 통화</span>
                <div class="custom-select">
                  <span class="select-icon">🌐</span>
                  <select v-model="selectedCurrency">
                    <option value="USD">USD - 미국 달러</option>
                    <option value="EUR">EUR - 유로</option>
                    <option value="JPY(100)">JPY - 일본 엔</option>
                    <option value="CNH">CNY - 중국 위안</option>
                    <option value="GBP">GBP - 영국 파운드</option>
                    <option value="AUD">AUD - 호주 달러</option>
                    <option value="CAD">CAD - 캐나다 달러</option>
                    <option value="CHF">CHF - 스위스 프랑</option>
                    <option value="HKD">HKD - 홍콩 달러</option>
                    <option value="SEK">SEK - 스웨덴 크로나</option>
                    <option value="SGD">SGD - 싱가포르 달러</option>
                    <option value="THB">THB - 태국 바트</option>
                  </select>
                </div>
              </label>
            </div>
          </div>

          <!-- 금액 입력 -->
          <div class="form-group amount-group">
            <label>
              <span class="label-text">{{ amountLabel }}</span>
              <div class="amount-input">
                <span class="currency-icon">💵</span>
                <input 
                  type="number" 
                  v-model.number="inputAmount"
                  min="0"
                  step="0.01"
                  placeholder="금액을 입력하세요"
                />
                <span class="currency-code">
                  {{ selectedDirection === 'toForeign' ? 'KRW' : selectedCurrency }}
                </span>
              </div>
            </label>
          </div>

          <!-- 계산 버튼 -->
          <button type="submit" class="calculate-button">
            <span class="button-icon">🔄</span>
            <span>환율 계산하기</span>
          </button>
        </form>

        <!-- 결과 표시 -->
        <div v-if="exchangeResult !== null" class="result-section">
          <div class="result-card">
            <div class="result-header">
              <span class="result-icon">✨</span>
              <span>계산 결과</span>
            </div>
            <div class="result-content">
              <div class="conversion-display">
                <div class="original-amount">
                  <span class="amount">{{ formatNumber(calculationAmount) }}</span>
                  <span class="currency">
                    {{ conversionDirection === 'toForeign' ? 'KRW' : targetCurrency }}
                  </span>
                </div>
                <div class="conversion-arrow">→</div>
                <div class="converted-amount">
                  <span class="amount">{{ formatNumber(exchangeResult) }}</span>
                  <span class="currency">
                    {{ conversionDirection === 'toForeign' ? targetCurrency : 'KRW' }}
                  </span>
                </div>
              </div>
              <div class="exchange-rate">
                <span class="rate-label">적용 환율:</span>
                <span class="rate-value">
                  1 {{ targetCurrency }} = {{ formatNumber(currentRate) }} KRW
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      selectedDirection: "toForeign",
      conversionDirection: "toForeign",
      selectedCurrency: "USD",
      targetCurrency: "USD",
      inputAmount: 1,
      calculationAmount: 1,
      exchangeResult: null,
      lastUpdateTime: null,
      currentRate: null,
    };
  },
  computed: {
    amountLabel() {
      return this.selectedDirection === "toForeign" ? "환전할 금액 (KRW)" : `환전할 금액 (${this.selectedCurrency})`;
    },
  },
  methods: {
    async fetchExchangeRate() {
      this.conversionDirection = this.selectedDirection;
      this.targetCurrency = this.selectedCurrency;
      this.calculationAmount = this.inputAmount;

      try {
        const response = await axios.get("http://127.0.0.1:8000/api/exchange-rate/", {
          params: {
            target: this.targetCurrency,
            date: new Date().toISOString().split("T")[0].replace(/-/g, ""),
          },
        });

        let rate = parseFloat(response.data.rate.replace(",", ""));
        if (this.targetCurrency === "JPY(100)") {
          rate = rate / 100;
        }
        
        this.currentRate = rate;
        this.lastUpdateTime = new Date().toLocaleString();

        if (this.conversionDirection === "toForeign") {
          this.exchangeResult = (this.calculationAmount / rate).toFixed(2);
        } else {
          this.exchangeResult = (this.calculationAmount * rate).toFixed(2);
        }
        this.exchangeResult = parseFloat(this.exchangeResult);
      } catch (error) {
        console.error("환율 정보를 가져오는데 실패했습니다.", error);
        this.exchangeResult = null;
      }
    },
    formatNumber(value) {
      if (value === null || isNaN(value)) return "0";
      return new Intl.NumberFormat().format(value);
    },
  },
  async mounted() {
    await this.fetchExchangeRate();
  }
};
</script>

<style scoped>
.calculator-container {
  min-height: 100vh;
  background: linear-gradient(135deg, #f6f8fb 0%, #e9ecef 100%);
  padding: 2rem;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-top: -30px;
}

.calculator-wrapper {
  width: 100%;
  max-width: 800px;
  animation: slideUp 0.5s ease-out;
}

.main-card {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  border-radius: 24px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
  overflow: hidden;
}

.header-section {
  background: linear-gradient(135deg, #2c3e50 0%, #3498db 100%);
  color: white;
  padding: 2.5rem;
  text-align: center;
}

.header-icon {
  font-size: 3rem;
  margin-bottom: 1rem;
  animation: bounce 2s infinite;
}

.header-section h1 {
  font-size: 2rem;
  font-weight: 700;
  margin: 0;
  margin-bottom: 0.5rem;
}

.subtitle {
  color: rgba(255, 255, 255, 0.8);
  font-size: 1rem;
}

.calculator-form {
  padding: 2rem;
}

.form-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1.5rem;
  margin-bottom: 2rem;
}

.form-group {
  margin-bottom: 1.5rem;
}

.label-text {
  display: block;
  font-size: 0.9rem;
  color: #64748b;
  margin-bottom: 0.5rem;
  font-weight: 500;
}

.custom-select {
  position: relative;
}

.select-icon {
  position: absolute;
  left: 1rem;
  top: 50%;
  transform: translateY(-50%);
  font-size: 1.2rem;
}

select, .amount-input input {
  width: 100%;
  padding: 0.8rem 1rem 0.8rem 3rem;
  border: 1px solid #e2e8f0;
  border-radius: 12px;
  font-size: 1rem;
  background: white;
  transition: all 0.3s ease;
  appearance: none;
}

select:focus, .amount-input input:focus {
  outline: none;
  border-color: #3498db;
  box-shadow: 0 0 0 3px rgba(52, 152, 219, 0.1);
}

.amount-input {
  position: relative;
}

.currency-icon {
  position: absolute;
  left: 1rem;
  top: 50%;
  transform: translateY(-50%);
  font-size: 1.2rem;
}

.currency-code {
  position: absolute;
  right: 1rem;
  top: 50%;
  transform: translateY(-50%);
  color: #64748b;
  font-weight: 500;
}

.calculate-button {
  width: 100%;
  padding: 1rem;
  background: linear-gradient(135deg, #2c3e50 0%, #3498db 100%);
  color: white;
  border: none;
  border-radius: 12px;
  font-size: 1.1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
}

.calculate-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(52, 152, 219, 0.2);
}

.button-icon {
  font-size: 1.2rem;
}

.result-section {
  padding: 0 2rem 2rem 2rem;
}

.result-card {
  background: #f8fafc;
  border-radius: 16px;
  overflow: hidden;
  animation: fadeIn 0.5s ease-out;
}

.result-header {
  background: linear-gradient(135deg, #2c3e50 0%, #3498db 100%);
  color: white;
  padding: 1rem;
  font-weight: 600;
  text-align: center;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
}

.result-content {
  padding: 2rem;
}

.conversion-display {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 1.5rem;
  margin-bottom: 1.5rem;
}

.original-amount, .converted-amount {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.amount {
  font-size: 1.5rem;
  font-weight: 700;
  color: #2c3e50;
}

.currency {
  font-size: 0.9rem;
  color: #64748b;
  margin-top: 0.25rem;
}

.conversion-arrow {
  color: #3498db;
  font-size: 1.5rem;
}

.exchange-rate {
  text-align: center;
  color: #64748b;
  font-size: 0.9rem;
  padding-top: 1rem;
  border-top: 1px solid #e2e8f0;
}

@keyframes slideUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

@keyframes bounce {
  0%, 20%, 50%, 80%, 100% {
    transform: translateY(0);
  }
  40% {
    transform: translateY(-10px);
  }
  60% {
    transform: translateY(-5px);
  }
}

@media (max-width: 768px) {
  .calculator-container {
    padding: 1rem;
  }

  .form-grid {
    grid-template-columns: 1fr;
    gap: 1rem;
  }

  .header-section {
    padding: 2rem;
  }

  .header-section h1 {
    font-size: 1.5rem;
  }

  .amount {
    font-size: 1.2rem;
  }
}
</style>