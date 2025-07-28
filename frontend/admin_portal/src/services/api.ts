import axios from 'axios'

const API_URL = import.meta.env.VITE_ADMIN_API_URL || 'https://api.example.com/admin'

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
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

export const api = {
  // User management
  async getUsers(params = {}) {
    try {
      const response = await apiClient.get('/users', { params })
      return response.data
    } catch (error) {
      console.error('Error fetching users:', error)
      throw error
    }
  },

  async getUserDetails(userId: string) {
    try {
      const response = await apiClient.get(`/users/${userId}`)
      return response.data
    } catch (error) {
      console.error(`Error fetching user ${userId}:`, error)
      throw error
    }
  },

  async disableUser(userId: string) {
    try {
      const response = await apiClient.post(`/users/${userId}/deactivate`)
      return response.data
    } catch (error) {
      console.error(`Error disabling user ${userId}:`, error)
      throw error
    }
  },

  async enableUser(userId: string) {
    try {
      const response = await apiClient.post(`/users/${userId}/activate`)
      return response.data
    } catch (error) {
      console.error(`Error enabling user ${userId}:`, error)
      throw error
    }
  },

  async resetPassword(userId: string) {
    try {
      const response = await apiClient.post(`/users/${userId}/reset-password`)
      return response.data
    } catch (error) {
      console.error(`Error resetting password for user ${userId}:`, error)
      throw error
    }
  },

  async deleteUser(userId: string) {
    try {
      const response = await apiClient.delete(`/users/${userId}`)
      return response.data
    } catch (error) {
      console.error(`Error deleting user ${userId}:`, error)
      throw error
    }
  }
}
