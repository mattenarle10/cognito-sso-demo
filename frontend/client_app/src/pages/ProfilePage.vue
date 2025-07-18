<template>
  <div class="profile-page min-h-screen bg-black text-white overflow-hidden">
    <!-- Header -->
    <header class="fixed top-0 left-0 right-0 z-50 px-4 py-4">
      <nav class="flex items-center justify-between max-w-4xl mx-auto">
        <div class="flex items-center">
          <button @click="router.push('/')" class="back-button">
            <span class="back-icon">←</span> BACK
          </button>
        </div>
        <div class="flex items-center">
          <UserDropdown :userName="getUserDisplayName()" />
        </div>
      </nav>
    </header>
    
    <!-- Animated Background -->
    <div class="fixed inset-0 bg-gradient">
      <!-- Animated dots -->
      <div v-for="i in 8" :key="i" class="animated-dot" :style="getRandomDotStyle(i)"></div>
    </div>
    
    <!-- Main Content -->
    <main class="relative z-10 flex items-center justify-center min-h-screen px-4 pt-24 pb-12">
      <div class="profile-container w-full mx-auto">
        <h1 class="profile-title">PROFILE</h1>
        
        <div class="profile-card">
          <div class="profile-header">
            <div class="avatar">
              {{ initials }}
            </div>
            <div class="user-name">
              <h2>{{ authStore.user?.name || 'User' }}</h2>
              <p class="email">{{ authStore.user?.email }}</p>
            </div>
          </div>
        
          <div class="profile-details">
            <div class="detail-row">
              <div class="detail-label">First Name</div>
              <div class="detail-value">{{ firstName }}</div>
            </div>
            
            <div class="detail-row">
              <div class="detail-label">Last Name</div>
              <div class="detail-value">{{ lastName }}</div>
            </div>
            
            <div class="detail-row">
              <div class="detail-label">Phone Number</div>
              <div class="detail-value">{{ authStore.user?.phone_number || '-' }}</div>
            </div>
            
            <div class="detail-row">
              <div class="detail-label">Gender</div>
              <div class="detail-value">{{ capitalizeFirstLetter(authStore.user?.gender) || '-' }}</div>
            </div>
            
            <div class="detail-row">
              <div class="detail-label">Email Verified</div>
              <div class="detail-value">
                <span :class="['verification-status', authStore.user?.email_verified ? 'verified' : 'not-verified']">
                  {{ authStore.user?.email_verified ? 'Verified' : 'Not Verified' }}
                </span>
              </div>
            </div>
          </div>
        </div>
        
        <div class="actions">
          <button @click="redirectToLogin" class="manage-profile-btn">MANAGE ACCOUNT</button>
          <button @click="signOut" class="sign-out-btn">SIGN OUT</button>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/authStore'
import UserDropdown from '../components/UserDropdown.vue'

const router = useRouter()
const authStore = useAuthStore()

// Computed property to get user initials
const initials = computed(() => {
  const name = authStore.user?.name || ''
  if (!name) return 'U'
  
  const parts = name.split(' ')
  if (parts.length === 1) return parts[0].charAt(0).toUpperCase()
  return (parts[0].charAt(0) + parts[parts.length - 1].charAt(0)).toUpperCase()
})

// Computed properties to get first and last name from full name if needed
const firstName = computed(() => {
  if (authStore.user?.given_name) return authStore.user.given_name
  if (authStore.user?.name) {
    const parts = authStore.user.name.split(' ')
    return parts[0] || '-'
  }
  return '-'
})

const lastName = computed(() => {
  if (authStore.user?.family_name) return authStore.user.family_name
  if (authStore.user?.name) {
    const parts = authStore.user.name.split(' ')
    return parts.length > 1 ? parts[parts.length - 1] : '-'
  }
  return '-'
})

// Function to get user display name
function getUserDisplayName(): string {
  return authStore.user?.name || 'User'
}

// Function to capitalize first letter
function capitalizeFirstLetter(str?: string): string {
  if (!str) return ''
  return str.charAt(0).toUpperCase() + str.slice(1).toLowerCase()
}

// Function to sign out
function signOut() {
  authStore.logout()
}

// Function to redirect to login page
function redirectToLogin() {
  window.location.href = import.meta.env.VITE_SSO_FRONTEND_URL + '/profile'
}

// Generate random dot styles for background animation
function getRandomDotStyle(_: number) {
  const size = Math.floor(Math.random() * 6) + 2 + 'px'
  const animationDuration = (Math.random() * 50) + 50 + 's'
  const initialTop = Math.floor(Math.random() * 100) + '%'
  const initialLeft = Math.floor(Math.random() * 100) + '%'
  const delay = (Math.random() * 40) + 's'
  
  return {
    width: size,
    height: size,
    top: initialTop,
    left: initialLeft,
    animationDuration,
    animationDelay: delay
  }
}
</script>

<style scoped>
/* Base styles */
.profile-page {
  min-height: 100vh;
  background-color: #000;
  color: #fff;
  overflow: hidden;
  font-family: system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
}

/* Header styles */
header {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 50;
  padding: 1.5rem 2rem;
}

nav {
  display: flex;
  align-items: center;
  justify-content: space-between;
  max-width: 80rem;
  margin: 0 auto;
}

.text-2xl {
  font-size: 1.5rem;
  font-weight: 300;
  letter-spacing: 0.2em;
}

.back-button {
  background-color: transparent;
  border: 1px solid rgba(255, 255, 255, 0.2);
  color: #fff;
  padding: 0.5rem 1rem;
  font-size: 0.875rem;
  font-weight: 300;
  letter-spacing: 0.05em;
  cursor: pointer;
  transition: all 0.3s;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.back-button:hover {
  background-color: rgba(255, 255, 255, 0.1);
}

.back-icon {
  font-size: 1.25rem;
  line-height: 1;
}

/* Background styles */
.bg-gradient {
  background: linear-gradient(135deg, #000000 0%, #1a1a1a 100%);
}

.animated-dot {
  position: absolute;
  background-color: rgba(255, 255, 255, 0.15);
  border-radius: 50%;
  animation: float 10s infinite ease-in-out;
}

@keyframes float {
  0%, 100% { transform: translateY(0) rotate(0deg); }
  25% { transform: translateY(-20px) rotate(90deg); }
  50% { transform: translateY(0) rotate(180deg); }
  75% { transform: translateY(20px) rotate(270deg); }
}

/* Main content styles */
main {
  position: relative;
  z-index: 10;
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 100vh;
  padding: 0;
}

.profile-container {
  width: 100%;
  max-width: 600px;
  padding: 0 1.5rem;
  margin: 0 auto;
}

.profile-title {
  font-size: 2.5rem;
  font-weight: 100;
  margin-bottom: 2.5rem;
  letter-spacing: 0.1em;
  text-align: center;
}

.profile-card {
  background-color: rgba(26, 26, 26, 0.8);
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 15px 35px rgba(0, 0, 0, 0.3);
  margin-bottom: 2.5rem;
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.08);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.profile-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.4);
}

.profile-header {
  display: flex;
  align-items: center;
  padding: 2rem;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.avatar {
  width: 80px;
  height: 80px;
  border-radius: 50%;
  background-color: rgba(255, 255, 255, 0.1);
  color: #fff;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 2rem;
  font-weight: 300;
  margin-right: 1.5rem;
  border: 1px solid rgba(255, 255, 255, 0.2);
}

.user-name h2 {
  font-size: 1.8rem;
  font-weight: 300;
  margin: 0 0 0.5rem 0;
  letter-spacing: -0.02em;
}

.email {
  color: rgba(255, 255, 255, 0.6);
  margin: 0;
  font-size: 1rem;
}

.profile-details {
  padding: 2rem;
}

.detail-row {
  display: flex;
  margin-bottom: 1.5rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid rgba(255, 255, 255, 0.05);
}

.detail-row:last-child {
  margin-bottom: 0;
  padding-bottom: 0;
  border-bottom: none;
}

.detail-label {
  width: 150px;
  color: rgba(255, 255, 255, 0.6);
  font-size: 0.9rem;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.detail-value {
  flex: 1;
  font-size: 1rem;
}

.verification-status {
  display: inline-block;
  padding: 0.25rem 0.75rem;
  border-radius: 4px;
  font-size: 0.8rem;
  font-weight: 500;
}

.verified {
  background-color: rgba(46, 125, 50, 0.2);
  color: #4caf50;
}

.not-verified {
  background-color: rgba(211, 47, 47, 0.2);
  color: #f44336;
}

.actions {
  display: flex;
  gap: 1.25rem;
  margin-top: 2.5rem;
  justify-content: center;
}

.manage-profile-btn, .sign-out-btn {
  padding: 0.85rem 2rem;
  font-size: 0.95rem;
  font-weight: 400;
  letter-spacing: 0.1em;
  border-radius: 6px;
  border: none;
  cursor: pointer;
  transition: all 0.3s ease;
  min-width: 180px;
  text-align: center;
}

.manage-profile-btn {
  background-color: #fff;
  color: #000;
  box-shadow: 0 4px 12px rgba(255, 255, 255, 0.15);
}

.manage-profile-btn:hover {
  background-color: rgba(255, 255, 255, 0.95);
  transform: translateY(-3px);
  box-shadow: 0 6px 16px rgba(255, 255, 255, 0.2);
}

.sign-out-btn {
  background-color: transparent;
  color: #fff;
  border: 1px solid rgba(255, 255, 255, 0.2);
}

.sign-out-btn:hover {
  background-color: rgba(255, 255, 255, 0.1);
  transform: translateY(-2px);
}

@media (max-width: 768px) {
  .profile-title {
    font-size: 2rem;
  }
  
  .profile-header {
    flex-direction: column;
    text-align: center;
  }
  
  .avatar {
    margin-right: 0;
    margin-bottom: 1rem;
  }
  
  .detail-row {
    flex-direction: column;
  }
  
  .detail-label {
    width: 100%;
    margin-bottom: 0.5rem;
  }
  
  .actions {
    flex-direction: column;
  }
  
  .manage-profile-btn, .sign-out-btn {
    width: 100%;
  }
}
</style>