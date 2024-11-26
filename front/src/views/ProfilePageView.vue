<template>
  <div class="profile-container">
    <!-- 사이드바 -->
    <aside class="sidebar">
      <div class="user-info">
        <div class="user-avatar">
          <img 
            v-if="auth.profile_img_url" 
            :src="auth.profile_img_url" 
            alt="Profile"
            class="avatar-image"
          >
          <span v-else>{{ auth.nickname?.charAt(0) }}</span>
        </div>
        <h2 class="user-name">{{ auth.nickname }}</h2>
      </div>

      <nav class="menu-list">
        <button 
          v-for="menu in menuItems"
          :key="menu.id"
          class="menu-item"
          :class="{ 'active': activeMenu === menu.id }"
          @click="activeMenu = menu.id"
        >
          <span class="icon">{{ menu.icon }}</span>
          {{ menu.label }}
        </button>
      </nav>
    </aside>

    <!-- 메인 컨텐츠 -->
    <main class="main-content">
      <!-- 회원정보 섹션 -->
      <div v-if="activeMenu === 'info'" class="content-section">
        <div class="section-header">
          <h1>회원정보</h1>
        </div>

        <div class="content-card">
        <div v-if="!isEditing">
          <div class="profile-image-section">
            <div class="current-image">
              <img 
                v-if="auth.profile_img_url" 
                :src="auth.profile_img_url" 
                alt="Profile"
                class="profile-preview"
              >
              <div v-else class="profile-placeholder">
                {{ auth.nickname?.charAt(0) }}
              </div>
            </div>
            <div class="image-upload">
              <input 
                type="file" 
                ref="fileInput" 
                @change="handleImageChange" 
                accept="image/*"
                class="file-input"
                hidden
              >
              <button 
                @click="$refs.fileInput.click()"
                class="upload-btn"
              >
                이미지 변경
              </button>
              <button 
                v-if="auth.profile_img_url"
                @click="removeProfileImage"
                class="remove-btn"
              >
                이미지 삭제
              </button>
            </div>
          </div>
          <!-- 기존 정보 표시 부분 -->
          <div class="info-row">
            <label class="fw-bold">사용자 이름</label>
            <p>{{ auth.username }}</p>
          </div>
          <div class="info-row">
            <label class="fw-bold">닉네임</label>
            <p>{{ auth.nickname }}</p>
          </div>
          <div class="info-row">
            <label class="fw-bold">이메일</label>
            <p>{{ auth.email }}</p>
          </div>
          <div class="info-row">
            <label class="fw-bold">생일</label>
            <p>{{ auth.userDetails.birth }}</p>
          </div>
          <div class="info-row">
            <label class="fw-bold">연간 소득</label>
            <p>{{ auth.userDetails.annual_income }}</p>
          </div>
          <div class="info-row">
            <label class="fw-bold">자산</label>
            <p>{{ auth.userDetails.total_assets }}</p>
          </div>
          <div class="info-row">
            <label class="fw-bold">선호도</label>
            <p>{{ auth.userDetails.preference }}</p>
          </div>
          <button @click="startEditing" class="primary-btn">
            정보 수정
          </button>
        </div>

          <form v-else @submit.prevent="updateProfile" class="edit-form">
            <div class="form-group">
              <label>닉네임</label>
              <input
                v-model="editForm.nickname"
                type="text"
                required
              >
            </div>
            <div class="form-group">
              <label>이메일</label>
              <input
                v-model="editForm.email"
                type="email"
                required
              >
            </div>
            <div class="form-group">
              <label>생일</label>
              <input
                v-model="editForm.birth"
                type="date"
                required
              >
            </div>
            <div class="form-group">
              <label>연간 소득</label>
              <input
                v-model="editForm.annual_income"
                type="number"
                required
              >
            </div>
            <div class="form-group">
              <label>자산</label>
              <input
                v-model="editForm.total_assets"
                type="number"
                required
              >
            </div>
            <div class="form-group">
              <label>선호도</label>
              <div class="select-wrapper">
                <span class="select-icon">👛</span>
                <select
                  v-model="editForm.preference"
                  class="form-select"
                  required
                >
                  <option value="">선택하세요</option>
                  <option value="안정형">안정형</option>
                  <option value="위험회피형">위험회피형</option>
                  <option value="수익추구형">수익추구형</option>
                </select>
              </div>
            </div>
            <div class="button-group">
              <button type="submit" class="primary-btn">저장</button>
              <button type="button" @click="cancelEditing" class="secondary-btn">
                취소
              </button>
            </div>
          </form>
        </div>
      </div>

      <!-- 보안설정 섹션 -->
      <div v-if="activeMenu === 'security'" class="content-section">
        <div class="section-header">
          <h1>보안설정</h1>
        </div>

        <div class="content-card">
          <form @submit.prevent="updatePassword" class="password-form">
            <div class="form-group">
              <label>현재 비밀번호</label>
              <input
                v-model="passwordForm.old_password"
                type="password"
                required
              >
            </div>
            <div class="form-group">
              <label>새 비밀번호</label>
              <input
                v-model="passwordForm.new_password1"
                type="password"
                required
              >
            </div>
            <div class="form-group">
              <label>새 비밀번호 확인</label>
              <input
                v-model="passwordForm.new_password2"
                type="password"
                required
              >
            </div>
            <button type="submit" class="primary-btn">
              비밀번호 변경
            </button>
          </form>
        </div>
      </div>

      <!-- 가입 상품 섹션 -->
      <div v-if="activeMenu === 'subscriptions'" class="content-section">
        <div class="section-header">
          <h1>가입 상품 목록</h1>
        </div>

        <!-- 예금 상품 -->
        <div class="content-card">
          <h2 class="product-section-title">예금 상품</h2>
          <div v-if="subscriptionStore.subscribedDeposits.length === 0" class="empty-state">
            <div class="empty-icon">💰</div>
            <p>가입한 예금 상품이 없습니다.</p>
          </div>
          <div v-else>
            <!-- 금리 비교 차트 -->
            <InterestRateChart 
              :products="subscriptionStore.subscribedDeposits"
              :details="depositDetails"
              type="deposit"
            />
            <!-- 상품 목록 -->
            <div class="subscribed-products mt-4">
              <div 
                v-for="product in subscriptionStore.subscribedDeposits" 
                :key="product.fin_prdt_cd" 
                class="product-card"
              >
                <div class="product-info">
                  <h3>{{ product.fin_prdt_nm }}</h3>
                  <p class="bank-name">{{ product.kor_co_nm }}</p>
                  <div class="product-actions">
                    <button 
                      @click="showProductDetail('deposit', product)"
                      class="detail-btn"
                    >
                      상세 정보
                    </button>
                    <button 
                      @click="handleUnsubscribe('deposit', product.fin_prdt_cd)"
                      class="unsubscribe-btn"
                    >
                      가입 취소
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- 적금 상품 -->
        <div class="content-card mt-4">
          <h2 class="product-section-title">적금 상품</h2>
          <div v-if="subscriptionStore.subscribedSavings.length === 0" class="empty-state">
            <div class="empty-icon">🎯</div>
            <p>가입한 적금 상품이 없습니다.</p>
          </div>
          <div v-else>
            <!-- 금리 비교 차트 -->
            <InterestRateChart 
              :products="subscriptionStore.subscribedSavings"
              :details="savingsDetails"
              type="savings"
            />
            <!-- 상품 목록 -->
            <div class="subscribed-products mt-4">
              <div 
                v-for="product in subscriptionStore.subscribedSavings" 
                :key="product.fin_prdt_cd" 
                class="product-card"
              >
                <div class="product-info">
                  <h3>{{ product.fin_prdt_nm }}</h3>
                  <p class="bank-name">{{ product.kor_co_nm }}</p>
                  <div class="product-actions">
                    <button 
                      @click="showProductDetail('savings', product)"
                      class="detail-btn"
                    >
                      상세 정보
                    </button>
                    <button 
                      @click="handleUnsubscribe('savings', product.fin_prdt_cd)"
                      class="unsubscribe-btn"
                    >
                      가입 취소
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- 좋아요한 게시글 섹션 -->
      <div v-if="activeMenu === 'likes'" class="content-section">
        <div class="section-header">
          <h1>좋아요한 게시글</h1>
        </div>

        <div class="content-card">
          <div v-if="likedArticles.length === 0" class="empty-state">
            <div class="empty-icon">❤️</div>
            <p>아직 좋아요한 게시글이 없습니다.</p>
          </div>

          <div v-else class="liked-articles">
            <div v-for="article in likedArticles" :key="article.id" class="liked-article">
              <RouterLink 
                :to="{ name: 'articleDetail', params: { id: article.id }}"
                class="article-link"
              >
                <h3>{{ article.title }}</h3>
                <p class="article-excerpt">{{ article.content }}</p>
                <div class="article-meta">
                  <span class="like-count">❤️ {{ article.like_count }}</span>
                  <span class="date">{{ formatDate(article.created_at) }}</span>
                </div>
              </RouterLink>
            </div>
          </div>
        </div>
      </div>

      <!-- 탈퇴하기 섹션 -->
      <div v-if="activeMenu === 'delete'" class="content-section">
        <div class="section-header">
          <h1>회원 탈퇴</h1>
        </div>

        <div class="content-card warning">
          <div class="warning-icon">⚠️</div>
          <h2>회원 탈퇴 전 꼭 확인해주세요</h2>
          <p>
            탈퇴 시 모든 데이터가 삭제되며 복구할 수 없습니다.
            신중하게 결정해 주세요.
          </p>
          <button @click="confirmDelete" class="danger-btn">
            회원 탈퇴
          </button>
        </div>
      </div>
    </main>

    <!-- 상품 상세 정보 모달 -->
    <ProductDetailModal
      v-if="activeMenu === 'subscriptions'"
      :is-open="!!selectedProduct"
      :product="selectedProduct"
      :details="productDetails"
      :is-subscribed="true"
      @close="closeModal"
      @toggle-subscription="handleUnsubscribe"
    />
  </div>
</template>


<script setup>
import { ref, onMounted, watch } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useRouter } from 'vue-router'
import axios from 'axios'
import ProductDetailModal from '@/components/ProductDetailModal.vue'
import { useSubscriptionStore } from '@/stores/subscription'
import { useDepositStore } from '@/stores/deposit'
import { useSavingsStore } from '@/stores/savings'
import InterestRateChart from '@/components/InterestRateChart.vue'

const router = useRouter()
const auth = useAuthStore()
const subscriptionStore = useSubscriptionStore()
const depositStore = useDepositStore()
const savingsStore = useSavingsStore()

const isEditing = ref(false)
const activeMenu = ref('info')
const likedArticles = ref([])
const selectedProduct = ref(null)
const productDetails = ref(null)
const depositDetails = ref({})
const savingsDetails = ref({})

const formatDate = (dateString) => {
  if (!dateString) return ''
  
  const date = new Date(dateString)
  const options = { 
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  }
  
  return new Date(dateString).toLocaleDateString('ko-KR', options)
}

// 폼 초기화 추가
const editForm = ref({
 nickname: '',
 email: '',
 birth: null,
 preference: null,
 annual_income: null,
 total_assets: null,
})

const passwordForm = ref({
 old_password: '',
 new_password1: '',
 new_password2: ''
})

// 메뉴 아이템 정의
const menuItems = [
 { id: 'info', icon: '👤', label: '회원정보' },
 { id: 'security', icon: '🔒', label: '보안설정' },
 { id: 'subscriptions', icon: '💰', label: '가입 상품' },
 { id: 'likes', icon: '❤️', label: '좋아요한 게시글' },
 { id: 'delete', icon: '⚠️', label: '탈퇴하기' }
]

// 상품별 상세 정보 로드 함수
const loadProductDetails = async (products, type) => {
 const details = {}
 for (const product of products) {
   try {
     let response
     if (type === 'deposit') {
       response = await depositStore.getDepositDetails(product.fin_prdt_cd)
     } else {
       response = await savingsStore.getSavingsDetails(product.fin_prdt_cd)
     }
     details[product.fin_prdt_cd] = response
   } catch (error) {
     console.error(`상품 상세 정보 로드 실패 (${product.fin_prdt_cd}):`, error)
   }
 }
 return details
}

// 상품 상세 정보 표시
const showProductDetail = async (type, product) => {
 try {
   selectedProduct.value = { ...product, type }
   if (type === 'deposit') {
     const response = await depositStore.getDepositDetails(product.fin_prdt_cd)
     productDetails.value = {
       product: response.product,
       options: response.options
     }
   } else {
     const response = await savingsStore.getSavingsDetails(product.fin_prdt_cd)
     productDetails.value = {
       product: response.product,
       options: response.options
     }
   }
 } catch (error) {
   console.error('상품 상세 정보를 가져오는데 실패했습니다:', error)
   selectedProduct.value = null
   productDetails.value = null
   alert('상품 정보를 불러오는데 실패했습니다.')
 }
}

// 가입 취소 처리
const handleUnsubscribe = async (productType, productId) => {
 try {
   const result = await subscriptionStore.toggleSubscription(productType, productId)
   alert(result.message)
   await subscriptionStore.fetchSubscriptions()
 } catch (error) {
   console.error('가입 취소 실패:', error)
   alert('가입 취소 중 오류가 발생했습니다.')
 }
}

// 모달 닫기
const closeModal = () => {
 selectedProduct.value = null
 productDetails.value = null
}

// 컴포넌트 마운트 시 초기 데이터 로드
onMounted(async () => {
 try {
   await auth.fetchUserInfo()
   if (auth.isLogin && activeMenu.value === 'subscriptions') {
     await subscriptionStore.fetchSubscriptions()
     // 초기 상세 정보 로드
     if (subscriptionStore.subscribedDeposits.length > 0) {
       depositDetails.value = await loadProductDetails(
         subscriptionStore.subscribedDeposits, 
         'deposit'
       )
     }
     if (subscriptionStore.subscribedSavings.length > 0) {
       savingsDetails.value = await loadProductDetails(
         subscriptionStore.subscribedSavings, 
         'savings'
       )
     }
   }
 } catch (error) {
   console.error('데이터 로딩 실패:', error)
   alert('데이터를 불러오는데 실패했습니다.')
 }
})

// 메뉴 변경 시 데이터 로드
watch(activeMenu, async (newValue) => {
 if (newValue === 'subscriptions') {
   await subscriptionStore.fetchSubscriptions()
   // 상세 정보 로드
   if (subscriptionStore.subscribedDeposits.length > 0) {
     depositDetails.value = await loadProductDetails(
       subscriptionStore.subscribedDeposits, 
       'deposit'
     )
   }
   if (subscriptionStore.subscribedSavings.length > 0) {
     savingsDetails.value = await loadProductDetails(
       subscriptionStore.subscribedSavings, 
       'savings'
     )
   }
 } else if (newValue === 'likes') {
   await fetchLikedArticles()
 }
})

// 좋아요한 게시글 불러오기
const fetchLikedArticles = async () => {
 try {
   const response = await axios.get('http://127.0.0.1:8000/articles/articles/likes/', {
     headers: {
       Authorization: `Token ${auth.token}`
     }
   })
   likedArticles.value = response.data
 } catch (error) {
   console.error('좋아요한 게시글을 불러오는데 실패했습니다:', error)
 }
}

// 수정 모드 시작
const startEditing = () => {
 isEditing.value = true
 editForm.value.nickname = auth.nickname
 editForm.value.email = auth.email
 editForm.value.birth = auth.userDetails.birth
 editForm.value.preference = auth.userDetails.preference
 editForm.value.annual_income = auth.userDetails.annual_income
 editForm.value.total_assets = auth.userDetails.total_assets
}

// 수정 취소
const cancelEditing = () => {
 isEditing.value = false
}

// 프로필 업데이트
const updateProfile = async () => {
  try {
    // 현재 값과 다른 경우에만 업데이트할 데이터 포함
    const updateData = {}
    
    // nickname이 변경된 경우
    if (editForm.value.nickname !== auth.nickname) {
      updateData.nickname = editForm.value.nickname
    }
    
    // email이 변경된 경우
    if (editForm.value.email !== auth.email) {
      updateData.email = editForm.value.email
    }
    
    // birth가 변경된 경우
    if (editForm.value.birth !== auth.userDetails.birth) {
      updateData.birth = editForm.value.birth
    }
    
    // preference가 변경된 경우
    if (editForm.value.preference !== auth.userDetails.preference) {
      updateData.preference = editForm.value.preference
    }
    
    // annual_income이 변경된 경우
    if (editForm.value.annual_income !== auth.userDetails.annual_income) {
      updateData.annual_income = editForm.value.annual_income
    }
    
    // total_assets이 변경된 경우
    if (editForm.value.total_assets !== auth.userDetails.total_assets) {
      updateData.total_assets = editForm.value.total_assets
    }

    await axios.put('http://127.0.0.1:8000/accounts/update/', updateData, {
      headers: {
        Authorization: `Token ${auth.token}`,
        'Content-Type': 'application/json',
      }
    })

    await auth.fetchUserInfo()
    isEditing.value = false
    alert('프로필이 성공적으로 업데이트되었습니다.')
  } catch (error) {
    console.error('프로필 업데이트 실패:', error)
    if (error.response?.data) {
      let errorMessage = ''
      Object.keys(error.response.data).forEach(key => {
        errorMessage += `${key}: ${error.response.data[key].join(', ')} `
      })
      alert(`프로필 업데이트에 실패했습니다: ${errorMessage}`)
    } else {
      alert('프로필 업데이트에 실패했습니다.')
    }
  }
};

// 비밀번호 변경
const updatePassword = async () => {
 if (passwordForm.value.new_password1 !== passwordForm.value.new_password2) {
   alert('새 비밀번호가 일치하지 않습니다.')
   return
 }

 try {
   await axios.post('http://127.0.0.1:8000/accounts/password/change/', {
     old_password: passwordForm.value.old_password,
     new_password1: passwordForm.value.new_password1,
     new_password2: passwordForm.value.new_password2
   }, {
     headers: {
       Authorization: `Token ${auth.token}`
     }
   })

   passwordForm.value = {
     old_password: '',
     new_password1: '',
     new_password2: ''
   }

   alert('비밀번호가 성공적으로 변경되었습니다.')
   activeMenu.value = 'info'
 } catch (error) {
   console.error('비밀번호 변경 실패:', error)
   if (error.response?.data) {
     alert(`비밀번호 변경에 실패했습니다: ${JSON.stringify(error.response.data)}`)
   } else {
     alert('비밀번호 변경에 실패했습니다.')
   }
 }
}

// 계정 삭제
const confirmDelete = async () => {
 if (confirm('정말로 계정을 삭제하시겠습니까? 이 작업은 되돌릴 수 없습니다.')) {
   try {
     await axios.delete('http://127.0.0.1:8000/accounts/delete/', {
       headers: {
         Authorization: `Token ${auth.token}`
       }
     })
     
     auth.logout()
     router.push({ name: 'home' })
     alert('계정이 성공적으로 삭제되었습니다.')
   } catch (error) {
     console.error('계정 삭제 실패:', error)
     if (error.response?.data) {
       alert(`계정 삭제 실패: ${JSON.stringify(error.response.data)}`)
     } else {
       alert('계정 삭제에 실패했습니다.')
     }
   }
 }
}

const handleImageChange = async (event) => {
  const file = event.target.files[0]
  if (!file) return
  
  // 파일 크기 체크 (5MB 제한)
  if (file.size > 5 * 1024 * 1024) {
    alert('파일 크기는 5MB를 초과할 수 없습니다.')
    return
  }
  
  try {
    const formData = new FormData()
    formData.append('profile_img', file)
    
    await axios.patch('http://127.0.0.1:8000/accounts/user/', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
        'Authorization': `Token ${auth.token}`
      }
    })
    
    await auth.fetchUserInfo()
    alert('프로필 이미지가 업데이트되었습니다.')
  } catch (error) {
    console.error('이미지 업로드 실패:', error)
    alert('이미지 업로드에 실패했습니다.')
  }
  
  // 파일 입력 초기화
  event.target.value = ''
}

const removeProfileImage = async () => {
  if (!confirm('프로필 이미지를 삭제하시겠습니까?')) return
  
  try {
    const formData = new FormData()
    formData.append('profile_img', '')
    
    await axios.patch('http://127.0.0.1:8000/accounts/user/', formData, {
      headers: {
        'Authorization': `Token ${auth.token}`
      }
    })
    
    await auth.fetchUserInfo()
    alert('프로필 이미지가 삭제되었습니다.')
  } catch (error) {
    console.error('이미지 삭제 실패:', error)
    alert('이미지 삭제에 실패했습니다.')
  }
}

</script>

<style scoped>

.mt-4 {
  margin-top: 1rem;
}

.product-section-title {
  font-size: 1.25rem;
  font-weight: 600;
  color: #1f2937;
  margin-bottom: 1.5rem;
}

.profile-container {
  display: flex;
  min-height: 100vh;
  background-color: #f5f7fa;
}

/* 사이드바 스타일링 */
.sidebar {
  width: 250px;
  background-color: white;
  padding: 2rem;
  box-shadow: 2px 0 5px rgba(0, 0, 0, 0.05);
}

.user-info {
  text-align: center;
  margin-bottom: 2rem;
}

.user-avatar {
  width: 80px;
  height: 80px;
  background-color: #10b981;
  color: white;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 2rem;
  margin: 0 auto 1rem;
}

.user-name {
  font-size: 1.25rem;
  font-weight: 600;
  color: #1f2937;
}

.menu-list {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.menu-item {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.75rem 1rem;
  border-radius: 0.5rem;
  color: #4b5563;
  transition: all 0.2s;
  border: none;
  background: none;
  width: 100%;
  text-align: left;
  cursor: pointer;
}

.menu-item:hover {
  background-color: #f3f4f6;
}

.menu-item.active {
  background-color: #10b981;
  color: white;
}

/* 메인 컨텐츠 영역 */
.main-content {
  flex: 1;
  padding: 2rem;
  overflow-y: auto;
}

.content-section {
  max-width: 800px;
  margin: 0 auto;
}

.section-header {
  margin-bottom: 2rem;
}

.section-header h1 {
  font-size: 1.875rem;
  font-weight: 600;
  color: #1f2937;
}

/* 카드 스타일링 */
.content-card {
  background-color: white;
  border-radius: 0.75rem;
  padding: 2rem;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

/* 폼 스타일링 */
.form-group {
  margin-bottom: 1.5rem;
}

.form-group label {
  display: block;
  font-weight: 500;
  margin-bottom: 0.5rem;
  color: #374151;
}

.form-group input {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #d1d5db;
  border-radius: 0.5rem;
  transition: border-color 0.2s;
}

.form-group input:focus {
  border-color: #10b981;
  outline: none;
  box-shadow: 0 0 0 2px rgba(79, 70, 229, 0.1);
}

/* 버튼 스타일링 */
.primary-btn {
  background-color: #10b981;
  color: white;
  padding: 0.75rem 1.5rem;
  border-radius: 0.5rem;
  border: none;
  font-weight: 500;
  cursor: pointer;
  transition: background-color 0.2s;
}

.primary-btn:hover {
  background-color: #4338ca;
}

.secondary-btn {
  background-color: #e5e7eb;
  color: #374151;
  padding: 0.75rem 1.5rem;
  border-radius: 0.5rem;
  border: none;
  font-weight: 500;
  cursor: pointer;
  transition: background-color 0.2s;
}

.secondary-btn:hover {
  background-color: #d1d5db;
}

.danger-btn {
  background-color: #ef4444;
  color: white;
  padding: 0.75rem 1.5rem;
  border-radius: 0.5rem;
  border: none;
  font-weight: 500;
  cursor: pointer;
  transition: background-color 0.2s;
}

.danger-btn:hover {
  background-color: #dc2626;
}

/* 상품 카드 스타일링 */
.product-section-title {
  font-size: 1.25rem;
  font-weight: 600;
  color: #1f2937;
  margin-bottom: 1.5rem;
}

.product-card {
  border: 1px solid #e5e7eb;
  border-radius: 0.5rem;
  padding: 1.5rem;
  margin-bottom: 1rem;
}

.product-info h3 {
  font-size: 1.125rem;
  font-weight: 600;
  color: #1f2937;
  margin-bottom: 0.5rem;
}

.bank-name {
  color: #6b7280;
  margin-bottom: 1rem;
}

.product-actions {
  display: flex;
  gap: 1rem;
}

.detail-btn, .unsubscribe-btn {
  padding: 0.5rem 1rem;
  border-radius: 0.375rem;
  font-size: 0.875rem;
  cursor: pointer;
}

.detail-btn {
  background-color: #f3f4f6;
  color: #374151;
  border: 1px solid #d1d5db;
}

.unsubscribe-btn {
  background-color: #fee2e2;
  color: #ef4444;
  border: 1px solid #fecaca;
}

/* 빈 상태 스타일링 */
.empty-state {
  text-align: center;
  padding: 3rem 0;
  color: #6b7280;
}

.empty-icon {
  font-size: 2.5rem;
  margin-bottom: 1rem;
}

/* 경고 카드 스타일링 */
.warning {
  border: 1px solid #fee2e2;
  background-color: #fef2f2;
}

.warning-icon {
  font-size: 2rem;
  text-align: center;
  margin-bottom: 1rem;
}

/* 좋아요한 게시글 스타일링 */
.liked-article {
  padding: 1rem 0;
  border-bottom: 1px solid #e5e7eb;
}

.article-link {
  text-decoration: none;
  color: inherit;
  display: block;
}

.article-link h3 {
  font-size: 1.125rem;
  font-weight: 600;
  color: #1f2937;
  margin-bottom: 0.5rem;
}

.article-excerpt {
  color: #6b7280;
  margin-bottom: 0.5rem;
}

.article-meta {
  display: flex;
  gap: 1rem;
  font-size: 0.875rem;
  color: #9ca3af;
}

.user-avatar {
  width: 80px;
  height: 80px;
  background-color: #10b981;
  color: white;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 2rem;
  margin: 0 auto 1rem;
  overflow: hidden;
}

.avatar-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.profile-image-section {
  display: flex;
  align-items: center;
  gap: 2rem;
  margin-bottom: 2rem;
  padding-bottom: 2rem;
  border-bottom: 1px solid #e5e7eb;
}

.current-image {
  width: 120px;
  height: 120px;
  border-radius: 50%;
  overflow: hidden;
  background-color: #10b981;
  display: flex;
  align-items: center;
  justify-content: center;
}

.profile-preview {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.profile-placeholder {
  color: white;
  font-size: 3rem;
}

.image-upload {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.upload-btn {
  background-color: #10b981;
  color: white;
  padding: 0.5rem 1rem;
  border-radius: 0.5rem;
  border: none;
  cursor: pointer;
  transition: background-color 0.2s;
}

.upload-btn:hover {
  background-color: #059669;
}

.remove-btn {
  background-color: #f16262;
  color: white;
  padding: 0.5rem 1rem;
  border-radius: 0.5rem;
  border: none;
  cursor: pointer;
  transition: background-color 0.2s;
}

.remove-btn:hover {
  background-color: #e15151;
}

.select-wrapper {
  position: relative;
  display: flex;
  align-items: center;
}

.select-icon {
  position: absolute;
  left: 1rem;
  font-size: 1.25rem;
  pointer-events: none;
}

.form-select {
  width: 100%;
  padding: 0.75rem 1rem 0.75rem 3rem;
  border: 1px solid #d1d5db;
  border-radius: 0.5rem;
  appearance: none;
  background-color: white;
  font-size: 1rem;
  line-height: 1.5;
  color: #374151;
  transition: border-color 0.2s, box-shadow 0.2s;
}

.form-select:focus {
  outline: none;
  border-color: #10b981;
  box-shadow: 0 0 0 2px rgba(16, 185, 129, 0.1);
}

/* 셀렉트 박스의 화살표 커스터마이징 */
.form-select {
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' fill='none' viewBox='0 0 20 20'%3E%3Cpath stroke='%236B7280' stroke-linecap='round' stroke-linejoin='round' stroke-width='1.5' d='M6 8l4 4 4-4'/%3E%3C/svg%3E");
  background-position: right 0.5rem center;
  background-repeat: no-repeat;
  background-size: 1.5em 1.5em;
  padding-right: 2.5rem;
}

.form-select option {
  padding: 0.5rem;
}
</style>