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
            <span>{{ user.attributes?.name || 'N/A' }}</span>
          </div>
          <div class="detail-row">
            <strong>Email:</strong>
            <span>{{ user.attributes?.email || 'N/A' }}</span>
          </div>
          <div class="detail-row">
            <strong>Phone:</strong>
            <span>{{ user.attributes?.phone_number || 'N/A' }}</span>
          </div>
          <div class="detail-row">
            <strong>Status:</strong>
            <span>{{ user.user_status }}</span>
          </div>
          <div class="detail-row">
            <strong>Enabled:</strong>
            <span>{{ user.enabled ? 'Yes' : 'No' }}</span>
          </div>
          <div class="detail-row">
            <strong>Created:</strong>
            <span>{{ new Date(user.user_create_date).toLocaleString() }}</span>
          </div>
          <div class="detail-row">
            <strong>Last Modified:</strong>
            <span>{{ new Date(user.user_last_modified_date).toLocaleString() }}</span>
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
  isOpen: boolean;
  user: User | null;
}>();

defineEmits<{
  (e: 'close'): void
}>();
</script>

<style scoped>
.modal-backdrop {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 100;
}

.modal {
  background-color: white;
  border-radius: 8px;
  width: 90%;
  max-width: 500px;
  max-height: 90vh;
  overflow-y: auto;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  display: flex;
  flex-direction: column;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem 1.5rem;
  border-bottom: 1px solid #eee;
}

.modal-header h3 {
  margin: 0;
  font-size: 1.25rem;
  color: #333;
}

.close-button {
  background: none;
  border: none;
  font-size: 1.5rem;
  cursor: pointer;
  color: #666;
  padding: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 2rem;
  height: 2rem;
  border-radius: 50%;
  transition: background-color 0.2s;
}

.close-button:hover {
  background-color: #f5f5f5;
}

.modal-body {
  padding: 1.5rem;
  overflow-y: auto;
}

.user-details {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.detail-row {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

@media (min-width: 640px) {
  .detail-row {
    flex-direction: row;
    align-items: center;
  }
  
  .detail-row strong {
    width: 120px;
    flex-shrink: 0;
  }
}

.detail-row strong {
  font-weight: 600;
  color: #555;
}

.detail-row span {
  color: #333;
}

.modal-footer {
  padding: 1rem 1.5rem;
  border-top: 1px solid #eee;
  display: flex;
  justify-content: flex-end;
  gap: 0.75rem;
}
</style>
