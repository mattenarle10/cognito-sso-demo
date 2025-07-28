<template>
  <div class="table-container">
    <table class="user-table">
      <thead>
        <tr>
          <th><i class="fas fa-user"></i> Name</th>
          <th><i class="fas fa-envelope"></i> Email</th>
          <th><i class="fas fa-circle-info"></i> Status</th>
          <th><i class="fas fa-calendar"></i> Created</th>
          <th><i class="fas fa-tools"></i> Actions</th>
        </tr>
      </thead>
      <tbody>
        <tr v-if="users.length === 0">
          <td colspan="5" class="no-data">No users found</td>
        </tr>
        <tr v-for="user in users" :key="user.username">
          <td>{{ user.attributes?.name || 'N/A' }}</td>
          <td>{{ user.attributes?.email || '' }}</td>
          <td>
            <span :class="['status-badge', user.user_status === 'CONFIRMED' && user.enabled ? 'active' : 'disabled']">
              {{ user.user_status === 'CONFIRMED' && user.enabled ? 'Active' : 'Disabled' }}
            </span>
          </td>
          <td>{{ user.user_create_date ? new Date(user.user_create_date).toLocaleDateString() : 'N/A' }}</td>
          <td class="actions">
            <button class="btn-action view" @click="$emit('view-user', user)" title="View User Details">
              <i class="fas fa-eye"></i>
            </button>
            <button v-if="user.enabled" class="btn-action disable" @click="$emit('disable-user', user)" title="Disable User">
              <i class="fas fa-ban"></i>
            </button>
            <button v-else class="btn-action enable" @click="$emit('enable-user', user)" title="Enable User">
              <i class="fas fa-check-circle"></i>
            </button>
            <button class="btn-action reset" @click="$emit('reset-password', user)" title="Reset Password">
              <i class="fas fa-key"></i>
            </button>
            <button class="btn-action delete" @click="$emit('delete-user', user)" title="Delete User">
              <i class="fas fa-trash-alt"></i>
            </button>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script setup lang="ts">
interface User {
  username: string;
  user_status: string;
  enabled: boolean;
  user_create_date: string;
  user_last_modified_date: string;
  attributes?: {
    name?: string;
    email?: string;
    phone_number?: string;
    'email_verified'?: string;
    'phone_number_verified'?: string;
    gender?: string;
    'custom:accepts_marketing'?: string;
    sub?: string;
    [key: string]: any;
  };
  [key: string]: any;
}

defineProps<{
  users: User[]
}>();

defineEmits<{
  (e: 'view-user', user: User): void
  (e: 'disable-user', user: User): void
  (e: 'enable-user', user: User): void
  (e: 'reset-password', user: User): void
  (e: 'delete-user', user: User): void
}>();
</script>

<style scoped>
.table-container {
  width: 100%;
  overflow-x: auto;
  margin: 1rem 0;
  border-radius: 4px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.user-table {
  width: 100%;
  border-collapse: collapse;
  background-color: #fff;
  font-size: 0.9rem;
}

.user-table th,
.user-table td {
  padding: 0.75rem 1rem;
  text-align: left;
  border-bottom: 1px solid #eee;
}

.user-table th {
  background-color: #f8f8f8;
  font-weight: 600;
  color: #333;
  position: sticky;
  top: 0;
  z-index: 1;
}

.user-table tr:hover {
  background-color: #f5f5f5;
}

.status-badge {
  display: inline-block;
  padding: 0.25rem 0.5rem;
  border-radius: 12px;
  font-size: 0.8rem;
  font-weight: 500;
}

.status-badge.active {
  background-color: rgba(0, 128, 0, 0.1);
  color: green;
}

.status-badge.disabled {
  background-color: rgba(128, 128, 128, 0.1);
  color: #666;
}

.actions {
  display: flex;
  gap: 0.5rem;
  flex-wrap: nowrap;
  justify-content: flex-start;
}

.btn-action {
  width: 36px;
  height: 36px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.9rem;
  transition: all 0.2s;
  display: flex;
  align-items: center;
  justify-content: center;
}

.btn-action.view {
  background-color: #e7f5ff;
  color: #0077cc;
}

.btn-action.disable {
  background-color: #fff5f5;
  color: #e03131;
}

.btn-action.enable {
  background-color: #ebfbee;
  color: #2b8a3e;
}

.btn-action.reset {
  background-color: #fff9db;
  color: #f08c00;
}

.btn-action.delete {
  background-color: #ffeeee;
  color: #c92a2a;
}

.btn-action:hover {
  filter: brightness(0.95);
}

.no-data {
  text-align: center;
  color: #666;
  padding: 2rem 0;
}
</style>
