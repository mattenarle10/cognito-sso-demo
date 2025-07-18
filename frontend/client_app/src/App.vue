<script setup lang="ts">
import { onMounted } from 'vue'
import { RouterView } from 'vue-router'
import { useAuthStore } from './stores/authStore'

const authStore = useAuthStore()

// Initialize auth state on app mount
onMounted(() => {
  authStore.initialize()
})
</script>

<template>
  <div class="app-container">
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
  --card-bg: rgba(26, 26, 26, 0.8);
  --card-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
  --transition-speed: 0.3s;
}

/* Apply a smooth scrolling effect to the whole page */
html {
  scroll-behavior: smooth;
}

body {
  margin: 0;
  padding: 0;
  font-family: system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  background-color: var(--primary-bg);
  color: var(--primary-text);
  min-height: 100vh;
  line-height: 1.6;
  font-weight: 300;
  overflow-x: hidden;
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
  border: none;
  outline: none;
  transition: all var(--transition-speed);
}

/* Reset default link styles */
a {
  text-decoration: none;
  color: inherit;
  transition: all var(--transition-speed);
}

/* Form elements styling */
input, select, textarea {
  font-family: inherit;
  font-size: 1rem;
  padding: 0.75rem 1rem;
  background-color: rgba(255, 255, 255, 0.05);
  border: 1px solid var(--border-color);
  color: var(--primary-text);
  border-radius: 4px;
  transition: all var(--transition-speed);
}

input:focus, select:focus, textarea:focus {
  border-color: rgba(255, 255, 255, 0.5);
  outline: none;
  box-shadow: 0 0 0 2px rgba(255, 255, 255, 0.1);
}

/* Custom scrollbar */
::-webkit-scrollbar {
  width: 8px;
  height: 8px;
}

::-webkit-scrollbar-track {
  background: rgba(0, 0, 0, 0.2);
}

::-webkit-scrollbar-thumb {
  background: rgba(255, 255, 255, 0.2);
  border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
  background: rgba(255, 255, 255, 0.3);
}
</style>

<style scoped>
/* App container */
.app-container {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  position: relative;
  overflow: hidden;
}

/* Add subtle animated gradient background */
.app-container::before {
  content: '';
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: radial-gradient(circle at 30% 30%, rgba(30, 30, 30, 0.4) 0%, rgba(0, 0, 0, 0) 70%),
              radial-gradient(circle at 70% 70%, rgba(30, 30, 30, 0.3) 0%, rgba(0, 0, 0, 0) 70%);
  z-index: -1;
  pointer-events: none;
}
</style>
