<script setup lang="ts">
import { RouterView } from 'vue-router'
import { onMounted } from 'vue'
import { useAuthStore } from './stores/authStore'

// Initialize auth state from localStorage if present
const authStore = useAuthStore()
onMounted(() => {
  authStore.initialize()
})
</script>

<template>
  <div class="app-container">
    <header class="navbar">
      <div class="navbar-brand">
        <h1>The Grind</h1>
      </div>
      <div class="navbar-menu">
        <div v-if="authStore.isAuthenticated" class="auth-menu">
          <router-link to="/orders" class="menu-link">My Orders</router-link>
          <div class="user-dropdown">
            <span class="username">My Account</span>
            <div class="dropdown-content">
              <button @click="authStore.logout()" class="logout-btn">Sign Out</button>
            </div>
          </div>
        </div>
        <div v-else class="guest-menu">
          <button @click="redirectToLogin" class="login-btn">Sign In</button>
        </div>
      </div>
    </header>

    <main>
      <RouterView />
    </main>
  </div>
</template>

<script lang="ts">
export default {
  methods: {
    redirectToLogin() {
      const ssoUrl = import.meta.env.VITE_SSO_FRONTEND_URL
      const appName = import.meta.env.VITE_APPLICATION_NAME
      const channelId = import.meta.env.VITE_CHANNEL_ID
      const redirectUrl = `${window.location.origin}`
      
      window.location.href = `${ssoUrl}/login?application_name=${appName}&channel_id=${channelId}&redirect_url=${redirectUrl}`
    }
  }
}
</script>

<style>
* {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}

body {
  font-family: Arial, sans-serif;
  line-height: 1.6;
  color: #333;
}

.app-container {
  width: 100%;
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
}

.navbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px 0;
  border-bottom: 1px solid #eee;
}

.navbar-brand h1 {
  font-size: 1.8rem;
  color: #6b4226; /* Coffee brown */
}

.menu-link {
  text-decoration: none;
  color: #333;
  margin-right: 20px;
}

.login-btn, .logout-btn {
  background-color: #6b4226;
  color: white;
  border: none;
  padding: 8px 15px;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.9rem;
}

.login-btn:hover, .logout-btn:hover {
  background-color: #8c5a35;
}

.user-dropdown {
  position: relative;
  display: inline-block;
}

.username {
  cursor: pointer;
  padding: 8px;
}

.dropdown-content {
  display: none;
  position: absolute;
  right: 0;
  background-color: #f9f9f9;
  min-width: 160px;
  box-shadow: 0px 8px 16px 0px rgba(0,0,0,0.2);
  z-index: 1;
}

.user-dropdown:hover .dropdown-content {
  display: block;
}

.dropdown-content .logout-btn {
  width: 100%;
  text-align: left;
  padding: 12px 16px;
  border-radius: 0;
}

main {
  padding: 20px 0;
}
</style>
