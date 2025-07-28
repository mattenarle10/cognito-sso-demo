<template>
  <div v-if="isOpen" class="modal-backdrop" @click="$emit('close')">
    <div class="modal" @click.stop>
      <div class="modal-header">
        <h3><i class="fas fa-user-circle"></i> User Details</h3>
        <button class="close-button" @click="$emit('close')">&times;</button>
      </div>
      <div class="modal-body">
        <div class="user-details" v-if="user">
          <div class="user-header">
            <div class="user-avatar">
              <i class="fas fa-user"></i>
            </div>
            <div class="user-name">
              {{ user.attributes?.name || user.username || 'N/A' }}
            </div>
            <div class="user-status" :class="{ 'status-active': user.enabled, 'status-disabled': !user.enabled }">
              {{ user.enabled ? 'Active' : 'Disabled' }}
            </div>
          </div>
          
          <div class="detail-section">
            <h4><i class="fas fa-id-card"></i> Basic Information</h4>
            <div class="detail-row">
              <strong>Username:</strong>
              <span>{{ user.username || 'N/A' }}</span>
            </div>
            <div class="detail-row">
              <strong>Email:</strong>
              <span>{{ user.attributes?.email || 'N/A' }}</span>
            </div>
            <div class="detail-row">
              <strong>Phone:</strong>
              <span>{{ user.attributes?.phone_number || 'N/A' }}</span>
            </div>
          </div>
          
          <div class="detail-section">
            <h4><i class="fas fa-info-circle"></i> Status Information</h4>
            <div class="detail-row">
              <strong>Status:</strong>
              <span class="status-badge">{{ user.user_status || 'N/A' }}</span>
            </div>
            <div class="detail-row">
              <strong>Enabled:</strong>
              <span>{{ user.enabled ? 'Yes' : 'No' }}</span>
            </div>
          </div>
          
          <div class="detail-section">
            <h4><i class="fas fa-calendar-alt"></i> Dates</h4>
            <div class="detail-row">
              <strong>Created:</strong>
              <span>{{ user.user_create_date ? new Date(user.user_create_date).toLocaleString() : 'N/A' }}</span>
            </div>
            <div class="detail-row">
              <strong>Last Modified:</strong>
              <span>{{ user.user_last_modified_date ? new Date(user.user_last_modified_date).toLocaleString() : 'N/A' }}</span>
            </div>
          </div>
          
          <div class="detail-section" v-if="hasCustomAttributes">
            <h4><i class="fas fa-cog"></i> Custom Attributes</h4>
            <div class="detail-row" v-for="(value, key) in customAttributes" :key="key">
              <strong>{{ formatAttributeName(key) }}:</strong>
              <span>{{ value }}</span>
            </div>
          </div>
        </div>
      </div>
      <div class="modal-footer">
        <button class="btn-primary" @click="$emit('close')">Close</button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue';

const props = defineProps<{
  isOpen: boolean;
  user: User | null;
}>();

interface User {
  username: string;
  attributes?: {
    name?: string;
    email?: string;
    phone_number?: string;
    [key: string]: string | undefined;
  };
  user_status: string;
  enabled: boolean;
  user_create_date: string;
  user_last_modified_date: string;
}

const hasCustomAttributes = computed(() => {
  if (!props.user?.attributes) return false;
  
  const standardAttrs = ['name', 'email', 'phone_number', 'sub'];
  return Object.keys(props.user.attributes).some(key => 
    !standardAttrs.includes(key) && key.startsWith('custom:'));
});

const customAttributes = computed(() => {
  if (!props.user?.attributes) return {};
  
  const standardAttrs = ['name', 'email', 'phone_number', 'sub'];
  const custom: Record<string, string> = {};
  
  Object.entries(props.user.attributes).forEach(([key, value]) => {
    if (!standardAttrs.includes(key) && value !== undefined) {
      custom[key] = value;
    }
  });
  
  return custom;
});

const formatAttributeName = (key: string) => {
  // Remove 'custom:' prefix if present
  const name = key.startsWith('custom:') ? key.substring(7) : key;
  
  // Convert snake_case to Title Case
  return name
    .split('_')
    .map(word => word.charAt(0).toUpperCase() + word.slice(1))
    .join(' ');
};

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
  display: flex;
  align-items: center;
  gap: 0.5rem;
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
  gap: 1.25rem;
}

.user-header {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.75rem;
  padding-bottom: 1.25rem;
  border-bottom: 1px solid #eee;
}

.user-avatar {
  width: 80px;
  height: 80px;
  border-radius: 50%;
  background-color: #f0f0f0;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 2.5rem;
  color: #666;
}

.user-name {
  font-size: 1.25rem;
  font-weight: 600;
  color: #333;
}

.user-status {
  padding: 0.25rem 0.75rem;
  border-radius: 12px;
  font-size: 0.875rem;
  font-weight: 500;
}

.status-active {
  background-color: rgba(0, 128, 0, 0.1);
  color: green;
}

.status-disabled {
  background-color: rgba(128, 128, 128, 0.1);
  color: #666;
}

.detail-section {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.detail-section h4 {
  margin: 0;
  font-size: 1rem;
  color: #333;
  padding-bottom: 0.5rem;
  border-bottom: 1px solid #eee;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.detail-section h4 i {
  color: #666;
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

.status-badge {
  display: inline-block;
  padding: 0.25rem 0.5rem;
  border-radius: 12px;
  font-size: 0.8rem;
  font-weight: 500;
  background-color: #f0f0f0;
  color: #333;
}

.modal-footer {
  padding: 1rem 1.5rem;
  border-top: 1px solid #eee;
  display: flex;
  justify-content: flex-end;
  gap: 0.75rem;
}

.btn-primary {
  padding: 0.5rem 1.25rem;
  background-color: #0077cc;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-weight: 500;
  transition: background-color 0.2s;
}

.btn-primary:hover {
  background-color: #0066b3;
}
</style>
