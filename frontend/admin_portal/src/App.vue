<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useAuth } from './composables/useAuth'
import { UserService, type User } from './services/UserService'
import AdminPage from './pages/AdminPage.vue'

// State
const isLoading = ref(true)
const isAdmin = ref(false)
const userName = ref('')
const errorMessage = ref('')

// Auth functions
const { verifyAdmin, getUsername, logout } = useAuth()

// Load data
onMounted(async () => {
  // Verify admin status from token
  try {
    isAdmin.value = await verifyAdmin()
    if (isAdmin.value) {
      userName.value = await getUsername()
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
    <div v-else-if="isAdmin">
      <AdminPage :current-user="{ email: userName }" :logout="handleLogout" />
    </div>
    
    <!-- Unauthorized State -->
    <div v-else class="unauthorized">
      <h2>Unauthorized</h2>
      <p>You do not have permission to access the admin portal.</p>
      <button class="btn-primary" @click="handleLogout">Back to Login</button>
    </div>
    
    <!-- Error Message -->
    <div v-if="errorMessage" class="alert alert-error">
      {{ errorMessage }}
      <button @click="errorMessage = ''" class="alert-close">×</button>
    </div>
  </div>
</template>

<style>
/* App-specific styles */
.admin-app {
  width: 100%;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

/* Loading & Unauthorized */
.loading, .unauthorized {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 100vh;
}

.spinner {
  border: 4px solid rgba(0, 0, 0, 0.1);
  width: 36px;
  height: 36px;
  border-radius: 50%;
  border-left-color: var(--primary-color);
  animation: spin 1s linear infinite;
  margin-bottom: 16px;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

/* Alerts */
.alert {
  padding: 12px 16px;
  margin: 16px 24px 0;
  border-radius: 4px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  position: fixed;
  top: 16px;
  right: 16px;
  z-index: 1000;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.alert-error {
  background-color: #f8eaec;
  color: var(--error-color);
  border: 1px solid #f5c6cb;
}

.alert-close {
  background: transparent;
  border: none;
  font-size: 18px;
  cursor: pointer;
  padding: 0;
  line-height: 1;
}

/* Buttons */
.btn-primary {
  background-color: var(--primary-color);
  color: white;
  border: none;
  padding: 8px 16px;
  border-radius: 4px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-primary:hover {
  background-color: var(--secondary-color);
}

/* Responsive */
@media (max-width: 768px) {
  .unauthorized h2 {
    font-size: 1.5rem;
  }
}
</style>
