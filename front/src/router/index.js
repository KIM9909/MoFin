import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import SignUpView from '@/views/SignUpView.vue'
import SignInView from '@/views/SignInView.vue'
import HomeView from '@/views/HomeView.vue'
import LocationView from '@/views/LocationView.vue'
import ExchangeRateView from '@/views/ExchangeRateView.vue'
import SavingsView from '@/views/SavingsView.vue'
import ProductView from '@/views/ProductView.vue'
import DepositView from '@/views/DepositView.vue'

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
      path: '/deposit',
      name: 'deposit',
      component: DepositView
    },
    {
      path: '/exchange_rate',
      name: 'exchangeRate',
      component: ExchangeRateView
    },
    {
      path: '/savings',
      name: 'savings',
      component: SavingsView
    },
    {
      path: '/products',
      name: 'products',
      component: ProductView
    }
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