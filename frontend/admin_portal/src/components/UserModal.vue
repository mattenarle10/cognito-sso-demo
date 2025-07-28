<template>
  <div v-if="isOpen" class="modal-backdrop" @click="$emit('close')">
    <div class="modal" @click.stop>
      <div class="modal-header">
        <h3>User Details</h3>
        <button class="close-button" @click="$emit('close')">&times;</button>
      </div>
      <div class="modal-body">
        <div class="user-details" v-if="user">
          <div class="detail-row">
            <strong>Username:</strong>
            <span>{{ user.username }}</span>
          </div>
          <div class="detail-row">
            <strong>Name:</strong>
            <span>{{ user.name || 'N/A' }}</span>
          </div>
          <div class="detail-row">
            <strong>Email:</strong>
            <span>{{ user.email }}</span>
          </div>
          <div class="detail-row">
            <strong>Phone:</strong>
            <span>{{ user.phone_number || 'N/A' }}</span>
          </div>
          <div class="detail-row">
            <strong>Status:</strong>
            <span>{{ user.status }}</span>
          </div>
          <div class="detail-row">
            <strong>Enabled:</strong>
            <span>{{ user.enabled ? 'Yes' : 'No' }}</span>
          </div>
          <div class="detail-row">
            <strong>Created:</strong>
            <span>{{ new Date(user.created_date).toLocaleString() }}</span>
          </div>
        </div>
      </div>
      <div class="modal-footer">
        <button class="btn-secondary" @click="$emit('close')">Close</button>
      </div>
    </div>
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
  isOpen: boolean;
  user: User | null;
}>();

defineEmits<{
  (e: 'close'): void
}>();
</script>
