import { defineStore } from 'pinia'
import { ref } from 'vue'

// Define user type
interface User {
  sub: string
  email: string
  name?: string
}

export const useAuthStore = defineStore('auth', () => {
  // State
  const isAuthenticated = ref(false)
  const user = ref<User | null>(null)
  const tokens = ref<{
    id_token: string
    access_token: string
    refresh_token?: string
  } | null>(null)
  
  // Initialize from localStorage on app start
  function initialize() {
    const storedIdToken = localStorage.getItem('id_token')
    const storedAccessToken = localStorage.getItem('access_token')
    const storedRefreshToken = localStorage.getItem('refresh_token')
    
    if (storedIdToken && storedAccessToken) {
      tokens.value = {
        id_token: storedIdToken,
        access_token: storedAccessToken,
        refresh_token: storedRefreshToken || undefined
      }
      isAuthenticated.value = true
      
      // Could decode JWT to get user info
      // For now we'll just set basic authenticated state
    }
  }
  
  // Set tokens after successful authentication
  function setTokens(sessionTokens: {
    id_token: string
    access_token: string
    refresh_token?: string
  }) {
    tokens.value = sessionTokens
    
    // Store tokens in localStorage
    localStorage.setItem('id_token', sessionTokens.id_token)
    localStorage.setItem('access_token', sessionTokens.access_token)
    if (sessionTokens.refresh_token) {
      localStorage.setItem('refresh_token', sessionTokens.refresh_token)
    }
    
    isAuthenticated.value = true
  }
  
  // Clear auth state on logout
  function logout() {
    tokens.value = null
    user.value = null
    isAuthenticated.value = false
    
    // Remove from localStorage
    localStorage.removeItem('id_token')
    localStorage.removeItem('access_token')
    localStorage.removeItem('refresh_token')
  }
  
  return {
    isAuthenticated,
    user,
    tokens,
    initialize,
    setTokens,
    logout
  }
})
