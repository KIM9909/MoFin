<template>
  <div class="chart-container">
    <p class="chart-title">
      <span class="chart-icon">{{ type === 'deposit' ? '💰' : '🎯' }}</span>
      {{ type === 'deposit' ? '예금' : '적금' }} 상품 금리 비교
    </p>
    <div v-if="isLoading" class="loading-state">
      <div class="loading-spinner"></div>
      <p>상품 정보를 불러오는 중입니다...</p>
    </div>
    <div v-else-if="!hasData" class="loading-state">
      <p>금리 정보가 없습니다.</p>
    </div>
    <div v-else class="chart-wrapper">
      <Bar
        :data="chartData"
        :options="chartOptions"
      />
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend
} from 'chart.js'
import { Bar } from 'vue-chartjs'

ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend
)

const props = defineProps({
  products: {
    type: Array,
    required: true
  },
  details: {
    type: Object,
    required: true
  },
  type: {
    type: String,
    required: true
  }
})

const isLoading = computed(() => {
  return !props.products || !props.details || Object.keys(props.details).length === 0;
})

const hasData = computed(() => {
  return !isLoading.value && chartData.value.datasets[0].data.length > 0;
})

const chartData = computed(() => {
  if (isLoading.value) return { labels: [], datasets: [] };

  const labels = []
  const savingRates = []
  const preferentialRates = []
  const tooltipLabels = []

  props.products.forEach(product => {
    const detail = props.details[product.fin_prdt_cd]
    if (!detail || !detail.options) return

    labels.push(product.fin_prdt_nm)
    tooltipLabels.push({
      productName: product.fin_prdt_nm,
      bankName: product.kor_co_nm
    })
    
    let maxSavingRate = 0
    let maxPreferentialRate = 0

    detail.options.forEach(opt => {
      const savingRate = parseFloat(opt.intr_rate || 0)
      if (savingRate > maxSavingRate) {
        maxSavingRate = savingRate
      }

      const preferentialRate = parseFloat(opt.intr_rate2 || 0)
      if (preferentialRate > maxPreferentialRate) {
        maxPreferentialRate = preferentialRate
      }
    })

    savingRates.push(parseFloat(maxSavingRate.toFixed(2)))
    preferentialRates.push(parseFloat(maxPreferentialRate.toFixed(2)))
  })

  return {
    labels,
    datasets: [
      {
        label: '저축 금리',
        data: savingRates,
        backgroundColor: 'rgba(16, 185, 129, 0.8)',
        borderColor: 'rgb(16, 185, 129)',
        borderWidth: 1,
        borderRadius: 6,
        hoverBackgroundColor: 'rgb(16, 185, 129)',
        barPercentage: 0.7,
      },
      {
        label: '우대 금리',
        data: preferentialRates,
        backgroundColor: 'rgba(99, 102, 241, 0.8)',
        borderColor: 'rgb(99, 102, 241)',
        borderWidth: 1,
        borderRadius: 6,
        hoverBackgroundColor: 'rgb(99, 102, 241)',
        barPercentage: 0.7,
      }
    ],
    tooltipLabels
  }
})

const chartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  animation: {
    duration: 1000,
    easing: 'easeInOutQuart'
  },
  scales: {
    y: {
      beginAtZero: true,
      title: {
        display: true,
        text: '금리 (%)',
        font: {
          weight: 'bold'
        }
      },
      grid: {
        color: 'rgba(0, 0, 0, 0.05)',
        drawBorder: false
      },
      ticks: {
        padding: 8,
        font: {
          size: 11
        }
      }
    },
    x: {
      grid: {
        display: false
      },
      ticks: {
        maxRotation: 45,
        minRotation: 45,
        padding: 8,
        font: {
          size: 11
        },
        callback: function(value, index) {
          const label = this.getLabelForValue(index)
          if (label.length > 12) {
            return label.substr(0, 12) + '...'
          }
          return label
        }
      }
    }
  },
  plugins: {
    legend: {
      position: 'top',
      labels: {
        padding: 15,
        usePointStyle: true,
        pointStyle: 'circle',
        font: {
          size: 12
        }
      }
    },
    tooltip: {
      backgroundColor: 'rgba(255, 255, 255, 0.95)',
      titleColor: '#1f2937',
      bodyColor: '#4b5563',
      bodyFont: {
        size: 12
      },
      titleFont: {
        size: 13,
        weight: 'bold'
      },
      padding: 12,
      borderWidth: 1,
      borderColor: 'rgba(0, 0, 0, 0.1)',
      callbacks: {
        title: function(context) {
          const dataIndex = context[0].dataIndex
          const tooltipLabel = chartData.value.tooltipLabels[dataIndex]
          return [
            tooltipLabel.productName,
            `${tooltipLabel.bankName}`
          ]
        },
        label: function(context) {
          let label = context.dataset.label || ''
          if (label) {
            label += ': '
          }
          if (context.parsed.y !== null) {
            label += context.parsed.y.toFixed(2) + '%'
          }
          return label
        }
      }
    }
  }
};
</script>

<style scoped>
.chart-container {
  width: 100%;
  padding: 1.5rem;
  background: white;
  border-radius: 12px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1), 0 1px 2px rgba(0, 0, 0, 0.06);
}

.chart-title {
  font-size: 1.25rem;
  font-weight: 600;
  color: #1f2937;
  margin-bottom: 1.5rem;
  text-align: center;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
}

.chart-icon {
  font-size: 1.5rem;
}

.chart-wrapper {
  height: 300px;
  position: relative;
  margin-top: 1rem;
}

.loading-state {
  height: 300px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  color: #6b7280;
  background-color: #f9fafb;
  border-radius: 0.5rem;
  gap: 1rem;
}

.loading-spinner {
  width: 40px;
  height: 40px;
  border: 3px solid #f3f3f3;
  border-top: 3px solid #10b981;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

@media (max-width: 640px) {
  .chart-container {
    padding: 1rem;
  }

  .chart-title {
    font-size: 1.125rem;
  }

  .chart-wrapper {
    height: 250px;
  }
}
</style>