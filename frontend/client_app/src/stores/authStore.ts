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
        // User info loaded from stored token
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
    session_id?: string
  }) {
    tokens.value = sessionTokens
    
    // Store tokens in localStorage
    localStorage.setItem('id_token', sessionTokens.id_token)
    localStorage.setItem('access_token', sessionTokens.access_token)
    if (sessionTokens.refresh_token) {
      localStorage.setItem('refresh_token', sessionTokens.refresh_token)
    }
    
    // Store session ID if available
    if (sessionTokens.session_id) {
      localStorage.setItem('session_id', sessionTokens.session_id)
    } else {
      // Try to extract session ID from URL if not provided in tokens
      const urlParams = new URLSearchParams(window.location.search)
      const sessionId = urlParams.get('session_id')
      if (sessionId) {
        localStorage.setItem('session_id', sessionId)
      }
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
      // User info extracted from token
    } catch (error) {
      console.error('Failed to parse JWT token:', error)
    }
    
    isAuthenticated.value = true
  }
  
  // Clear auth state on logout
  async function logout() {
    try {
      // First, revoke the session on the backend if we have tokens
      if (tokens.value?.id_token) {
        // Get the current session ID
        const sessionId = localStorage.getItem('session_id')
        
        if (sessionId) {
          // Call the SSO backend to revoke the session
          // Using the correct endpoint format that works in the SSO frontend
          const response = await fetch(`${import.meta.env.VITE_SSO_API_URL}/user-sessions/${sessionId}`, {
            method: 'DELETE',
            headers: {
              'Authorization': `Bearer ${tokens.value.id_token}`
            }
          })
          
          if (!response.ok) {
            console.warn('Session revocation API returned an error:', await response.text())
          } else {
            console.log('Session successfully revoked on the backend')
          }
        } else {
          console.warn('No session_id found in localStorage, skipping backend revocation')
        }
      }
    } catch (error) {
      console.error('Error revoking session:', error)
      // Continue with local logout even if the API call fails
    } finally {
      // Clear local state
      tokens.value = null
      user.value = null
      isAuthenticated.value = false
      
      // Remove from localStorage
      localStorage.removeItem('id_token')
      localStorage.removeItem('access_token')
      localStorage.removeItem('refresh_token')
      localStorage.removeItem('session_id')
      
      // Redirect to home page with signedout parameter
      window.location.href = '/?signedout=true'
    }
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
