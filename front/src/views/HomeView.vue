<template>
  <div class="home-container">
    <!-- 히어로 섹션 -->
    <section class="hero-section">
      <div class="container">
        <div class="row align-items-center justify-content-center">
          <!-- 로고 섹션 -->
          <div class="col-12 text-center mb-4">
            <img 
              src="/MoFinLogo2.png" 
              alt="MoFin Logo" 
              class="mofin-logo"
            />
          </div>
          <!-- 메인 컨텐츠 -->
          <div class="col-lg-8 text-center">
            <h1 class="hero-title">당신을 위한 스마트한 금융 파트너</h1>
            <p class="hero-subtitle">
              맞춤형 금융상품 추천부터 실시간 환율 정보까지,<br> MoFin과 함께 시작하세요
            </p>
            <div class="hero-buttons">
              <button @click="$router.push({ name: 'signUp' })" class="btn-primary-gradient">
                시작하기
              </button>
              <button @click="$router.push({ name: 'products' })" class="btn-outline">
                상품 둘러보기
              </button>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- 특징 섹션 -->
    <section class="features-section">
      <div class="container">
        <h2 class="section-title text-center">Why MoFin?</h2>
        <div class="row g-4 justify-content-center">
          <!-- 맞춤형 추천 -->
          <div class="col-md-3">
            <div class="feature-card">
              <div class="feature-icon">
                <i class="bi bi-graph-up-arrow"></i>
              </div>
              <h3>맞춤형 금융상품 추천</h3>
              <p>당신의 생애주기와 재무상태에 맞는 최적의 금융상품을 추천해드립니다.</p>
            </div>
          </div>

          <!-- 실시간 환율 -->
          <div class="col-md-3">
            <div class="feature-card">
              <div class="feature-icon">
                <i class="bi bi-currency-exchange"></i>
              </div>
              <h3>실시간 환율 정보</h3>
              <p>실시간 환율 정보와 함께 편리한 환율 계산기를 제공합니다.</p>
            </div>
          </div>

          <!-- 은행 위치 -->
          <div class="col-md-3">
            <div class="feature-card">
              <div class="feature-icon">
                <i class="bi bi-geo-alt"></i>
              </div>
              <h3>주변 은행 찾기</h3>
              <p>현재 위치 기반으로 가까운 은행 지점을 쉽게 찾아보세요.</p>
            </div>
          </div>

          <!-- 재무 분석 -->
          <div class="col-md-3">
            <div class="feature-card">
              <div class="feature-icon">
                <i class="bi bi-clipboard2-data"></i>
              </div>
              <h3>재무 분석 서비스</h3>
              <p>개인 맞춤형 재무 분석으로 현명한 자산 관리를 도와드립니다.</p>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- CTA 섹션 -->
    <section class="cta-section">
      <div class="container">
        <div class="cta-content">
          <div class="cta-text">
            <h2 class="cta-title">나만의 맞춤 금융 솔루션</h2>
            <p class="cta-subtitle">AI 기반 금융상품 추천 서비스를 시작해보세요</p>
          </div>
          <button @click="$router.push({ name: 'signUp' })" class="cta-button">
            무료로 시작하기
          </button>
        </div>
      </div>
    </section>
  </div>
</template>

<style scoped>
/* 기본 스타일 */
.home-container {
  overflow-x: hidden;
}

/* 히어로 섹션 */
.hero-section {
  background: white;
  padding: 4rem 0;
  position: relative;
}

.mofin-logo {
  width: 200px;
  height: auto;
  margin-bottom: 2rem;
  transition: transform 0.3s ease;
}

.mofin-logo:hover {
  transform: scale(1.05);
}

.hero-title {
  font-size: 2.5rem;
  font-weight: 700;
  color: #2c662f;
  margin-bottom: 1.5rem;
  line-height: 1.2;
}

.hero-subtitle {
  font-size: 1.2rem;
  color: #495057;
  margin-bottom: 2rem;
  max-width: 600px;
  margin-left: auto;
  margin-right: auto;
}

.hero-buttons {
  display: flex;
  gap: 1rem;
  justify-content: center;
}

/* 버튼 스타일 */
.btn-primary-gradient {
  background: #218838;
  color: white;
  padding: 0.8rem 1.8rem;
  border: none;
  border-radius: 50px;
  font-weight: 600;
  transition: all 0.3s ease;
}

.btn-primary-gradient:hover {
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(44, 102, 47, 0.2);
}

.btn-outline {
  background: transparent;
  border: 2px solid #2c662f;
  color: #2c662f;
  padding: 0.8rem 1.8rem;
  border-radius: 50px;
  font-weight: 600;
  transition: all 0.3s ease;
}

.btn-outline:hover {
  background: #2c662f;
  color: white;
}

/* 특징 섹션 */
.features-section {
  padding: 5rem 0;
  background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
}

.section-title {
  font-size: 2rem;
  font-weight: 700;
  color: #2c662f;
  margin-bottom: 3rem;
}

.feature-card {
  background: white;
  padding: 2rem;
  border-radius: 15px;
  box-shadow: 0 5px 20px rgba(0, 0, 0, 0.08);
  transition: all 0.3s ease;
  height: 100%;
  text-align: center;
}

.feature-card:hover {
  transform: translateY(-5px);
}

.feature-icon {
  width: 60px;
  height: 60px;
  background: rgba(44, 102, 47, 0.1);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 1.5rem;
}

.feature-icon i {
  font-size: 1.5rem;
  color: #2c662f;
}

.feature-card h3 {
  font-size: 1.3rem;
  color: #2c662f;
  margin-bottom: 1rem;
}

.feature-card p {
  color: #666;
  font-size: 1rem;
  line-height: 1.6;
}

/* CTA 섹션 */
.cta-section {
  background: white;
  padding: 3rem 0;
  border-top: 1px solid #eee;
  border-bottom: 1px solid #eee;
}

.cta-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  max-width: 1000px;
  margin: 0 auto;
  padding: 0 1rem;
}

.cta-text {
  flex-grow: 1;
}

.cta-title {
  color: #1f2937;
  font-size: 1.75rem;
  font-weight: 700;
  margin-bottom: 0.5rem;
  letter-spacing: -0.02em;
}

.cta-subtitle {
  color: #6b7280;
  font-size: 1.1rem;
  margin: 0;
}

.cta-button {
  background: #3d8e41;
  color: white;
  border: none;
  padding: 0.75rem 2rem;
  border-radius: 8px;
  font-size: 1rem;
  font-weight: 500;
  white-space: nowrap;
  transition: all 0.3s ease;
  box-shadow: 0 2px 6px rgba(44, 102, 47, 0.15);
}

.cta-button:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(44, 102, 47, 0.2);
}

/* 반응형 디자인 */
@media (max-width: 992px) {
  .col-md-3 {
    width: 50%;
  }
}

@media (max-width: 768px) {
  .hero-title {
    font-size: 2rem;
  }
  
  .hero-subtitle {
    font-size: 1rem;
  }
  
  .hero-buttons {
    flex-direction: column;
    gap: 0.8rem;
  }
  
  .btn-primary-gradient,
  .btn-outline {
    width: 100%;
  }

  .section-title {
    font-size: 1.8rem;
  }
  
  .feature-card {
    padding: 1.5rem;
  }
  
  .cta-section {
    padding: 2rem 0;
  }

  .cta-content {
    flex-direction: column;
    text-align: center;
    gap: 1.5rem;
  }

  .cta-title {
    font-size: 1.5rem;
  }

  .cta-subtitle {
    font-size: 1rem;
  }

  .cta-button {
    width: 100%;
  }
}

@media (max-width: 576px) {
  .col-md-3 {
    width: 100%;
  }

  .hero-title {
    font-size: 1.75rem;
  }

  .section-title {
    font-size: 1.5rem;
  }
  
  .feature-card {
    padding: 1.25rem;
  }
  
  .feature-icon {
    width: 50px;
    height: 50px;
  }
  
  .feature-icon i {
    font-size: 1.2rem;
  }
  
  .feature-card h3 {
    font-size: 1.2rem;
  }
  
  .feature-card p {
    font-size: 0.9rem;
  }
}

/* 여백 조정 */
.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 1rem;
}

.row {
  margin: 0 -1rem;
}

.col-12, .col-lg-8, .col-md-3 {
  padding: 0 1rem;
}
</style>