<template>
  <v-container fluid class="fill-height bg-grey-lighten-4">
    <v-row align="center" justify="center">
      <v-col cols="12" md="10" lg="8" xl="6">
        <v-card elevation="4" class="text-center pa-12">
          <!-- 로고 영역 -->
          <div class="mb-8">
            <img 
              src="/MoFinLogo.png" 
              alt="MoFin Logo" 
              class="mofin-logo mb-4"
            />
          </div>
          
          <!-- 헤더 영역 -->
          <h1 class="text-h3 font-weight-bold primary--text mb-6">
            MoFin을 찾아주셔서 감사합니다.
          </h1>
          
          <h2 class="text-h4 font-weight-medium grey--text text--darken-1 mb-16">
            최고의 서비스로 보답하겠습니다.
          </h2>
          
          <!-- 서비스 특징 영역 -->
          <v-row class="mt-6">
            <v-col cols="12" md="4">
              <v-card variant="outlined" class="pa-8 h-100">
                <v-icon
                  icon="mdi-account-check"
                  size="x-large"
                  color="primary"
                  class="mb-6"
                ></v-icon>
                <h3 class="text-h5 mb-4">맞춤형 분석</h3>
                <p class="text-body-1">개인별 맞춤 금융 분석을 제공합니다</p>
              </v-card>
            </v-col>
            
            <v-col cols="12" md="4">
              <v-card variant="outlined" class="pa-8 h-100">
                <v-icon
                  icon="mdi-chart-line"
                  size="x-large"
                  color="primary"
                  class="mb-6"
                ></v-icon>
                <h3 class="text-h5 mb-4">실시간 모니터링</h3>
                <p class="text-body-1">24시간 자산을 모니터링합니다</p>
              </v-card>
            </v-col>
            
            <v-col cols="12" md="4">
              <v-card variant="outlined" class="pa-8 h-100">
                <v-icon
                  icon="mdi-shield-check"
                  size="x-large"
                  color="primary"
                  class="mb-6"
                ></v-icon>
                <h3 class="text-h5 mb-4">안전한 보안</h3>
                <p class="text-body-1">철저한 보안 시스템을 제공합니다</p>
              </v-card>
            </v-col>
          </v-row>
          
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup>
// Vuetify 컴포넌트는 자동으로 import됩니다
</script>

<style scoped>
.fill-height {
  min-height: 100vh;
}

.v-card {
  transition: transform 0.3s;
}

.v-card:hover {
  transform: translateY(-5px);
}

/* 로고 스타일 */
.mofin-logo {
  width: 200px;
  height: auto;
  margin: 0 auto;
}

/* 추가된 스타일 */
.v-container {
  max-width: 100%;
}

.text-body-1 {
  line-height: 1.6;
}

/* 반응형 패딩 조정 */
@media (max-width: 600px) {
  .v-card {
    padding: 1rem !important;
  }
  
  .text-h2 {
    font-size: 2rem !important;
  }
  
  .text-h4 {
    font-size: 1.5rem !important;
  }

  .mofin-logo {
    width: 150px;
  }
}
</style>