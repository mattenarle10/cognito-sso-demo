import { ref } from 'vue'
import { apiClient } from '../utils/api'
import { API_CONFIG } from '../utils/constants'
import type { AppValidationResponse, UserAuthResponse, SessionResponse, TokenResponse } from '../types/api'

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
      const response = await apiClient.get(API_CONFIG.endpoints.checkAppUser, {
        params: { application_id: applicationId },
        headers: { Authorization: `Bearer ${idToken}` }
      })
      return response.data.data
    } catch (err: any) {
      error.value = err.response?.data?.message || 'authorization check failed'
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
      return response.data.data
    } catch (err: any) {
      error.value = err.response?.data?.message || 'failed to get session'
      return null
    } finally {
      loading.value = false
    }
  }

  // authorize application with granted scopes
  const authorizeApplication = async (data: {
    application_id: string
    granted_scopes: string[]
    action: 'approve' | 'deny'
  }): Promise<{ status: string; scopes_granted?: string[] } | null> => {
    loading.value = true
    error.value = null
    
    try {
      const idToken = localStorage.getItem('id_token')
      if (!idToken) {
        throw new Error('no authentication token found')
      }

      const response = await apiClient.post('/authorize-application', data, {
        headers: { Authorization: `Bearer ${idToken}` }
      })
      return response.data.data
    } catch (err: any) {
      error.value = err.response?.data?.message || 'authorization failed'
      return null
    } finally {
      loading.value = false
    }
  }

  return {
    loading,
    error,
    validateAppChannel,
    checkAppUser,
    initSession,
    getSession,
    authorizeApplication
  }
} 