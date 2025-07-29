import { ref } from 'vue'
import { apiClient } from '../utils/api'
import { API_CONFIG } from '../utils/constants'
import type { AppValidationResponse, UserAuthResponse, SessionResponse, TokenResponse, UserSession } from '../types/api'
import type { CognitoTokens } from '../services/cognitoService'

export function useApi() {
  const loading = ref(false)
  const error = ref<string | null>(null)

  // validate application and channel combination
  const validateAppChannel = async (applicationId: string, channelId: string): Promise<AppValidationResponse | null> => {
    loading.value = true
    error.value = null
    
    try {
      const response = await apiClient.get(API_CONFIG.endpoints.validateAppChannel, {
        params: { application_id: applicationId, channel_id: channelId }
      })
      return response.data.data
    } catch (err: any) {
      error.value = err.response?.data?.message || 'validation failed'
      return null
    } finally {
      loading.value = false
    }
  }

  // check if user is authorized for application
  const checkAppUser = async (idToken: string, applicationId: string): Promise<UserAuthResponse | null> => {
    loading.value = true
    error.value = null
    
    try {
      // Use token from parameter or fallback to localStorage
      // This ensures we always use the most recent token
      const token = idToken || localStorage.getItem('id_token')
      
      if (!token) {
        throw new Error('No authentication token available')
      }
      
      // Check if user has authorized the application
      const response = await apiClient.get(API_CONFIG.endpoints.checkAppUser, {
        params: { application_id: applicationId },
        headers: { Authorization: `Bearer ${token}` }
      })
      return response.data.data
    } catch (err: any) {
      // For first-time users, a 404 is expected (not authorized yet)
      // This will trigger the consent screen
      if (err.response?.status === 404) {
        return null
      }
      
      // For token expiration, provide a clear error message
      if (err.response?.status === 401 && 
          err.response?.data?.error_code === 'INVALID_TOKEN') {
        error.value = 'Your session has expired. Please log in again.'
        return null
      }
      
      error.value = err.response?.data?.message || 'Failed to check app user'
      return null
    } finally {
      loading.value = false
    }
  }

  // initialize session with cognito tokens
  const initSession = async (tokens: any, applicationId: string): Promise<SessionResponse | null> => {
    loading.value = true
    error.value = null
    
    try {
      const response = await apiClient.post(API_CONFIG.endpoints.initSession, {
        tokens,
        application_id: applicationId
      })
      return response.data.data
    } catch (err: any) {
      error.value = err.response?.data?.message || 'session initialization failed'
      return null
    } finally {
      loading.value = false
    }
  }

  // get session tokens by session_id
  const getSession = async (sessionId: string): Promise<TokenResponse | null> => {
    loading.value = true
    error.value = null
    
    try {
      const response = await apiClient.get(API_CONFIG.endpoints.getSession, {
        params: { session_id: sessionId }
      })
      
      // If successful, store tokens in localStorage
      const data = response.data.data;
      if (data && data.tokens) {
        if (data.tokens.id_token) {
          localStorage.setItem('id_token', data.tokens.id_token);
        }
        if (data.tokens.access_token) {
          localStorage.setItem('access_token', data.tokens.access_token);
        }
        if (data.tokens.refresh_token) {
          localStorage.setItem('refresh_token', data.tokens.refresh_token);
        }
      }
      
      return response.data.data
    } catch (err: any) {
      error.value = err.response?.data?.message || 'failed to get session'
      return null
    } finally {
      loading.value = false
    }
  }
  
  // refresh tokens using session_id
  const refreshTokens = async (): Promise<TokenResponse | null> => {
    // Get session_id from URL query parameter or localStorage
    const urlParams = new URLSearchParams(window.location.search);
    const sessionId = urlParams.get('session_id') || localStorage.getItem('session_id');
    
    if (!sessionId) {
      console.log('No session ID available for token refresh');
      return null;
    }
    
    return await getSession(sessionId);
  }

  // authorize application with granted scopes
  const authorizeApplication = async (
    data: {
      application_id: string
      granted_scopes: string[]
      action: 'approve' | 'deny'
    },
    idToken?: string
  ): Promise<{ status: string; scopes_granted?: string[] } | null> => {
    loading.value = true
    error.value = null
    
    try {
      // Use token from parameter or fallback to localStorage
      // This ensures we always use the most recent token
      const token = idToken || localStorage.getItem('id_token')
      
      if (!token) {
        throw new Error('No ID token available')
      }
      
      console.log('Authorizing application with token')
      const response = await apiClient.post(
        API_CONFIG.endpoints.authorizeApplication,
        data,
        {
          headers: { Authorization: `Bearer ${token}` }
        }
      )
      
      return response.data.data
    } catch (err: any) {
      // For token expiration, provide a clear error message
      if (err.response?.status === 401 && 
          err.response?.data?.error_code === 'INVALID_TOKEN') {
        console.error('Token expired during application authorization')
        error.value = 'Your session has expired. Please log in again.'
      } else {
        error.value = err.response?.data?.message || 'Failed to authorize application'
      }
      return null
    } finally {
      loading.value = false
    }
  }

  // get user's authorized applications
  const getUserAuthorizations = async (idToken?: string): Promise<{ authorizations: any[]; total_count: number } | null> => {
    loading.value = true
    error.value = null
    
    try {
      const token = idToken || localStorage.getItem('id_token') || localStorage.getItem('temp_id_token')
      if (!token) {
        throw new Error('no authentication token found')
      }

      const response = await apiClient.get('/user-authorizations', {
        headers: { Authorization: `Bearer ${token}` }
      })
      return response.data.data
    } catch (err: any) {
      error.value = err.response?.data?.message || 'failed to get authorizations'
      return null
    } finally {
      loading.value = false
    }
  }

  // revoke authorization for specific application
  const revokeAuthorization = async (applicationId: string, idToken?: string): Promise<boolean> => {
    loading.value = true
    error.value = null
    
    try {
      const token = idToken || localStorage.getItem('id_token') || localStorage.getItem('temp_id_token')
      if (!token) {
        throw new Error('no authentication token found')
      }

      await apiClient.delete(`/user-authorizations/${applicationId}`, {
        headers: { Authorization: `Bearer ${token}` }
      })
      return true
    } catch (err: any) {
      error.value = err.response?.data?.message || 'failed to revoke authorization'
      return false
    } finally {
      loading.value = false
    }
  }

  // update user profile information
  const updateUserProfile = async (updates: Record<string, any>, tokens: any): Promise<boolean> => {
    loading.value = true
    error.value = null
    
    try {
      if (!tokens?.id_token || !tokens?.access_token) {
        throw new Error('authentication tokens required')
      }

      const response = await apiClient.patch('/user-profile', {
        updates,
        access_token: tokens.access_token
      }, {
        headers: { Authorization: `Bearer ${tokens.id_token}` }
      })
      
      return response.data.success
    } catch (err: any) {
      error.value = err.response?.data?.message || 'failed to update profile'
      return false
    } finally {
      loading.value = false
    }
  }

  // get user's active sessions
  const getUserSessions = async (idToken?: string): Promise<{ sessions: { active: UserSession[], expired: UserSession[] }; summary: { active_count: number, expired_count: number, total_count: number }; user_id: string } | null> => {
    loading.value = true
    error.value = null
    
    try {
      const token = idToken || localStorage.getItem('id_token') || localStorage.getItem('temp_id_token')
      if (!token) {
        throw new Error('no authentication token found')
      }

      const response = await apiClient.get('/user-sessions', {
        headers: { Authorization: `Bearer ${token}` }
      })
      return response.data.data
    } catch (err: any) {
      error.value = err.response?.data?.message || 'failed to get sessions'
      return null
    } finally {
      loading.value = false
    }
  }

  // revoke a user session
  const revokeUserSession = async (sessionId: string, idToken?: string): Promise<boolean> => {
    loading.value = true
    error.value = null
    
    try {
      const token = idToken || localStorage.getItem('id_token') || localStorage.getItem('temp_id_token')
      if (!token) {
        throw new Error('no authentication token found')
      }

      console.log(`Revoking session: ${sessionId}`)
      const response = await apiClient.delete(`/user-sessions/${sessionId}`, {
        headers: { Authorization: `Bearer ${token}` }
      })
      console.log('Revoke response:', response.data)
      return true
    } catch (err: any) {
      console.error('Error revoking session:', err)
      error.value = err.response?.data?.message || 'failed to revoke session'
      return false
    } finally {
      loading.value = false
    }
  }

  // Note: Token refresh is now handled by the session mechanism via getSession

  // Note: We're using getUserAuthorizations to get application details instead of a separate endpoint

  return {
    loading,
    error,
    validateAppChannel,
    checkAppUser,
    initSession,
    getSession,
    refreshTokens,
    authorizeApplication,
    getUserAuthorizations,
    revokeAuthorization,
    updateUserProfile,
    getUserSessions,
    revokeUserSession
  }
}