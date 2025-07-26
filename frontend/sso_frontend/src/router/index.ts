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
    {
      path: '/authorizations',
      name: 'authorizations',
      component: () => import('@/pages/AuthorizationsPage.vue')
    },
    {
      path: '/manage-account',
      name: 'manage-account',
      component: () => import('@/pages/ManageAccountPage.vue')
    },
    {
      path: '/sessions',
      name: 'sessions',
      component: () => import('../pages/SessionsPage.vue')
    },
    {
      path: '/auth/callback',
      name: 'AuthCallback',
      component: () => import('../pages/AuthCallback.vue'),
    },
    {
      path: '/complete-profile',
      name: 'CompleteProfile',
      component: () => import('@/pages/CompleteProfilePage.vue'),
    },
    {
      path: '/mfa-verify',
      name: 'mfa-verify',
      component: () => import('@/pages/MfaVerifyPage.vue'),
    },
    {
      path: '/phone-otp',
      name: 'phone-otp',
      component: () => import('@/pages/PhoneOtpPage.vue'),
    }
  ],
})

// Add default query parameters for development mode
router.beforeEach((to, from, next) => {
  // Only apply this to login and register routes
  if ((to.name === 'login' || to.name === 'register') && import.meta.env.DEV) {
    // Check if the URL already has the required parameters
    const hasAppName = to.query.application_name !== undefined
    const hasChannelId = to.query.channel_id !== undefined
    const hasRedirectUrl = to.query.redirect_url !== undefined
    
    // If any parameter is missing, add all default parameters
    if (!hasAppName || !hasChannelId || !hasRedirectUrl) {
      next({
        name: to.name,
        query: {
          ...to.query,
          application_name: import.meta.env.VITE_DEFAULT_APPLICATION_NAME,
          channel_id: import.meta.env.VITE_DEFAULT_CHANNEL_ID,
          redirect_url: import.meta.env.VITE_DEFAULT_REDIRECT_URL
        }
      })
      return
    }
  }
  
  next()
})

export default router
