import { ref } from 'vue'
import axios from 'axios'

// Backend API URLs from environment variables
const ssoApiUrl = import.meta.env.VITE_SSO_API_URL || 'https://17xe662baj.execute-api.ap-southeast-2.amazonaws.com'

/**
 * Parse a JWT token
 * @param token JWT token string
 * @returns Parsed token payload or null if invalid
 */
function parseJwt(token: string): any {
  try {
    const base64Url = token.split('.')[1]
    const base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/')
    const jsonPayload = decodeURIComponent(
      atob(base64)
        .split('')
        .map(c => '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2))
        .join('')
    )
    return JSON.parse(jsonPayload)
  } catch (error) {
    console.error('Error parsing JWT token:', error)
    return null
  }
}

/**
 * Check if a JWT token has expired
 * @param token JWT token string
 * @returns Boolean indicating if the token has expired
 */
function isTokenExpired(token: string): boolean {
  const decoded = parseJwt(token)
  if (!decoded) return true

  const currentTime = Date.now() / 1000
  return decoded.exp < currentTime
}

/**
 * Composable for handling authentication in the admin portal
 */
export function useAuth() {
  const isAuthenticated = ref(false)
  const userData = ref<any>(null)

  /**
   * Get session ID from URL or localStorage
   */
  const getSessionId = (): string | null => {
    // First check URL parameters
    const urlParams = new URLSearchParams(window.location.search)
    const sessionId = urlParams.get('session_id')
    
    // If found in URL, save to localStorage for future use and return it
    if (sessionId) {
      console.log('Found session_id in URL:', sessionId)
      localStorage.setItem('admin_session_id', sessionId)
      // Clean up URL by removing the session_id parameter
      if (window.history && window.history.replaceState) {
        const cleanUrl = window.location.pathname
        window.history.replaceState({}, document.title, cleanUrl)
      }
      return sessionId
    }
    
    // If not in URL, check localStorage
    const storedSessionId = localStorage.getItem('admin_session_id')
    if (storedSessionId) {
      console.log('Using session_id from localStorage')
      return storedSessionId
    }
    
    console.log('No session_id found in URL or localStorage')
    return null
  }

  /**
   * Verify if the current user is an admin by checking the session
   * @returns Promise<boolean> indicating if user is admin
   */
  const verifyAdmin = async (): Promise<boolean> => {
    try {
      const sessionId = getSessionId()
      
      if (!sessionId) {
        console.log('No session ID found')
        return false
      }
      
      console.log('Verifying admin session with ID:', sessionId)
      console.log(`Calling ${ssoApiUrl}/get-session with session_id=${sessionId}`)
      
      // Using axios instead of fetch to handle CORS better
      const response = await axios.get(`${ssoApiUrl}/get-session`, {
        params: { session_id: sessionId },
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json'
        }
      })
      
      // Axios puts the parsed JSON directly in response.data
      const responseData = response.data
      console.log('Response data:', responseData)
      
      // The API returns nested data structure: { data: { tokens, user, application_id } }
      if (!responseData || !responseData.data) {
        console.error('Invalid response format from SSO API')
        return false
      }
      
      const sessionData = responseData.data
      console.log('Session data extracted:', sessionData)
      
      // Store tokens in localStorage for future use
      if (sessionData.tokens && sessionData.tokens.id_token) {
        localStorage.setItem('id_token', sessionData.tokens.id_token)
        console.log('Stored ID token in localStorage')
      }
      
      // Store user data from session
      userData.value = sessionData.user || {}
      console.log('User data:', userData.value)
      
      // Check if this session is for the admin-portal application
      const isAdminApp = sessionData.application_id === 'admin-portal'
      isAuthenticated.value = isAdminApp
      
      console.log(`User admin status: ${isAdminApp}`)
      return isAdminApp
    } catch (error) {
      console.error('Error verifying admin status:', error)
      return false
    }
  }
  
  /**
   * Get the username from user data
   * @returns Promise<string> with the username
   */
  const getUsername = async (): Promise<string> => {
    // If we already have user data from the session verification
    if (userData.value && userData.value.name) {
      return userData.value.name
    }
    
    // If no user data yet but we're authenticated, try to get the session again
    if (isAuthenticated.value) {
      await verifyAdmin() // This will populate userData
      return userData.value?.name || 'Admin User'
    }
    
    return ''
  }
  
  /**
   * Logout the user by clearing session storage and redirecting
   */
  const logout = (): void => {
    // Clear all stored session data
    localStorage.removeItem('admin_session_id')
    localStorage.removeItem('id_token') // Remove any legacy tokens too
    
    // Reset state
    isAuthenticated.value = false
    userData.value = null
  }
  
  return {
    isAuthenticated,
    userData,
    verifyAdmin,
    getUsername,
    logout,
    getSessionId
  }
}
