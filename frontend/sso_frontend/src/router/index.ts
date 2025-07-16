import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      redirect: '/login'
    },
    {
      path: '/login',
      name: 'login',
      component: () => import('@/pages/LoginPage.vue')
    },
    {
      path: '/register', 
      name: 'register',
      component: () => import('@/pages/RegisterPage.vue')
    },
    {
      path: '/email-otp',
      name: 'email-otp',
      component: () => import('@/pages/EmailOtpPage.vue')
    },
  ],
})

export default router
