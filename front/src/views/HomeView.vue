<template>
  <div class="home-container">
    <v-container fluid class="fill-height">
      <v-row align="center" justify="center">
        <v-col cols="12" md="10" lg="8" xl="6">
          <v-card elevation="4" class="main-card">
            <!-- 로고 섹션 -->
            <div class="logo-section">
              <img 
                src="/MoFinLogo.png" 
                alt="MoFin Logo" 
                class="mofin-logo"
              />
            </div>
            
            <!-- 헤더 섹션 -->
            <div class="header-content">
              <h1 class="welcome-title">
                MoFin을 찾아주셔서 감사합니다
              </h1>
              <h2 class="welcome-subtitle">
                최고의 서비스로 보답하겠습니다
              </h2>
            </div>
            
            <!-- 서비스 특징 섹션 -->
            <v-row class="features-grid">
              <v-col cols="12" md="4">
                <div class="feature-card">
                  <div class="icon-wrapper">
                    <v-icon
                      icon="mdi-account-check"
                      size="x-large"
                      color="primary"
                    ></v-icon>
                  </div>
                  <h3>맞춤형 추천</h3>
                  <p>개인의 맞춤 금융 상품 추천 서비스를 제공합니다.</p>
                </div>
              </v-col>
              
              <v-col cols="12" md="4">
                <div class="feature-card">
                  <div class="icon-wrapper">
                    <v-icon
                      icon="mdi-chart-line"
                      size="x-large"
                      color="primary"
                    ></v-icon>
                  </div>
                  <h3>실시간 환율</h3>
                  <p>실시간 환율 계산 서비스를 제공합니다.</p>
                </div>
              </v-col>
              
              <v-col cols="12" md="4">
                <div class="feature-card">
                  <div class="icon-wrapper">
                    <v-icon
                      icon="mdi-shield-check"
                      size="x-large"
                      color="primary"
                    ></v-icon>
                  </div>
                  <h3>위치 서비스</h3>
                  <p>사용자 위치 기반 은행 찾기 서비스를 제공합니다.</p>
                </div>
              </v-col>
            </v-row>
          </v-card>
        </v-col>
      </v-row>
    </v-container>
  </div>
</template>

<script setup>
// Vuetify 컴포넌트는 자동으로 import됩니다
</script>

<style scoped>
.home-container {
  background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
  min-height: 100vh;
}

.main-card {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  border-radius: 24px;
  overflow: hidden;
  padding: 3rem 2rem;
}

.logo-section {
  text-align: center;
  margin-bottom: 3rem;
  animation: fadeInDown 0.8s ease-out;
}

.mofin-logo {
  width: 220px;
  height: auto;
  transition: transform 0.3s ease;
}

.mofin-logo:hover {
  transform: scale(1.05);
}

.header-content {
  text-align: center;
  margin-bottom: 4rem;
  animation: fadeIn 1s ease-out;
}

.welcome-title {
  font-size: 2.5rem;
  font-weight: 700;
  color: #2c662f;
  margin-bottom: 1rem;
  line-height: 1.2;
}

.welcome-subtitle {
  font-size: 1.5rem;
  color: #666;
  font-weight: 500;
}

.features-grid {
  animation: fadeInUp 1.2s ease-out;
}

.feature-card {
  background: white;
  border-radius: 16px;
  padding: 2rem;
  height: 100%;
  transition: all 0.3s ease;
  border: 1px solid rgba(0, 0, 0, 0.08);
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
}

.feature-card:hover {
  transform: translateY(-8px);
  box-shadow: 0 12px 20px rgba(0, 0, 0, 0.1);
  border-color: #2c662f;
}

.icon-wrapper {
  background: rgba(44, 102, 47, 0.1);
  width: 80px;
  height: 80px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 1.5rem;
  transition: all 0.3s ease;
}

.feature-card:hover .icon-wrapper {
  background: #2c662f;
}

.feature-card:hover .icon-wrapper .v-icon {
  color: white !important;
}

.feature-card h3 {
  font-size: 1.4rem;
  color: #2c662f;
  margin-bottom: 1rem;
  font-weight: 600;
}

.feature-card p {
  color: #666;
  line-height: 1.6;
  margin: 0;
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

@keyframes fadeInDown {
  from {
    opacity: 0;
    transform: translateY(-20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* 반응형 디자인 */
@media (max-width: 960px) {
  .main-card {
    padding: 2rem 1rem;
  }

  .welcome-title {
    font-size: 2rem;
  }

  .welcome-subtitle {
    font-size: 1.2rem;
  }

  .mofin-logo {
    width: 180px;
  }

  .feature-card {
    padding: 1.5rem;
    margin-bottom: 1rem;
  }

  .icon-wrapper {
    width: 60px;
    height: 60px;
  }
}

@media (max-width: 600px) {
  .welcome-title {
    font-size: 1.8rem;
  }

  .icon-wrapper {
    width: 50px;
    height: 50px;
  }

  .feature-card h3 {
    font-size: 1.2rem;
  }
}
</style>