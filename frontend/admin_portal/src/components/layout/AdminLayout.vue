<script setup lang="ts">
// Import components directly from their relative paths
import AdminHeader from './AdminHeader.vue'
import AdminSidebar from './AdminSidebar.vue'
import Dashboard from '../../pages/Dashboard.vue'

defineProps<{
  userName: string
}>()

defineEmits<{
  (e: 'logout'): void
}>()
</script>

<template>
  <div class="admin-layout">
    <AdminSidebar />
    
    <div class="admin-content">
      <AdminHeader 
        :user-name="userName"
        @logout="$emit('logout')"
      />
      
      <main>
        <Dashboard />
      </main>
    </div>
  </div>
</template>

<style scoped>
.admin-layout {
  display: flex;
  min-height: 100vh;
}

.admin-content {
  flex: 1;
  display: flex;
  flex-direction: column;
}

main {
  flex: 1;
  padding: 24px;
  background-color: var(--light-bg);
  max-width: 100%;
  overflow-x: auto;
}
</style>
