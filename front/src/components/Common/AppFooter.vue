<!-- src/components/Common/AppFooter.vue -->
<script setup>
const currentYear = new Date().getFullYear()

const links = [
  { text: '회사소개', url: '#' },
  { text: '개인정보처리방침', url: '#' },
  { text: '이용약관', url: '#' },
  { text: '고객센터', url: '#' },
  { text: '사이트맵', url: '#' }
]


</script>

<template>
  <footer class="footer">
    <div class="footer-content">
      <!-- 메인 링크 영역 -->
      <div class="main-links">
        <nav>
          <ul>
            <li v-for="(link, index) in links" :key="index">
              <a :href="link.url">{{ link.text }}</a>
              <span v-if="index < links.length - 1" class="divider">|</span>
            </li>
          </ul>
        </nav>
      </div>

      <!-- 회사 정보 영역 -->
      <div class="company-info">
        <p>
          사업자등록번호: 123-45-67890 | 
          대표: 김홍범 | 
          Tel: 010-5062-1874 | 
          Email: fkdldj48@naver.com
        </p>
        <p>
          주소: 서울특별시 중구 을지로 100번길 123 | 
          Copyright © {{ currentYear }} Your Company. All Rights Reserved.
        </p>
      </div>
    </div>
  </footer>
</template>

<style scoped>
.footer {
  padding: 0.6rem 0;
  background-color: #f8f9fa;
  border-top: 1px solid #e9ecef;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
}

.footer-content {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 1rem;
}

.main-links {
  margin-bottom: 1.5rem;
  text-align: center;
}

.main-links ul {
  list-style: none;
  padding: 0;
  margin: 0;
  display: flex;
  justify-content: center;
  flex-wrap: wrap;
}

.main-links li {
  display: flex;
  align-items: center;
  margin: 0.25rem 0;
}

.main-links a {
  color: #333;
  text-decoration: none;
  font-size: 0.9rem;
  padding: 0 1rem;
}

.main-links a:hover {
  text-decoration: underline;
}

.divider {
  color: #ccc;
  margin: 0 0.5rem;
}

.company-info {
  text-align: center;
  color: #666;
  font-size: 0.85rem;
  line-height: 1.6;
  margin-bottom: 1.5rem;
}

.company-info p {
  margin: 0.5rem 0;
}


@media (max-width: 768px) {
  .main-links ul {
    flex-direction: column;
    align-items: center;
  }

  .divider {
    display: none;
  }

  .main-links a {
    padding: 0.5rem 1rem;
  }

  .company-info {
    font-size: 0.8rem;
  }
}
</style>