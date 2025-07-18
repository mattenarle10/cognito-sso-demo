<template>
  <div class="fixed inset-0 bg-black/70 backdrop-blur-sm flex items-center justify-center z-50">
    <AuthCard>
        <!-- Header -->
        <div class="text-center mb-8">
          <div class="w-16 h-16 bg-gradient-to-br from-zinc-800 to-zinc-900 border border-zinc-700/50 rounded-xl mx-auto mb-4 flex items-center justify-center shadow-inner">
            <svg class="w-8 h-8 text-zinc-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.75 17L9 20l-1 1h8l-1-1-.75-3M3 13h18M5 17h14a2 2 0 002-2V5a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"></path>
            </svg>
          </div>
          
          <h1 class="text-2xl font-bold tracking-tight mb-2">
            <span class="bg-gradient-to-r from-gray-200 via-gray-100 to-gray-300 bg-clip-text text-transparent">
              authorize access
            </span>
          </h1>
          
          <p class="text-zinc-400 text-sm">
            allow <strong class="text-zinc-300">The Grind</strong> to access your grind account
          </p>
        </div>

        <!-- Simple Permission Notice -->
        <div class="bg-zinc-900/60 border border-zinc-700/60 rounded-lg p-6 mb-6">
          <div class="flex items-start gap-4">
            <div class="w-8 h-8 bg-blue-600/20 border border-blue-600/30 rounded-lg flex items-center justify-center mt-1">
              <svg class="w-4 h-4 text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
              </svg>
            </div>
            <div class="flex-1">
              <h3 class="font-medium text-zinc-200 mb-2">Authorize App Access</h3>
              <p class="text-zinc-400 text-sm leading-relaxed">
                this allows access your profile, email, and account information to provide you with personalized service.
              </p>
            </div>
          </div>
        </div>

        <!-- Security Notice -->
        <div class="bg-zinc-800/30 border border-zinc-700/50 rounded-lg p-4 mb-8">
          <div class="flex items-center gap-3">
            <svg class="w-5 h-5 text-zinc-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z"></path>
            </svg>
            <p class="text-zinc-400 text-sm">
              you can revoke this access anytime in your account settings
            </p>
          </div>
        </div>

        <!-- Error Display -->
        <div v-if="error" class="bg-red-500/10 border border-red-500/20 text-red-400 px-4 py-3 rounded-lg text-sm mb-6">
          {{ error }}
        </div>

        <!-- Action Buttons -->
        <div class="flex gap-3">
          <AuthButton
            @click="denyConsent"
            :disabled="loading"
            class="flex-1 !bg-transparent !border-zinc-700 !text-zinc-400 hover:!text-zinc-300 hover:!bg-zinc-800/50"
          >
            cancel
          </AuthButton>
          
          <AuthButton
            @click="approveConsent"
            :disabled="loading"
            :loading="loading"
            class="flex-1"
          >
            <span v-if="loading">authorizing...</span>
            <span v-else">allow access</span>
          </AuthButton>
        </div>
             </AuthCard>
     </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useApi } from '../composables/useApi'
import AuthCard from './ui/AuthCard.vue'
import AuthButton from './ui/AuthButton.vue'

// Props
interface Props {
  applicationId: string
  applicationName: string
  redirectUrl?: string
  idToken?: string
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

// Methods
const approveConsent = async () => {
  loading.value = true
  error.value = ''

  try {
    // Simple authorization - just basic access
    const response = await api.authorizeApplication({
      application_id: props.applicationId,
      granted_scopes: ['profile', 'email'],
      action: 'approve'
    }, props.idToken)

    if (response && response.status === 'approved') {
      emit('approved', ['profile', 'email'])
    } else {
      throw new Error('authorization failed')
    }
  } catch (err: any) {
    error.value = err.message || 'failed to authorize application'
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
</script>

 