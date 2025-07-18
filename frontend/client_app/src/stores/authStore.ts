import { defineStore } from 'pinia'
import { ref } from 'vue'

// Helper function to parse JWT tokens
function parseJwt(token: string) {
  try {
    // Split the token and get the payload part (second part)
    const base64Url = token.split('.')[1];
    // Replace characters for correct base64 decoding
    const base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
    // Decode and parse as JSON
    const jsonPayload = decodeURIComponent(atob(base64).split('').map(function(c) {
      return '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2);
    }).join(''));

    const parsed = JSON.parse(jsonPayload);
    console.log('Parsed JWT payload:', parsed);
    return parsed;
  } catch (e) {
    console.error('Error parsing JWT token:', e);
    return {};
  }
}

// Define user type
interface User {
  sub: string
  email: string
  name?: string
  given_name?: string
  family_name?: string
  phone_number?: string
  gender?: string
  email_verified?: boolean
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
      
      // Decode JWT to get user info
      try {
        const payload = parseJwt(storedIdToken)
        user.value = {
          sub: payload.sub,
          email: payload.email,
          name: payload.name,
          given_name: payload.given_name,
          family_name: payload.family_name,
          phone_number: payload.phone_number,
          gender: payload.gender,
          email_verified: payload.email_verified
        }
        console.log('User info loaded from stored token:', user.value)
      } catch (error) {
        console.error('Failed to parse stored JWT token:', error)
      }
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
    
    // Parse the JWT token to get user information
    try {
      const payload = parseJwt(sessionTokens.id_token)
      user.value = {
        sub: payload.sub,
        email: payload.email,
        name: payload.name,
        given_name: payload.given_name,
        family_name: payload.family_name,
        phone_number: payload.phone_number,
        gender: payload.gender,
        email_verified: payload.email_verified
      }
      console.log('User info extracted from token:', user.value)
    } catch (error) {
      console.error('Failed to parse JWT token:', error)
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
    
    // Redirect to home page with signedout parameter
    window.location.href = '/?signedout=true'
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
