<template>
  <div v-if="isOpen" class="modal-backdrop" @click="$emit('cancel')">
    <div class="modal" @click.stop>
      <div class="modal-header">
        <h3><i class="fas fa-user-edit"></i> Edit User Name</h3>
        <button class="close-button" @click="$emit('cancel')">&times;</button>
      </div>
      <div class="modal-body">
        <form @submit.prevent="handleSubmit">
          <div class="form-group">
            <label for="firstName">First Name</label>
            <input 
              type="text" 
              id="firstName" 
              v-model="firstName" 
              class="form-input"
              placeholder="First Name"
              required
            />
          </div>
          <div class="form-group">
            <label for="lastName">Last Name</label>
            <input 
              type="text" 
              id="lastName" 
              v-model="lastName" 
              class="form-input"
              placeholder="Last Name"
              required
            />
          </div>
          <div class="error-message" v-if="error">{{ error }}</div>
        </form>
      </div>
      <div class="modal-footer">
        <button 
          class="btn-primary" 
          @click="handleSubmit" 
          :disabled="loading || !isValid"
        >
          <span v-if="loading" class="spinner-small"></span>
          {{ loading ? 'Saving...' : 'Save Changes' }}
        </button>
        <button 
          class="btn-secondary" 
          @click="$emit('cancel')" 
          :disabled="loading"
        >
          Cancel
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, watch } from 'vue';
import { UserService } from '../services/UserService';

const props = defineProps<{
  isOpen: boolean;
  user: {
    username: string;
    attributes?: {
      name?: string;
      given_name?: string;
      family_name?: string;
      [key: string]: string | undefined;
    };
  } | null;
}>();

const emit = defineEmits<{
  (e: 'cancel'): void;
  (e: 'saved'): void;
}>();

const firstName = ref('');
const lastName = ref('');
const loading = ref(false);
const error = ref('');

// Watch for user changes to update the form
watch(() => props.user, (newUser) => {
  if (newUser?.attributes) {
    // Try to get first and last name from different possible sources
    if (newUser.attributes.given_name && newUser.attributes.family_name) {
      // If we have separate given_name and family_name fields
      firstName.value = newUser.attributes.given_name;
      lastName.value = newUser.attributes.family_name;
    } else if (newUser.attributes.name) {
      // If we have a combined name field, split it
      const nameParts = newUser.attributes.name.split(' ');
      firstName.value = nameParts[0] || '';
      lastName.value = nameParts.slice(1).join(' ') || '';
    } else {
      // Default to empty
      firstName.value = '';
      lastName.value = '';
    }
  }
}, { immediate: true });

const isValid = computed(() => {
  return firstName.value.trim() !== '' && lastName.value.trim() !== '';
});

const handleSubmit = async () => {
  if (!isValid.value || !props.user) return;
  
  loading.value = true;
  error.value = '';
  
  try {
    const fullName = `${firstName.value.trim()} ${lastName.value.trim()}`;
    
    await UserService.updateUser(props.user.username, {
      name: fullName,
      given_name: firstName.value.trim(),
      family_name: lastName.value.trim()
    });
    
    emit('saved');
  } catch (err: any) {
    console.error('Error updating user name:', err);
    error.value = err.message || 'Failed to update user name';
  } finally {
    loading.value = false;
  }
};
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
  max-width: 450px;
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
}

.form-group {
  margin-bottom: 1rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 500;
  color: #333;
}

.form-input {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 1rem;
  transition: border-color 0.2s;
}

.form-input:focus {
  border-color: #0077cc;
  outline: none;
  box-shadow: 0 0 0 2px rgba(0, 119, 204, 0.1);
}

.error-message {
  color: #e03131;
  font-size: 0.875rem;
  margin-top: 0.5rem;
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
  display: flex;
  align-items: center;
}

.btn-primary:hover:not(:disabled) {
  background-color: #0066b3;
}

.btn-secondary {
  padding: 0.5rem 1.25rem;
  background-color: #f1f3f5;
  color: #495057;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-weight: 500;
  transition: background-color 0.2s;
}

.btn-secondary:hover:not(:disabled) {
  background-color: #e9ecef;
}

.btn-primary:disabled, .btn-secondary:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.spinner-small {
  width: 16px;
  height: 16px;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-radius: 50%;
  border-top-color: #ffffff;
  animation: spin 1s ease-in-out infinite;
  display: inline-block;
  margin-right: 0.5rem;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}
</style>
