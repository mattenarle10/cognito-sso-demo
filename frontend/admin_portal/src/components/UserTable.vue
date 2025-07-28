<template>
  <div class="table-container">
    <table class="user-table">
      <thead>
        <tr>
          <th>Name</th>
          <th>Email</th>
          <th>Status</th>
          <th>Created Date</th>
          <th>Actions</th>
        </tr>
      </thead>
      <tbody>
        <tr v-if="users.length === 0">
          <td colspan="5" class="no-data">No users found</td>
        </tr>
        <tr v-for="user in users" :key="user.username">
          <td>{{ user.name || 'N/A' }}</td>
          <td>{{ user.email }}</td>
          <td>
            <span :class="['status-badge', user.status === 'CONFIRMED' && user.enabled ? 'active' : 'disabled']">
              {{ user.status === 'CONFIRMED' && user.enabled ? 'Active' : 'Disabled' }}
            </span>
          </td>
          <td>{{ new Date(user.created_date).toLocaleDateString() }}</td>
          <td class="actions">
            <button class="btn-action view" @click="$emit('view-user', user)">View</button>
            <button v-if="user.enabled" class="btn-action disable" @click="$emit('disable-user', user)">Disable</button>
            <button v-else class="btn-action enable" @click="$emit('enable-user', user)">Enable</button>
            <button class="btn-action reset" @click="$emit('reset-password', user)">Reset Password</button>
            <button class="btn-action delete" @click="$emit('delete-user', user)">Delete</button>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script setup lang="ts">
interface User {
  username: string;
  name?: string;
  email: string;
  phone_number?: string;
  status: string;
  enabled: boolean;
  created_date: string;
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
