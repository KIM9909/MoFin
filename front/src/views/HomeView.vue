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
            <h1 class="hero-title">
              당신을 위한 <strong>스마트한 금융 파트너</strong>
            </h1>
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
      <!-- 배경 장식 -->
      <div class="hero-decoration">
        <div class="circle circle-1"></div>
        <div class="circle circle-2"></div>
        <div class="circle circle-3"></div>
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
/* Google Fonts 추가 */
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;500;700&family=Poppins:wght@400;500;600;700&display=swap');

/* 기본 스타일 */
.home-container {
  overflow-x: hidden;
  font-family: 'Noto Sans KR', sans-serif;
}

/* 히어로 섹션 개선 */
.hero-section {
  background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
  padding: 6rem 0;
  position: relative;
  overflow: hidden;
}

/* 배경 장식 스타일 */
.hero-decoration {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
  z-index: 0;
}

.circle {
  position: absolute;
  border-radius: 50%;
  opacity: 0.1;
}

.circle-1 {
  width: 300px;
  height: 300px;
  background: #2c662f;
  top: -100px;
  right: -100px;
}

.circle-2 {
  width: 200px;
  height: 200px;
  background: #218838;
  bottom: -50px;
  left: -50px;
}

.circle-3 {
  width: 150px;
  height: 150px;
  background: #3d8e41;
  top: 50%;
  right: 10%;
}

.mofin-logo {
  width: 220px;
  height: auto;
  margin-bottom: 3rem;
  transition: transform 0.3s ease;
  filter: drop-shadow(0 4px 6px rgba(0, 0, 0, 0.1));
}

.mofin-logo:hover {
  transform: scale(1.05) rotate(-2deg);
}

.hero-title {
  font-size: 3.2rem;
  font-weight: 700;
  color: #1a1a1a;
  margin-bottom: 1.5rem;
  line-height: 1.2;
  font-family: 'Poppins', 'Noto Sans KR', sans-serif;
  letter-spacing: -0.02em;
}

.hero-title strong {
  color: #2c662f;
  display: block;
  margin-top: 0.2em;
}

.hero-subtitle {
  font-size: 1.3rem;
  color: #666;
  margin-bottom: 2.5rem;
  max-width: 600px;
  margin-left: auto;
  margin-right: auto;
  line-height: 1.6;
  font-weight: 300;
}

/* 버튼 스타일 개선 */
.hero-buttons {
  display: flex;
  gap: 1.5rem;
  justify-content: center;
}

.btn-primary-gradient {
  background: linear-gradient(45deg, #218838, #2c662f);
  color: white;
  padding: 1rem 2.2rem;
  border: none;
  border-radius: 50px;
  font-weight: 600;
  font-size: 1.1rem;
  transition: all 0.3s ease;
  font-family: 'Poppins', sans-serif;
}

.btn-primary-gradient:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(44, 102, 47, 0.25);
}

.btn-outline {
  background: transparent;
  border: 2px solid #2c662f;
  color: #2c662f;
  padding: 1rem 2.2rem;
  border-radius: 50px;
  font-weight: 600;
  font-size: 1.1rem;
  transition: all 0.3s ease;
  font-family: 'Poppins', sans-serif;
}

.btn-outline:hover {
  background: #2c662f;
  color: white;
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(44, 102, 47, 0.15);
}

/* 특징 섹션 개선 */
.features-section {
  padding: 7rem 0;
  background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
  position: relative;
}

.section-title {
  font-size: 2.5rem;
  font-weight: 700;
  color: #1a1a1a;
  margin-bottom: 4rem;
  font-family: 'Poppins', 'Noto Sans KR', sans-serif;
  letter-spacing: -0.02em;
}

.feature-card {
  background: white;
  padding: 2.5rem;
  border-radius: 20px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.06);
  transition: all 0.4s ease;
  height: 100%;
  text-align: center;
  position: relative;
  overflow: hidden;
}

.feature-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 4px;
  background: linear-gradient(45deg, #218838, #2c662f);
  opacity: 0;
  transition: all 0.3s ease;
}

.feature-card:hover {
  transform: translateY(-10px);
}

.feature-card:hover::before {
  opacity: 1;
}

.feature-icon {
  width: 80px;
  height: 80px;
  background: rgba(44, 102, 47, 0.08);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 2rem;
  transition: all 0.3s ease;
}

.feature-card:hover .feature-icon {
  background: rgba(44, 102, 47, 0.12);
  transform: scale(1.1);
}

.feature-icon i {
  font-size: 2rem;
  color: #2c662f;
}

.feature-card h3 {
  font-size: 1.4rem;
  color: #1a1a1a;
  margin-bottom: 1rem;
  font-family: 'Poppins', 'Noto Sans KR', sans-serif;
  font-weight: 600;
}

.feature-card p {
  color: #666;
  font-size: 1.05rem;
  line-height: 1.7;
  font-weight: 300;
}

/* CTA 섹션 개선 */
.cta-section {
  background: white;
  padding: 5rem 0;
  position: relative;
  border: none;
}

.cta-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  max-width: 1100px;
  margin: 0 auto;
  padding: 3rem 2rem;
  background: linear-gradient(135deg, #f8f9fa 0%, #ffffff 100%);
  border-radius: 20px;
  box-shadow: 0 15px 40px rgba(0, 0, 0, 0.05);
}

.cta-title {
  color: #1a1a1a;
  font-size: 2rem;
  font-weight: 700;
  margin-bottom: 0.8rem;
  letter-spacing: -0.02em;
  font-family: 'Poppins', 'Noto Sans KR', sans-serif;
}

.cta-subtitle {
  color: #666;
  font-size: 1.2rem;
  margin: 0;
  font-weight: 300;
}

.cta-button {
  background: linear-gradient(45deg, #218838, #2c662f);
  color: white;
  border: none;
  padding: 1rem 2.5rem;
  border-radius: 12px;
  font-size: 1.1rem;
  font-weight: 600;
  white-space: nowrap;
  transition: all 0.3s ease;
  font-family: 'Poppins', sans-serif;
}

.cta-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(44, 102, 47, 0.25);
}

/* 반응형 디자인 개선 */
@media (max-width: 992px) {
  .hero-title {
    font-size: 2.8rem;
  }
  
  .col-md-3 {
    width: 50%;
  }
  
  .cta-content {
    padding: 2.5rem 1.5rem;
  }
}

@media (max-width: 768px) {
  .hero-section {
    padding: 4rem 0;
  }

  .hero-title {
    font-size: 2.4rem;
  }
  
  .hero-subtitle {
    font-size: 1.1rem;
  }
  
  .hero-buttons {
    flex-direction: column;
    gap: 1rem;
  }
  
  .btn-primary-gradient,
  .btn-outline {
    width: 100%;
    padding: 0.9rem 1.8rem;
  }

  .section-title {
    font-size: 2rem;
  }
  
  .feature-card {
    padding: 2rem;
  }
  
  .cta-content {
    flex-direction: column;
    text-align: center;
    gap: 2rem;
    padding: 2rem 1.5rem;
  }
}

@media (max-width: 576px) {
  .hero-title {
    font-size: 2rem;
  }

  .col-md-3 {
    width: 100%;
  }

  .feature-card {
    padding: 1.8rem;
  }
  
  .feature-icon {
    width: 70px;
    height: 70px;
  }
}
</style>