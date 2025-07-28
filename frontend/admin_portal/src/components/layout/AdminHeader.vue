<script setup lang="ts">
defineProps<{
  userName: string
}>()

defineEmits<{
  (e: 'logout'): void
}>()
</script>

<template>
  <header class="admin-header">
    <div class="admin-header-content">
      <div class="header-title">
        <span class="material-symbols-outlined menu-icon">menu</span>
        <h1>THE GRIND • ADMIN PORTAL</h1>
      </div>
      
      <div class="user-controls">
        <span class="user-name">{{ userName }}</span>
        <button @click="$emit('logout')" class="logout-btn">
          <span class="material-symbols-outlined logout-icon">logout</span>
          <span>Logout</span>
        </button>
      </div>
    </div>
  </header>
</template>

<style scoped>
.admin-header {
  background-color: white;
  border-bottom: 1px solid var(--border-color);
  z-index: 10;
}

.admin-header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 20px;
  height: 64px;
  max-width: 1400px;
  margin: 0 auto;
  width: 100%;
}

.header-title {
  display: flex;
  align-items: center;
  gap: 16px;
}

.menu-icon {
  cursor: pointer;
  color: var(--secondary-color);
}

h1 {
  font-size: 1rem;
  font-weight: 600;
  margin: 0;
  color: var(--primary-color);
  letter-spacing: 0.5px;
}

.user-controls {
  display: flex;
  align-items: center;
  gap: 16px;
}

.user-name {
  font-weight: 500;
}

.logout-btn {
  background-color: transparent;
  border: 1px solid var(--border-color);
  border-radius: 4px;
  padding: 8px 12px;
  cursor: pointer;
  font-weight: 500;
  transition: all 0.2s;
  display: flex;
  align-items: center;
  gap: 8px;
}

.logout-btn:hover {
  background-color: #f8f8f8;
  border-color: #000000;
}

.logout-icon {
  font-size: 18px;
}
</style>
