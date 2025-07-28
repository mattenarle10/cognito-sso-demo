<script setup lang="ts">
import { ref, onMounted } from 'vue'
// Use proper relative paths for imports
import AdminLayout from './components/layout/AdminLayout.vue'
import { useAuth } from './composables/useAuth'

const isLoading = ref(true)
const isAdmin = ref(false)
const userName = ref('')
const { verifyAdmin, getUsername, logout } = useAuth()

onMounted(async () => {
  // Verify admin status from token
  isAdmin.value = await verifyAdmin()
  if (isAdmin.value) {
    userName.value = await getUsername()
  } else {
    // Redirect non-admin users to SSO login
    window.location.href = import.meta.env.VITE_SSO_URL || 'http://localhost:5173'
  }
  isLoading.value = false
})

const handleLogout = () => {
  logout()
  window.location.href = import.meta.env.VITE_SSO_URL || 'http://localhost:5173'
}
</script>

<template>
  <div class="admin-app">
    <div v-if="isLoading" class="loading">
      <div class="spinner"></div>
      <p>Verifying admin credentials...</p>
    </div>
    
    <AdminLayout 
      v-else-if="isAdmin" 
      :user-name="userName"
      @logout="handleLogout"
    />
    
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
