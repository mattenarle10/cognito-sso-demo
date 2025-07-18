<template>
  <div class="profile-page">
    <div class="container">
      <h1 class="page-title">Profile</h1>
      
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
            <div class="detail-value">{{ authStore.user?.given_name || '-' }}</div>
          </div>
          
          <div class="detail-row">
            <div class="detail-label">Last Name</div>
            <div class="detail-value">{{ authStore.user?.family_name || '-' }}</div>
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
        <button @click="redirectToLogin" class="manage-profile-btn">MANAGE PROFILE</button>
        <button @click="signOut" class="sign-out-btn">SIGN OUT</button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useAuthStore } from '../stores/authStore'
import { useRouter } from 'vue-router'
import { redirectToLogin } from '../router'

const router = useRouter()
const authStore = useAuthStore()

// Calculate initials from user's name
const initials = computed(() => {
  const name = authStore.user?.name || ''
  if (!name) return 'U'
  
  const parts = name.split(' ')
  if (parts.length === 1) return parts[0].charAt(0).toUpperCase()
  return (parts[0].charAt(0) + parts[parts.length - 1].charAt(0)).toUpperCase()
})

// Helper function to capitalize first letter
function capitalizeFirstLetter(string?: string) {
  if (!string) return null
  return string.charAt(0).toUpperCase() + string.slice(1)
}

// Sign out function
function signOut() {
  authStore.logout()
  router.push('/')
}
</script>

<style scoped>
.profile-page {
  min-height: 100vh;
  background-color: #121212;
  color: #fff;
  padding: 2rem 1rem;
}

.container {
  max-width: 800px;
  margin: 0 auto;
}

.page-title {
  font-size: 2.5rem;
  font-weight: 200;
  margin-bottom: 2rem;
  letter-spacing: -0.02em;
}

.profile-card {
  background-color: #1a1a1a;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
  margin-bottom: 2rem;
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
  background-color: #333;
  color: #fff;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 2rem;
  font-weight: 300;
  margin-right: 1.5rem;
}

.user-name h2 {
  font-size: 1.8rem;
  font-weight: 400;
  margin: 0 0 0.5rem 0;
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
  gap: 1rem;
  margin-top: 2rem;
}

.manage-profile-btn, .sign-out-btn {
  padding: 0.75rem 1.5rem;
  font-size: 1rem;
  font-weight: 300;
  letter-spacing: 0.05em;
  border: none;
  cursor: pointer;
  transition: all 0.3s;
}

.manage-profile-btn {
  background-color: #fff;
  color: #000;
}

.manage-profile-btn:hover {
  background-color: rgba(255, 255, 255, 0.9);
  transform: translateY(-2px);
}

.sign-out-btn {
  background-color: transparent;
  color: #fff;
  border: 1px solid rgba(255, 255, 255, 0.2);
}

.sign-out-btn:hover {
  background-color: rgba(255, 255, 255, 0.1);
}

@media (max-width: 768px) {
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