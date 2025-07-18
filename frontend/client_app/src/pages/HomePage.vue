<template>
  <div class="home-page min-h-screen bg-black text-white overflow-hidden">
    <!-- Header -->
    <header class="fixed top-0 left-0 right-0 z-50 px-8 py-6">
      <nav class="flex items-center justify-between max-w-7xl mx-auto">
        <div class="text-2xl font-light tracking-[0.2em]">THE GRIND</div>

        <div class="flex items-center">
          <template v-if="authStore.isAuthenticated">
            <UserDropdown :userName="getUserDisplayName()" />
          </template>
          <template v-else>
            <button
              @click="redirectToLogin"
              class="sign-in-button"
            >
              SIGN IN
            </button>
          </template>
        </div>
      </nav>
    </header>

    <!-- Animated Background -->
    <div class="fixed inset-0 bg-gradient">
      <!-- Animated dots -->
      <div v-for="i in 8" :key="i" class="animated-dot" :style="getRandomDotStyle(i)"></div>
    </div>

    <!-- Main Content -->
    <main class="relative z-10 flex items-center justify-center min-h-screen px-8">
      <div class="text-center max-w-6xl mx-auto">
        <div class="content-wrapper">
          <div class="title-section">
            <h1 class="main-title">THE</h1>
            <h1 class="main-title subtitle">GRIND</h1>
          </div>

          <div class="cta-section">
            <p class="tagline">PREMIUM MEMBERSHIP</p>

            <template v-if="!authStore.isAuthenticated">
              <div class="button-container">
                <button @click="redirectToLogin" class="primary-button">
                  ENTER
                </button>
              </div>
            </template>
            <template v-else>
              <div class="welcome-section">
                <div class="welcome-text">WELCOME BACK</div>
                <div class="button-group">
                  <router-link to="/orders">
                    <button class="primary-button">ORDERS</button>
                  </router-link>
                  <router-link to="/profile">
                    <button class="secondary-button">PROFILE</button>
                  </router-link>
                </div>
              </div>
            </template>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup lang="ts">
import { useAuthStore } from '../stores/authStore'
import UserDropdown from '../components/UserDropdown.vue'
import { redirectToLogin } from '../router'

const authStore = useAuthStore()

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

// Generate random positions for animated dots
function getRandomDotStyle(index: number) {
  const positions = [
    { top: '25%', left: '15%', size: '12px', delay: '0s', duration: '8s' },
    { top: '65%', left: '80%', size: '8px', delay: '0.5s', duration: '10s' },
    { top: '35%', right: '20%', size: '15px', delay: '1s', duration: '9s' },
    { top: '75%', left: '30%', size: '10px', delay: '1.5s', duration: '7s' },
    { top: '15%', right: '15%', size: '14px', delay: '2s', duration: '11s' },
    { top: '45%', left: '10%', size: '9px', delay: '2.5s', duration: '9s' },
    { top: '85%', right: '25%', size: '11px', delay: '3s', duration: '10s' },
    { top: '55%', left: '70%', size: '13px', delay: '3.5s', duration: '8s' },
  ]
  
  const pos = positions[index % positions.length]
  return {
    ...pos,
    width: pos.size,
    height: pos.size,
    animationDelay: pos.delay,
    animationDuration: pos.duration,
    opacity: (Math.random() * 0.3 + 0.1).toString()
  }
}
</script>

<style scoped>
/* Base styles */
.home-page {
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
  padding: 0 2rem;
}

.content-wrapper {
  display: flex;
  flex-direction: column;
  gap: 3rem;
}

/* Title section */
.title-section {
  display: flex;
  flex-direction: column;
  gap: 0;
}

.main-title {
  font-size: 6rem;
  font-weight: 100;
  letter-spacing: -0.02em;
  line-height: 1;
}

.subtitle {
  margin-top: -1.5rem;
}

/* Divider */
.divider {
  width: 1px;
  height: 6rem;
  background-color: rgba(255, 255, 255, 0.2);
  margin: 0 auto;
}

/* CTA section */
.cta-section {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.tagline {
  font-size: 1.25rem;
  font-weight: 300;
  letter-spacing: 0.1em;
  color: rgba(255, 255, 255, 0.6);
  max-width: 42rem;
  margin: 0 auto;
}

.button-container {
  display: flex;
  justify-content: center;
}

/* Button styles */
.primary-button {
  background-color: #fff;
  color: #000;
  padding: 1rem 3rem;
  font-size: 1.125rem;
  font-weight: 300;
  letter-spacing: 0.1em;
  transition: all 0.3s;
  border: none;
}

.primary-button:hover {
  background-color: rgba(255, 255, 255, 0.9);
  transform: scale(1.05);
}

.secondary-button {
  background-color: transparent;
  color: #fff;
  border: 1px solid rgba(255, 255, 255, 0.2);
  padding: 0.75rem 2rem;
  font-size: 1rem;
  font-weight: 300;
  letter-spacing: 0.1em;
  transition: all 0.3s;
}

.secondary-button:hover {
  background-color: #fff;
  color: #000;
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

/* Welcome section */
.welcome-section {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.welcome-text {
  font-size: 2.25rem;
  font-weight: 100;
  letter-spacing: -0.02em;
}

.button-group {
  display: flex;
  gap: 1.5rem;
  justify-content: center;
  align-items: center;
}

/* Media queries */
@media (min-width: 768px) {
  .main-title {
    font-size: 8rem;
  }
  
  .tagline {
    font-size: 1.5rem;
  }
  
  .welcome-text {
    font-size: 3.75rem;
  }
}
</style>
