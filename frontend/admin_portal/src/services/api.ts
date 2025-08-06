import axios from 'axios'
import { useToast } from 'vue-toastification'

const API_URL = import.meta.env.VITE_ADMIN_API_URL || 'https://api.example.com/admin'
const toast = useToast()

// Create axios instance with auth header
const apiClient = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json'
  }
})

// Add token to requests
apiClient.interceptors.request.use(config => {
  const token = localStorage.getItem('id_token')
  console.log('API Request - Token from localStorage:', token ? 'Token exists' : 'No token found')
  
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
    console.log('API Request - Authorization header set')
  } else {
    console.warn('API Request - No token available for request to:', config.url)
    toast.error('Authentication error: No token available')
  }
  
  return config
})

// Add response interceptor for error handling
apiClient.interceptors.response.use(
  response => response,
  error => {
    // Handle common errors
    if (error.response) {
      // Server responded with a status code outside of 2xx range
      const status = error.response.status
      const message = error.response.data?.message || 'An error occurred'
      
      if (status === 401) {
        toast.error('Authentication error: Please log in again')
      } else if (status === 403) {
        toast.error('Permission denied: You do not have access to this resource')
      }
    } else if (error.request) {
      // Request was made but no response received
      toast.error('Network error: Unable to connect to server')
    } else {
      // Something happened in setting up the request
      toast.error('Request error: ' + error.message)
    }
    
    return Promise.reject(error)
  }
)

export const api = {
  // User management
  async getUsers(params = {}) {
    try {
      const response = await apiClient.get('/admin/users', { params })
      return response.data
    } catch (error) {
      console.error('Error fetching users:', error)
      throw error
    }
  },

  async getUserDetails(userId: string) {
    try {
      const response = await apiClient.get(`/admin/users/${userId}`)
      return response.data
    } catch (error) {
      console.error(`Error fetching user ${userId}:`, error)
      throw error
    }
  },

  async disableUser(userId: string) {
    try {
      // Adding confirm: true parameter required by the backend
      const response = await apiClient.post(`/admin/users/${userId}/deactivate`, {
        confirm: true,
        action: 'deactivate'
      })
      toast.success('User disabled successfully')
      return response.data
    } catch (error: any) {
      console.error(`Error disabling user ${userId}:`, error)
      toast.error(`Failed to disable user: ${error.response?.data?.message || 'Unknown error'}`)
      throw error
    }
  },

  async enableUser(userId: string) {
    try {
      // Using the same endpoint as disable but with action=activate
      const response = await apiClient.post(`/admin/users/${userId}/deactivate`, {
        confirm: true,
        action: 'activate'
      })
      toast.success('User enabled successfully')
      return response.data
    } catch (error: any) {
      console.error(`Error enabling user ${userId}:`, error)
      toast.error(`Failed to enable user: ${error.response?.data?.message || 'Unknown error'}`)
      throw error
    }
  },

  async resetPassword(userId: string) {
    try {
      // Using the force_password_reset endpoint with confirm: true parameter
      const response = await apiClient.post(`/admin/users/${userId}/password-reset`, {
        confirm: true
      })
      toast.success('Password reset initiated successfully. User will receive an email with a verification code and will be directed straight to the reset password page on their next login.')
      return response.data
    } catch (error: any) {
      console.error(`Error resetting password for user ${userId}:`, error)
      const errorMsg = error.response?.data?.message || 'Unknown error';
      toast.error(`Failed to reset password: ${errorMsg}`)
      throw error
    }
  },

  async deleteUser(userId: string) {
    try {
      // Adding confirm: true parameter required by the backend for user deletion
      const response = await apiClient.delete(`/admin/users/${userId}`, {
        data: { confirm: true }
      })
      toast.success('User deleted successfully')
      return response.data
    } catch (error: any) {
      console.error(`Error deleting user ${userId}:`, error)
      toast.error(`Failed to delete user: ${error.response?.data?.message || 'Unknown error'}`)
      throw error
    }
  },
  
  async updateUser(userId: string, attributes: Record<string, string>) {
    try {
      const response = await apiClient.patch(`/admin/users/${userId}`, {
        attributes
      })
      toast.success('User information updated successfully')
      return response.data
    } catch (error: any) {
      console.error(`Error updating user ${userId}:`, error)
      toast.error(`Failed to update user: ${error.response?.data?.message || 'Unknown error'}`)
      throw error
    }
  }
}
