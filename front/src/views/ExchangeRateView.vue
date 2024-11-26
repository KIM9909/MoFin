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
import axios from "axios"

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
    }
  },
  computed: {
    amountLabel() {
      return this.selectedDirection === "toForeign" ? "환전할 금액 (KRW)" : `환전할 금액 (${this.selectedCurrency})`
    },
  },
  methods: {
        async fetchExchangeRate() {
      this.conversionDirection = this.selectedDirection
      this.targetCurrency = this.selectedCurrency
      this.calculationAmount = this.inputAmount

      try {
        const today = new Date()
        const formattedDate = today.toISOString().split("T")[0].replace(/-/g, "")
        
        const response = await axios.get("http://127.0.0.1:8000/api/exchange-rate/", {
          params: {
            target: this.targetCurrency,
            date: formattedDate
          },
        })

        if (response.data.error) {
          throw new Error(response.data.error)
        }

        let rate = parseFloat(response.data.rate.replace(",", ""))
        if (this.targetCurrency === "JPY(100)") {
          rate = rate / 100
        }
        
        this.currentRate = rate
        this.lastUpdateTime = new Date().toLocaleString()

        if (this.conversionDirection === "toForeign") {
          this.exchangeResult = (this.calculationAmount / rate).toFixed(2)
        } else {
          this.exchangeResult = (this.calculationAmount * rate).toFixed(2)
        }
        this.exchangeResult = parseFloat(this.exchangeResult)
        
      } catch (error) {
        console.error("환율 정보를 가져오는데 실패했습니다.", error)
        alert("환율 정보를 가져오는데 실패했습니다. 잠시 후 다시 시도해주세요.")
        this.exchangeResult = null
      }
    },
    formatNumber(value) {
      if (value === null || isNaN(value)) return "0"
      return new Intl.NumberFormat().format(value)
    },
  },
  async mounted() {
    await this.fetchExchangeRate()
  }
};
</script>

<style scoped>
.calculator-container {
  max-width: 1000px;
  margin: 0 auto;
  padding: 32px 16px;
  background: transparent;
  min-height: auto;
  margin-top: 0;
}

.calculator-wrapper {
  width: 100%;
  animation: fadeIn 0.5s ease-out;
}

.main-card {
  background: white;
  border-radius: 16px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
  overflow: hidden;
  transition: transform 0.3s ease;
}

.header-section {
  background: #5c9c5f 0%;
  color: white;
  padding: 24px;
  text-align: center;
}

.header-section h1 {
  font-size: 24px;
  font-weight: 600;
  margin: 0;
  margin-bottom: 8px;
}

.subtitle {
  color: rgba(255, 255, 255, 0.9);
  font-size: 14px;
}

.calculator-form {
  padding: 24px;
}

.form-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
  margin-bottom: 24px;
}

.form-group {
  margin-bottom: 20px;
}

.label-text {
  display: block;
  font-size: 14px;
  color: #047857;
  margin-bottom: 8px;
  font-weight: 500;
}

.custom-select {
  position: relative;
}

.select-icon {
  position: absolute;
  left: 12px;
  top: 50%;
  transform: translateY(-50%);
  font-size: 16px;
}

select, .amount-input input {
  width: 100%;
  padding: 12px 16px 12px 40px;
  border: 1px solid #d1fae5;
  border-radius: 12px;
  font-size: 14px;
  background: white;
  transition: all 0.3s ease;
  appearance: none;
  color: #065f46;
}

select:hover, .amount-input input:hover {
  border-color: #6ee7b7;
}

select:focus, .amount-input input:focus {
  outline: none;
  border-color: #10b981;
  box-shadow: 0 0 0 3px rgba(16, 185, 129, 0.1);
}

.amount-input {
  position: relative;
}

.currency-icon {
  position: absolute;
  left: 12px;
  top: 50%;
  transform: translateY(-50%);
  font-size: 16px;
}

.currency-code {
  position: absolute;
  right: 12px;
  top: 50%;
  transform: translateY(-50%);
  color: #047857;
  font-weight: 500;
}

.calculate-button {
  width: 100%;
  padding: 12px;
  background: #5c9c5f;
  color: white;
  border: none;
  border-radius: 12px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  box-shadow: 0 4px 6px rgba(5, 150, 105, 0.1);
}

.calculate-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 12px rgba(5, 150, 105, 0.2);
  background: #558f58;
}

.button-icon {
  font-size: 16px;
}

.result-section {
  padding: 0 24px 24px 24px;
}

.result-card {
  background: #f0fdf4;
  border-radius: 12px;
  overflow: hidden;
  animation: fadeIn 0.5s ease-out;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

.result-header {
  background: #5c9c5f;
  color: white;
  padding: 12px;
  font-weight: 600;
  text-align: center;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
}

.result-content {
  padding: 24px;
}

.conversion-display {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 24px;
  margin-bottom: 20px;
}

.original-amount, .converted-amount {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 16px 24px;
  background: white;
  border-radius: 12px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}

.amount {
  font-size: 20px;
  font-weight: 700;
  color: #064e3b;
}

.currency {
  font-size: 14px;
  color: #047857;
  margin-top: 4px;
}

.conversion-arrow {
  color: #059669;
  font-size: 20px;
}

.exchange-rate {
  text-align: center;
  color: #047857;
  font-size: 14px;
  padding-top: 16px;
  border-top: 1px solid #d1fae5;
  background: white;
  margin-top: 16px;
  padding: 16px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}

@keyframes fadeIn {
  from { 
    opacity: 0;
    transform: translateY(10px);
  }
  to { 
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes shimmer {
  0% {
    background-position: -1000px 0;
  }
  100% {
    background-position: 1000px 0;
  }
}

.result-card {
  position: relative;
  overflow: hidden;
}

.result-card::after {
  content: '';
  position: absolute;
  top: 0;
  right: 0;
  bottom: 0;
  left: 0;
  background: linear-gradient(
    90deg,
    rgba(255, 255, 255, 0) 0%,
    rgba(255, 255, 255, 0.2) 50%,
    rgba(255, 255, 255, 0) 100%
  );
  /* animation: shimmer 2s infinite; */
  transform: skewX(-20deg);
}

@media (max-width: 768px) {
  .calculator-container {
    padding: 16px;
  }

  .form-grid {
    grid-template-columns: 1fr;
    gap: 16px;
  }

  .header-section {
    padding: 20px;
  }

  .calculator-form {
    padding: 20px;
  }

  .result-section {
    padding: 0 20px 20px 20px;
  }

  .amount {
    font-size: 18px;
  }

  .header-section h1 {
    font-size: 20px;
  }

  .main-card {
    margin: 0 8px;
  }

  .conversion-display {
    flex-direction: column;
    gap: 16px;
  }

  .conversion-arrow {
    transform: rotate(90deg);
  }
}
</style>