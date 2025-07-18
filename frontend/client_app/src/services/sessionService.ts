import axios from 'axios'

// Constants for API configuration from environment variables
const SSO_API_URL = import.meta.env.VITE_SSO_API_URL

interface TokenResponse {
  id_token: string
  access_token: string
  refresh_token?: string
}

export class SessionService {
  /**
   * Get tokens using a session_id from the SSO backend
   * 
   * @param sessionId - The session ID received from SSO frontend redirect
   * @returns TokenResponse containing tokens or null if retrieval fails
   */
  async getSession(sessionId: string): Promise<TokenResponse | null> {
    try {
      const response = await axios.get(`${SSO_API_URL}/get-session`, {
        params: { session_id: sessionId }
      })
      
      if (response.data && response.data.data) {
        console.log('Session data received:', response.data.data)
        
        // Extract tokens from the response structure
        const { tokens } = response.data.data
        
        if (tokens && tokens.id_token && tokens.access_token) {
          return {
            id_token: tokens.id_token,
            access_token: tokens.access_token,
            refresh_token: tokens.refresh_token
          }
        }
      }
      
      console.error('Invalid response format from SSO API')
      return null
    } catch (error) {
      console.error('Failed to get session:', error)
      return null
    }
  }
  
  /**
   * Check if the current tokens are valid (not expired)
   * This is a simple check based on localStorage presence
   * In a production app, you would verify the expiration time
   */
  hasValidTokens(): boolean {
    return !!localStorage.getItem('id_token')
  }
}

// Create and export a singleton instance
export const sessionService = new SessionService()
