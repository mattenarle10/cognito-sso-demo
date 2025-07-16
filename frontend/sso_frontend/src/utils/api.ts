import axios from 'axios'
import { API_CONFIG } from './constants'

// create axios instance
export const apiClient = axios.create({
  baseURL: API_CONFIG.ssoBaseUrl,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json'
  }
})

// request interceptor
apiClient.interceptors.request.use(
  (config) => {
    // add auth header if available
    const token = localStorage.getItem('id_token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => Promise.reject(error)
)

// response interceptor
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    console.error('api error:', error.response?.data || error.message)
    return Promise.reject(error)
  }
) 