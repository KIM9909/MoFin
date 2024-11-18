import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import SignUpView from '@/views/SignUpView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/signup',
      name: 'signUp',
      component: SignUpView
    },

  ]
})

// router.beforeEach((to, from) => {
//   const store = useAuthStore()
//   if (to.name === 'home' && !store.isLogin) {
//     window.alert('로그인이 필요합니다.')
//     return { name: 'signIn'}
//   }
//   if ((to.name === 'signUp' || to.name === 'signIn') && (store.isLogin)) {
//     window.alert('이미 로그인이 되어 있습니다.')
//     return { name: 'home' }
//   }
// })
export default router