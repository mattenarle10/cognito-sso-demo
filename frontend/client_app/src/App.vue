<script setup lang="ts">
import { onMounted, computed } from 'vue'
import { RouterView, useRoute } from 'vue-router'
import { useAuthStore } from './stores/authStore'
import { redirectToLogin as loginRedirect } from './router'
import UserDropdown from './components/UserDropdown.vue'

const route = useRoute()
const authStore = useAuthStore()

// Hide header on home page to avoid duplication with HomePage.vue's header
const showHeader = computed(() => route.path !== '/')

// Get user's display name with preference for given_name or first part of full name
const getUserDisplayName = () => {
  if (authStore.user?.given_name) {
    return authStore.user.given_name
  } else if (authStore.user?.name) {
    return authStore.user.name.split(' ')[0]
  } else {
    return 'User'
  }
}

// Initialize auth state on app mount
onMounted(() => {
  authStore.initialize()
})

// Use the imported function with a different name
const redirectToLogin = () => {
  loginRedirect()
}
</script>

<template>
  <div class="app-container">
    <!-- Only show header on non-home pages -->
    <header v-if="showHeader" class="app-header">
      <nav class="app-nav">
        <div class="nav-brand">THE GRIND</div>
        <div class="nav-links">
          <router-link to="/" class="nav-link">Home</router-link>
          <router-link to="/orders" class="nav-link">Orders</router-link>
          <router-link to="/about" class="nav-link">About</router-link>
        </div>
        <div class="nav-auth">
          <div v-if="authStore.isAuthenticated">
            <UserDropdown :userName="getUserDisplayName()" />
          </div>
          <div v-else>
            <button @click="redirectToLogin" class="sign-in-button">SIGN IN</button>
          </div>
        </div>
      </nav>
    </header>
    
    <!-- Router view for all pages -->
    <RouterView />
  </div>
</template>

<style>
/* Global styles */
:root {
  --primary-bg: #000000;
  --secondary-bg: #1a1a1a;
  --primary-text: rgba(255, 255, 255, 0.87);
  --secondary-text: rgba(255, 255, 255, 0.6);
  --accent-color: #646cff;
  --border-color: rgba(255, 255, 255, 0.2);
}

body {
  margin: 0;
  padding: 0;
  font-family: system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  background-color: var(--primary-bg);
  color: var(--primary-text);
  min-height: 100vh;
}

#app {
  min-height: 100vh;
  width: 100%;
  margin: 0;
  padding: 0;
}

/* Reset default button styles */
button {
  cursor: pointer;
  font-family: inherit;
}

/* Reset default link styles */
a {
  text-decoration: none;
  color: inherit;
}
</style>

<style scoped>
/* App container */
.app-container {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

/* Header styles (only for non-home pages) */
.app-header {
  background-color: var(--secondary-bg);
  padding: 1rem 2rem;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.3);
}

.app-nav {
  display: flex;
  align-items: center;
  justify-content: space-between;
  max-width: 1200px;
  margin: 0 auto;
  width: 100%;
}

.nav-brand {
  font-size: 1.25rem;
  font-weight: 300;
  letter-spacing: 0.1em;
}

.nav-links {
  display: flex;
  gap: 2rem;
}

.nav-link {
  font-weight: 300;
  padding: 0.5rem 0;
  position: relative;
  transition: color 0.3s;
}

.nav-link:hover,
.nav-link.router-link-active {
  color: #fff;
}

.nav-link::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 0;
  width: 0;
  height: 1px;
  background-color: #fff;
  transition: width 0.3s;
}

.nav-link:hover::after,
.nav-link.router-link-active::after {
  width: 100%;
}

.sign-in-button {
  background-color: transparent;
  border: 1px solid var(--border-color, rgba(255, 255, 255, 0.2));
  color: var(--primary-text, white);
  padding: 0.5rem 1rem;
  font-size: 1rem;
  font-weight: 300;
  letter-spacing: 0.05em;
  cursor: pointer;
  transition: all 0.3s;
}

.sign-in-button:hover {
  background-color: rgba(255, 255, 255, 1);
  color: #000;
}

/* Responsive styles */
@media (max-width: 768px) {
  .app-nav {
    flex-direction: column;
    gap: 1rem;
  }
  
  .nav-links {
    order: 2;
  }
  
  .nav-auth {
    order: 3;
    margin-top: 1rem;
  }
}
</style>
