<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useAuth } from './composables/useAuth'
import { api } from './services/api'

// User interface
interface User {
  username: string;
  name?: string;
  email: string;
  phone_number?: string;
  status: string;
  created_date: string;
  [key: string]: any;
}

// State
const isLoading = ref(true)
const isAdmin = ref(false)
const userName = ref('')
const users = ref<User[]>([])
const isUserModalOpen = ref(false)
const isConfirmModalOpen = ref(false)
const selectedUser = ref<User | null>(null)
const actionType = ref('')
const errorMessage = ref('')
const successMessage = ref('')

// Auth functions
const { verifyAdmin, getUsername, logout } = useAuth()

// Load data
onMounted(async () => {
  // Verify admin status from token
  try {
    isAdmin.value = await verifyAdmin()
    if (isAdmin.value) {
      userName.value = await getUsername()
      await loadUsers()
    } else {
      // Redirect non-admin users to SSO login
      window.location.href = import.meta.env.VITE_SSO_URL || 'http://localhost:5173'
    }
  } catch (error) {
    console.error('Authentication error:', error)
    errorMessage.value = 'Failed to authenticate. Please try again.'
  } finally {
    isLoading.value = false
  }
})

// Load users from API
async function loadUsers() {
  try {
    const response = await api.getUsers()
    users.value = response.users || []
  } catch (error) {
    console.error('Error loading users:', error)
    errorMessage.value = 'Failed to load users. Please try again.'
  }
}

// User actions
function showUserModal(user: User) {
  selectedUser.value = user
  isUserModalOpen.value = true
}

function showConfirmModal(user: User, action: string) {
  selectedUser.value = user
  actionType.value = action
  isConfirmModalOpen.value = true
}

async function handleConfirmAction() {
  try {
    if (!selectedUser.value) return
    
    const userId = selectedUser.value.username
    
    if (actionType.value === 'disable') {
      await api.disableUser(userId)
      successMessage.value = 'User disabled successfully'
    } else if (actionType.value === 'enable') {
      await api.enableUser(userId)
      successMessage.value = 'User enabled successfully'
    } else if (actionType.value === 'reset') {
      await api.resetPassword(userId)
      successMessage.value = 'Password reset email sent'
    } else if (actionType.value === 'delete') {
      await api.deleteUser(userId)
      successMessage.value = 'User deleted successfully'
    }
    
    // Reload users after action
    await loadUsers()
    isConfirmModalOpen.value = false
    
    // Clear success message after 3 seconds
    setTimeout(() => {
      successMessage.value = ''
    }, 3000)
  } catch (error) {
    console.error(`Error performing ${actionType.value} action:`, error)
    errorMessage.value = `Failed to ${actionType.value} user. Please try again.`
    
    // Clear error message after 3 seconds
    setTimeout(() => {
      errorMessage.value = ''
    }, 3000)
  }
}

function closeUserModal() {
  isUserModalOpen.value = false
  selectedUser.value = null
}

function closeConfirmModal() {
  isConfirmModalOpen.value = false
  selectedUser.value = null
  actionType.value = ''
}

const handleLogout = () => {
  logout()
  window.location.href = import.meta.env.VITE_SSO_URL || 'http://localhost:5173'
}
</script>

<template>
  <div class="admin-app">
    <!-- Loading State -->
    <div v-if="isLoading" class="loading">
      <div class="spinner"></div>
      <p>Verifying admin credentials...</p>
    </div>
    
    <!-- Admin Dashboard -->
    <div v-else-if="isAdmin" class="admin-dashboard">
      <!-- Header -->
      <header class="admin-header">
        <h1>Admin Portal</h1>
        <div class="user-menu">
          <span class="user-name">{{ userName }}</span>
          <button @click="handleLogout" class="btn-logout">Logout</button>
        </div>
      </header>
      
      <!-- Alert Messages -->
      <div v-if="errorMessage" class="alert alert-error">
        {{ errorMessage }}
        <button @click="errorMessage = ''" class="alert-close">×</button>
      </div>
      
      <div v-if="successMessage" class="alert alert-success">
        {{ successMessage }}
        <button @click="successMessage = ''" class="alert-close">×</button>
      </div>
      
      <!-- Main Content -->
      <main class="main-content">
        <div class="card">
          <div class="card-header">
            <h2>User Management</h2>
          </div>
          
          <!-- User Table -->
          <div class="table-container">
            <table class="user-table">
              <thead>
                <tr>
                  <th>Name</th>
                  <th>Email</th>
                  <th>Status</th>
                  <th>Created Date</th>
                  <th>Actions</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="user in users" :key="user.username">
                  <td>{{ user.name || 'N/A' }}</td>
                  <td>{{ user.email }}</td>
                  <td>
                    <span 
                      class="status-badge" 
                      :class="{ 'active': user.status === 'CONFIRMED', 'disabled': user.status !== 'CONFIRMED' }"
                    >
                      {{ user.status === 'CONFIRMED' ? 'Active' : 'Disabled' }}
                    </span>
                  </td>
                  <td>{{ new Date(user.created_date).toLocaleDateString() }}</td>
                  <td class="actions">
                    <button class="btn-action view" @click="showUserModal(user)">View</button>
                    <button 
                      v-if="user.status === 'CONFIRMED'" 
                      class="btn-action disable" 
                      @click="showConfirmModal(user, 'disable')"
                    >
                      Disable
                    </button>
                    <button 
                      v-else 
                      class="btn-action enable" 
                      @click="showConfirmModal(user, 'enable')"
                    >
                      Enable
                    </button>
                    <button 
                      class="btn-action reset" 
                      @click="showConfirmModal(user, 'reset')"
                    >
                      Reset PW
                    </button>
                    <button 
                      class="btn-action delete" 
                      @click="showConfirmModal(user, 'delete')"
                    >
                      Delete
                    </button>
                  </td>
                </tr>
                <tr v-if="users.length === 0">
                  <td colspan="5" class="no-data">No users found</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </main>
      
      <!-- User Details Modal -->
      <div v-if="isUserModalOpen" class="modal-backdrop" @click="closeUserModal">
        <div class="modal" @click.stop>
          <div class="modal-header">
            <h3>User Details</h3>
            <button class="close-button" @click="closeUserModal">×</button>
          </div>
          <div class="modal-body" v-if="selectedUser">
            <div class="user-details">
              <div class="detail-row">
                <strong>Username:</strong>
                <span>{{ selectedUser.username }}</span>
              </div>
              <div class="detail-row">
                <strong>Name:</strong>
                <span>{{ selectedUser.name || 'N/A' }}</span>
              </div>
              <div class="detail-row">
                <strong>Email:</strong>
                <span>{{ selectedUser.email }}</span>
              </div>
              <div class="detail-row">
                <strong>Phone:</strong>
                <span>{{ selectedUser.phone_number || 'N/A' }}</span>
              </div>
              <div class="detail-row">
                <strong>Status:</strong>
                <span>{{ selectedUser.status }}</span>
              </div>
              <div class="detail-row">
                <strong>Created:</strong>
                <span>{{ new Date(selectedUser.created_date).toLocaleString() }}</span>
              </div>
            </div>
          </div>
          <div class="modal-footer">
            <button class="btn-secondary" @click="closeUserModal">Close</button>
          </div>
        </div>
      </div>
      
      <!-- Confirmation Modal -->
      <div v-if="isConfirmModalOpen" class="modal-backdrop" @click="closeConfirmModal">
        <div class="modal" @click.stop>
          <div class="modal-header">
            <h3>Confirm Action</h3>
            <button class="close-button" @click="closeConfirmModal">×</button>
          </div>
          <div class="modal-body" v-if="selectedUser">
            <p v-if="actionType === 'disable'">
              Are you sure you want to disable user <strong>{{ selectedUser.email }}</strong>?
              The user will not be able to login until re-enabled.
            </p>
            <p v-else-if="actionType === 'enable'">
              Are you sure you want to enable user <strong>{{ selectedUser.email }}</strong>?
              The user will be able to login again.
            </p>
            <p v-else-if="actionType === 'reset'">
              Are you sure you want to reset the password for <strong>{{ selectedUser.email }}</strong>?
              The user will receive an email with instructions.
            </p>
            <p v-else-if="actionType === 'delete'">
              Are you sure you want to permanently delete user <strong>{{ selectedUser.email }}</strong>?
              This action cannot be undone.
            </p>
          </div>
          <div class="modal-footer">
            <button class="btn-secondary" @click="closeConfirmModal">Cancel</button>
            <button 
              class="btn-primary" 
              :class="{ 'btn-danger': actionType === 'delete' }"
              @click="handleConfirmAction"
            >
              Confirm
            </button>
          </div>
        </div>
      </div>
    </div>
    
    <!-- Unauthorized -->
    <div v-else class="unauthorized">
      <h1>Unauthorized</h1>
      <p>You don't have admin privileges to access this portal.</p>
      <button @click="handleLogout" class="btn-primary">Return to Login</button>
    </div>
  </div>
</template>

<style>
:root {
  --primary-color: #000000;
  --secondary-color: #333333;
  --accent-color: #666666;
  --text-color: #000000;
  --light-bg: #f8f8f8;
  --border-color: #e0e0e0;
  --card-bg: #ffffff;
}

body {
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  margin: 0;
  padding: 0;
  color: var(--text-color);
  background-color: white;
  font-size: 14px;
  line-height: 1.5;
}

* {
  box-sizing: border-box;
}

h1, h2, h3, h4, h5, h6 {
  margin-top: 0;
  font-weight: 600;
  letter-spacing: 0.5px;
}

button {
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  cursor: pointer;
  transition: all 0.2s;
}

.card {
  background-color: var(--card-bg);
  border: 1px solid var(--border-color);
  border-radius: 4px;
  padding: 20px;
}

.btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 8px 16px;
  border-radius: 4px;
  font-weight: 500;
  font-size: 14px;
  border: 1px solid transparent;
}

.btn-primary {
  background-color: var(--primary-color);
  color: white;
  border-color: var(--primary-color);
}

.btn-primary:hover {
  background-color: var(--secondary-color);
}

.btn-secondary {
  background-color: white;
  border-color: var(--border-color);
  color: var(--text-color);
}

.btn-secondary:hover {
  border-color: var(--primary-color);
}

.admin-app {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.loading, .unauthorized {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 100vh;
}

.spinner {
  width: 50px;
  height: 50px;
  border: 5px solid var(--border-color);
  border-top-color: var(--primary-color);
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin-bottom: 20px;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.btn-primary {
  background-color: var(--primary-color);
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 4px;
  cursor: pointer;
  font-weight: 500;
  transition: background-color 0.2s;
}

.btn-primary:hover {
  background-color: var(--secondary-color);
}
</style>
