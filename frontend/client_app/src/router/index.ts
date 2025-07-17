import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '../stores/authStore'
import { sessionService } from '../services/sessionService'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: () => import('../pages/HomePage.vue')
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
  
  // Handle session_id parameter from SSO frontend redirect
  const sessionId = to.query.session_id as string
  if (sessionId) {
    try {
      // Get tokens from SSO backend using session_id
      const tokens = await sessionService.getSession(sessionId)
      if (tokens) {
        // Store tokens in auth store
        authStore.setTokens(tokens)
        
        // Remove session_id from URL for security
        const { query } = to
        delete query.session_id
        return next({ path: to.path, query })
      }
    } catch (error) {
      console.error('Failed to process session:', error)
    }
  }
  
  // Check if route requires authentication
  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    return next({ name: 'home' })
  }
  
  return next()
})

export default router
