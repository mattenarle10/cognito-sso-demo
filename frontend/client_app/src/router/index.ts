import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '../stores/authStore'
import { sessionService } from '../services/sessionService'
import { useToast } from 'vue-toastification'

// Authentication utility function for redirecting to login
export function redirectToLogin() {
  const ssoUrl = import.meta.env.VITE_SSO_FRONTEND_URL
  const appName = import.meta.env.VITE_APPLICATION_NAME
  const channelId = import.meta.env.VITE_CHANNEL_ID
  
  if (ssoUrl && appName && channelId) {
    const redirectUrl = `${ssoUrl}/login?application=${appName}&channel=${channelId}`
    window.location.href = redirectUrl
  } else {
    console.error('Missing environment variables for SSO redirect')
  }
}

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: () => import('../pages/HomePage.vue')
    },
    {
      path: '/profile',
      name: 'profile',
      component: () => import('../pages/ProfilePage.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/orders',
      name: 'orders',
      component: () => import('../pages/OrdersPage.vue'),
      meta: { requiresAuth: true }
    }
  ]
})

// Navigation guard to protect authenticated routes
router.beforeEach(async (to, _from, next) => {
  const authStore = useAuthStore()
  const toast = useToast()
  
  // Handle session_id parameter from SSO frontend redirect
  const sessionId = to.query.session_id as string
  if (sessionId) {
    try {
      // Get tokens from SSO backend using session_id
      const tokens = await sessionService.getSession(sessionId)
      if (tokens) {
        // Store tokens in auth store
        authStore.setTokens(tokens)
        
        // Show success toast notification
        toast.success(`Welcome to The Grind, ${authStore.user?.given_name || authStore.user?.name?.split(' ')[0] || 'User'}!`)
        
        // Remove session_id from URL for security
        const { query } = to
        delete query.session_id
        return next({ path: to.path, query })
      }
    } catch (error) {
      console.error('Failed to process session:', error)
      toast.error('Authentication failed. Please try logging in again.')
    }
  }
  
  // Check for sign-out parameter
  if (to.query.signedout === 'true') {
    toast.info('You have been signed out. Come back for another brew soon!')
    // Remove signedout parameter from URL
    const { query } = to
    delete query.signedout
    return next({ path: to.path, query })
  }
  
  // Check if route requires authentication
  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    return next({ name: 'home' })
  }
  
  return next()
})

export default router
