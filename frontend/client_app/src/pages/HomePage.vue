<template>
  <div class="home-container">
    <section class="hero">
      <h1>Welcome to The Grind</h1>
      <p>Your favorite coffee ordering application</p>
      
      <div v-if="!authStore.isAuthenticated" class="cta-section">
        <p>Sign in to view and manage your coffee orders</p>
        <button @click="redirectToLogin" class="cta-button">Sign In</button>
      </div>
      
      <div v-else class="welcome-back">
        <p>Welcome back! Check out your latest orders.</p>
        <router-link to="/orders" class="orders-link">View My Orders</router-link>
      </div>
    </section>
    
    <section class="features">
      <h2>Our Services</h2>
      <div class="feature-grid">
        <div class="feature">
          <h3>Mobile Ordering</h3>
          <p>Skip the line by ordering in advance</p>
        </div>
        <div class="feature">
          <h3>Loyalty Rewards</h3>
          <p>Earn points with every purchase</p>
        </div>
        <div class="feature">
          <h3>Custom Blends</h3>
          <p>Create your perfect coffee</p>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup lang="ts">
import { useAuthStore } from '../stores/authStore'

const authStore = useAuthStore()

function redirectToLogin() {
  const ssoUrl = import.meta.env.VITE_SSO_FRONTEND_URL
  const appName = import.meta.env.VITE_APPLICATION_NAME
  const channelId = import.meta.env.VITE_CHANNEL_ID
  const redirectUrl = `${window.location.origin}`
  
  window.location.href = `${ssoUrl}/login?application_name=${appName}&channel_id=${channelId}&redirect_url=${redirectUrl}`
}
</script>

<style scoped>
.home-container {
  padding: 20px 0;
}

.hero {
  text-align: center;
  padding: 60px 20px;
  background-color: #f8f5f2;
  border-radius: 8px;
  margin-bottom: 40px;
}

.hero h1 {
  font-size: 2.5rem;
  color: #6b4226;
  margin-bottom: 10px;
}

.hero p {
  font-size: 1.2rem;
  color: #666;
  margin-bottom: 30px;
}

.cta-section {
  margin: 30px 0;
}

.cta-button {
  background-color: #6b4226;
  color: white;
  border: none;
  padding: 12px 30px;
  font-size: 1rem;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.cta-button:hover {
  background-color: #8c5a35;
}

.welcome-back {
  margin: 30px 0;
}

.orders-link {
  display: inline-block;
  background-color: #6b4226;
  color: white;
  text-decoration: none;
  padding: 12px 30px;
  font-size: 1rem;
  border-radius: 4px;
  margin-top: 15px;
  transition: background-color 0.3s;
}

.orders-link:hover {
  background-color: #8c5a35;
}

.features {
  padding: 40px 0;
}

.features h2 {
  text-align: center;
  color: #6b4226;
  margin-bottom: 30px;
}

.feature-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 30px;
}

.feature {
  background-color: #fff;
  padding: 30px;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  text-align: center;
}

.feature h3 {
  color: #6b4226;
  margin-bottom: 15px;
}
</style>
