import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import SignUpView from '@/views/SignUpView.vue'
import SignInView from '@/views/SignInView.vue'
import HomeView from '@/views/HomeView.vue'
import LocationView from '@/views/LocationView.vue'
import InterestRateView from '@/views/InterestRateView.vue'
import ExchangeRateView from '@/views/ExchangeRateView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView
    },
    {
      path: '/signup',
      name: 'signUp',
      component: SignUpView
    },
    {
      path: '/signin',
      name: 'signIn',
      component: SignInView
    },
    {
      path: '/location',
      name: 'location',
      component: LocationView
    },
    {
      path: '/interest_rate',
      name: 'interestRate',
      component: InterestRateView
    },
    {
      path: '/exchage_rate',
      name: 'exchangeRate',
      component: ExchangeRateView
    },
  ]
})

router.beforeEach((to, from) => {
  const store = useAuthStore()
  if ((to.name === 'signUp' || to.name === 'signIn') && (store.isLogin)) {
    window.alert('이미 로그인이 되어 있습니다.')
    return { name: 'home' }
  }
})
export default router