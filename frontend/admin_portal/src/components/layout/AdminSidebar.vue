<script setup lang="ts">
import { ref } from 'vue'

const navItems = [
  { name: 'Dashboard', icon: 'grid_view' },
  { name: 'Users', icon: 'group' },
  { name: 'Applications', icon: 'apps' },
  { name: 'Settings', icon: 'settings' }
]

const activeItem = ref('Dashboard')
</script>

<template>
  <aside class="admin-sidebar">
    <div class="logo">
      <h2>THE GRIND</h2>
      <span class="subtitle">ADMIN PORTAL</span>
    </div>
    
    <nav>
      <ul>
        <li 
          v-for="item in navItems" 
          :key="item.name"
          :class="{ active: activeItem === item.name }"
          @click="activeItem = item.name"
        >
          <span class="material-symbols-outlined icon">{{ item.icon }}</span>
          <span>{{ item.name }}</span>
        </li>
      </ul>
    </nav>
    
    <div class="sidebar-footer">
      <span class="version">v1.0.0</span>
    </div>
  </aside>
</template>

<style scoped>
.admin-sidebar {
  width: 250px;
  background-color: #000000;
  color: white;
  display: flex;
  flex-direction: column;
  height: 100vh;
  box-shadow: 2px 0 5px rgba(0, 0, 0, 0.05);
}

.logo {
  padding: 24px 20px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

h2 {
  margin: 0;
  font-size: 1.5rem;
  font-weight: 600;
}

.subtitle {
  font-size: 0.875rem;
  opacity: 0.7;
}

nav {
  flex: 1;
  padding: 20px 0;
}

ul {
  list-style-type: none;
  margin: 0;
  padding: 0;
}

li {
  padding: 12px 20px;
  display: flex;
  align-items: center;
  gap: 12px;
  cursor: pointer;
  transition: background-color 0.2s;
  border-left: 3px solid transparent;
}

li:hover {
  background-color: rgba(255, 255, 255, 0.05);
}

li.active {
  background-color: rgba(255, 255, 255, 0.1);
  border-left-color: var(--primary-color);
}

.icon {
  width: 24px;
  display: inline-flex;
  justify-content: center;
  font-size: 20px;
}

.sidebar-footer {
  padding: 16px 20px;
  font-size: 0.75rem;
  opacity: 0.5;
  text-align: center;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
}
</style>
