<template>
  <div class="consent-overlay">
    <div class="consent-modal">
      <div class="consent-header">
        <div class="app-info">
          <div class="app-icon">
            <i class="icon-app"></i>
          </div>
          <div class="app-details">
            <h2>{{ applicationName }}</h2>
            <p class="app-subtitle">wants to access your account</p>
          </div>
        </div>
      </div>

      <div class="consent-body">
        <div class="permission-notice">
          <p><strong>{{ applicationName }}</strong> is requesting permission to:</p>
        </div>

        <div class="permissions-list">
          <div 
            v-for="scope in availableScopes" 
            :key="scope.id"
            class="permission-item"
          >
            <label class="permission-checkbox">
              <input 
                type="checkbox" 
                :value="scope.id"
                v-model="selectedScopes"
                :checked="scope.required"
                :disabled="scope.required"
              />
              <span class="checkmark"></span>
              <div class="permission-details">
                <span class="permission-name">{{ scope.name }}</span>
                <span class="permission-description">{{ scope.description }}</span>
                <span v-if="scope.required" class="required-badge">Required</span>
              </div>
            </label>
          </div>
        </div>

        <div class="security-notice">
          <div class="security-icon">
            <i class="icon-shield"></i>
          </div>
          <div class="security-text">
            <p>You can revoke these permissions at any time in your account settings.</p>
          </div>
        </div>
      </div>

      <div class="consent-footer">
        <button 
          class="btn btn-secondary" 
          @click="denyConsent"
          :disabled="loading"
        >
          Cancel
        </button>
        <button 
          class="btn btn-primary" 
          @click="approveConsent"
          :disabled="loading || selectedScopes.length === 0"
        >
          <span v-if="loading">Processing...</span>
          <span v-else>Allow Access</span>
        </button>
      </div>

      <div v-if="error" class="error-message">
        {{ error }}
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useApi } from '../composables/useApi'

// Props
interface Props {
  applicationId: string
  applicationName: string
  redirectUrl?: string
}

const props = defineProps<Props>()

// Emits
const emit = defineEmits<{
  approved: [scopes: string[]]
  denied: []
  error: [message: string]
}>()

// Services
const api = useApi()

// State
const loading = ref(false)
const error = ref('')
const selectedScopes = ref<string[]>([])

// Available scopes for the application
const availableScopes = ref([
  {
    id: 'profile',
    name: 'Basic profile information',
    description: 'Access your name and profile picture',
    required: true
  },
  {
    id: 'email',
    name: 'Email address',
    description: 'Access your email address',
    required: true
  },
  {
    id: 'orders',
    name: 'Order history',
    description: 'Access your order history and preferences',
    required: false
  }
])

// Computed
const requiredScopes = computed(() => 
  availableScopes.value.filter(scope => scope.required).map(scope => scope.id)
)

// Methods
const approveConsent = async () => {
  loading.value = true
  error.value = ''

  try {
    // Include all required scopes plus selected optional ones
    const scopesToGrant = [...new Set([...requiredScopes.value, ...selectedScopes.value])]
    
    const response = await api.authorizeApplication({
      application_id: props.applicationId,
      granted_scopes: scopesToGrant,
      action: 'approve'
    })

    if (response.status === 'approved') {
      emit('approved', scopesToGrant)
    } else {
      throw new Error('Authorization failed')
    }
  } catch (err: any) {
    error.value = err.message || 'Failed to authorize application'
    emit('error', error.value)
  } finally {
    loading.value = false
  }
}

const denyConsent = async () => {
  loading.value = true
  error.value = ''

  try {
    await api.authorizeApplication({
      application_id: props.applicationId,
      granted_scopes: [],
      action: 'deny'
    })

    emit('denied')
  } catch (err: any) {
    // Even if the API call fails, we still deny consent
    emit('denied')
  } finally {
    loading.value = false
  }
}

// Initialize selected scopes with required ones
onMounted(() => {
  selectedScopes.value = [...requiredScopes.value]
})
</script>

<style scoped>
.consent-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.consent-modal {
  background: white;
  border-radius: 12px;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
  max-width: 480px;
  width: 90%;
  max-height: 90vh;
  overflow-y: auto;
}

.consent-header {
  padding: 24px 24px 16px;
  border-bottom: 1px solid #e5e7eb;
}

.app-info {
  display: flex;
  align-items: center;
  gap: 16px;
}

.app-icon {
  width: 48px;
  height: 48px;
  background: #3b82f6;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 24px;
}

.app-details h2 {
  margin: 0;
  font-size: 20px;
  font-weight: 600;
  color: #111827;
}

.app-subtitle {
  margin: 4px 0 0;
  color: #6b7280;
  font-size: 14px;
}

.consent-body {
  padding: 24px;
}

.permission-notice {
  margin-bottom: 24px;
}

.permission-notice p {
  margin: 0;
  color: #374151;
  font-size: 16px;
}

.permissions-list {
  margin-bottom: 24px;
}

.permission-item {
  margin-bottom: 16px;
}

.permission-checkbox {
  display: flex;
  align-items: flex-start;
  gap: 12px;
  cursor: pointer;
  padding: 12px;
  border-radius: 8px;
  transition: background-color 0.2s;
}

.permission-checkbox:hover {
  background: #f9fafb;
}

.permission-checkbox input[type="checkbox"] {
  display: none;
}

.checkmark {
  width: 20px;
  height: 20px;
  border: 2px solid #d1d5db;
  border-radius: 4px;
  position: relative;
  flex-shrink: 0;
  margin-top: 2px;
  transition: all 0.2s;
}

.permission-checkbox input:checked + .checkmark {
  background: #3b82f6;
  border-color: #3b82f6;
}

.permission-checkbox input:checked + .checkmark::after {
  content: '✓';
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  color: white;
  font-size: 12px;
  font-weight: bold;
}

.permission-checkbox input:disabled + .checkmark {
  background: #3b82f6;
  border-color: #3b82f6;
  opacity: 0.7;
}

.permission-details {
  flex: 1;
}

.permission-name {
  display: block;
  font-weight: 500;
  color: #111827;
  margin-bottom: 4px;
}

.permission-description {
  display: block;
  font-size: 14px;
  color: #6b7280;
  margin-bottom: 4px;
}

.required-badge {
  display: inline-block;
  background: #fef3c7;
  color: #92400e;
  font-size: 12px;
  font-weight: 500;
  padding: 2px 8px;
  border-radius: 12px;
}

.security-notice {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 16px;
  background: #f0f9ff;
  border: 1px solid #e0f2fe;
  border-radius: 8px;
}

.security-icon {
  color: #0369a1;
  font-size: 20px;
}

.security-text p {
  margin: 0;
  font-size: 14px;
  color: #0369a1;
}

.consent-footer {
  padding: 16px 24px 24px;
  display: flex;
  gap: 12px;
  justify-content: flex-end;
}

.btn {
  padding: 12px 24px;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
  border: none;
}

.btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.btn-secondary {
  background: #f3f4f6;
  color: #374151;
}

.btn-secondary:hover:not(:disabled) {
  background: #e5e7eb;
}

.btn-primary {
  background: #3b82f6;
  color: white;
}

.btn-primary:hover:not(:disabled) {
  background: #2563eb;
}

.error-message {
  margin: 16px 24px 0;
  padding: 12px;
  background: #fef2f2;
  border: 1px solid #fecaca;
  border-radius: 8px;
  color: #dc2626;
  font-size: 14px;
}

.icon-app::before {
  content: '📱';
}

.icon-shield::before {
  content: '🛡️';
}
</style> 