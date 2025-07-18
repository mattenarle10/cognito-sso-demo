<template>
  <AuthBackground>
    <AuthCard wide>
      <!-- Header -->
      <div class="mb-8 text-center">
        <h1 class="text-3xl font-bold tracking-tight mb-2">
          <span class="bg-gradient-to-r from-gray-200 via-gray-100 to-gray-300 bg-clip-text text-transparent">
            App Authorizations
          </span>
        </h1>
        <p class="text-zinc-500 text-sm">
          manage applications that have access to your account
        </p>
      </div>

      <!-- Loading State -->
      <div v-if="loading" class="text-center py-8">
        <div class="inline-block w-8 h-8 border-2 border-zinc-600 border-t-zinc-300 rounded-full animate-spin"></div>
        <p class="mt-4 text-zinc-400">loading your authorizations...</p>
      </div>

      <!-- Error State -->
      <div v-else-if="error" class="bg-red-500/10 border border-red-500/20 text-red-400 px-4 py-3 rounded-lg text-sm mb-6">
        {{ error }}
      </div>

      <!-- Empty State -->
      <div v-else-if="authorizations.length === 0" class="text-center py-12">
        <div class="w-16 h-16 bg-zinc-800 rounded-full mx-auto mb-4 flex items-center justify-center">
          <svg class="w-8 h-8 text-zinc-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10"></path>
          </svg>
        </div>
        <h3 class="text-lg font-medium text-zinc-300 mb-2">no authorized applications</h3>
        <p class="text-zinc-500 text-sm">you haven't authorized any applications yet</p>
      </div>

      <!-- Authorizations List -->
      <div v-else class="space-y-4">
        <div 
          v-for="auth in authorizations" 
          :key="auth.application_id"
          class="bg-zinc-800/30 border border-zinc-700/50 rounded-lg p-6 hover:bg-zinc-800/50 transition-colors"
        >
          <div class="flex items-start justify-between">
            <div class="flex-1">
              <div class="flex items-center gap-3 mb-2">
                <div class="w-10 h-10 bg-gradient-to-br from-zinc-700 to-zinc-800 rounded-lg flex items-center justify-center">
                  <svg class="w-5 h-5 text-zinc-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.75 17L9 20l-1 1h8l-1-1-.75-3M3 13h18M5 17h14a2 2 0 002-2V5a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"></path>
                  </svg>
                </div>
                <div>
                  <h3 class="font-medium text-zinc-200">{{ auth.application_name }}</h3>
                  <p class="text-sm text-zinc-400">{{ auth.application_description || 'no description available' }}</p>
                </div>
              </div>
              
              <div class="flex items-center gap-4 text-xs text-zinc-500">
                <span>authorized: {{ formatDate(auth.created_at) }}</span>
                <span class="flex items-center gap-1">
                  <div class="w-2 h-2 bg-green-500 rounded-full"></div>
                  active
                </span>
              </div>
            </div>

            <button
              @click="handleRevoke(auth.application_id, auth.application_name)"
              :disabled="revokingId === auth.application_id"
              class="px-4 py-2 text-sm bg-red-600/20 hover:bg-red-600/30 text-red-400 border border-red-600/30 rounded-lg transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
            >
              <span v-if="revokingId === auth.application_id">revoking...</span>
              <span v-else>revoke access</span>
            </button>
          </div>
        </div>
      </div>

      <!-- Back Button -->
      <div class="mt-8 pt-6 border-t border-zinc-800/50">
        <button 
          @click="goBack"
          class="text-zinc-400 hover:text-zinc-300 text-sm transition-colors flex items-center gap-2"
        >
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18"></path>
          </svg>
          back to profile
        </button>
      </div>
    </AuthCard>

    <!-- Confirmation Dialog -->
    <div v-if="showConfirmDialog" class="fixed inset-0 bg-black/60 flex items-center justify-center z-50">
      <div class="bg-zinc-900 border border-zinc-700 rounded-lg p-6 max-w-md w-full mx-4">
        <h3 class="text-lg font-medium text-zinc-200 mb-2">revoke authorization?</h3>
        <p class="text-zinc-400 text-sm mb-6">
          this will remove <strong>{{ appToRevoke?.name }}</strong> access to your account. 
          you'll need to re-authorize if you want to use this app again.
        </p>
        
        <div class="flex gap-3">
          <button
            @click="confirmRevoke"
            :disabled="loading"
            class="flex-1 bg-red-600 hover:bg-red-700 text-white py-2 px-4 rounded-lg transition-colors disabled:opacity-50"
          >
            <span v-if="loading">revoking...</span>
            <span v-else>revoke access</span>
          </button>
          <button
            @click="cancelRevoke"
            :disabled="loading"
            class="flex-1 bg-zinc-700 hover:bg-zinc-600 text-zinc-300 py-2 px-4 rounded-lg transition-colors disabled:opacity-50"
          >
            cancel
          </button>
        </div>
      </div>
    </div>
  </AuthBackground>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useApi } from '../composables/useApi'
import { useToast } from 'vue-toastification'
import AuthBackground from '../components/ui/AuthBackground.vue'
import AuthCard from '../components/ui/AuthCard.vue'

// composables
const router = useRouter()
const api = useApi()
const toast = useToast()

// state
const authorizations = ref<any[]>([])
const loading = ref(false)
const error = ref('')
const revokingId = ref<string | null>(null)
const showConfirmDialog = ref(false)
const appToRevoke = ref<{ id: string; name: string } | null>(null)

// load user authorizations
const loadAuthorizations = async () => {
  loading.value = true
  error.value = ''
  
  try {
    const result = await api.getUserAuthorizations()
    if (result) {
      authorizations.value = result.authorizations
    } else {
      error.value = api.error.value || 'failed to load authorizations'
    }
  } catch (err: any) {
    error.value = err.message || 'failed to load authorizations'
  } finally {
    loading.value = false
  }
}

// handle revoke button click
const handleRevoke = (applicationId: string, applicationName: string) => {
  appToRevoke.value = { id: applicationId, name: applicationName }
  showConfirmDialog.value = true
}

// confirm revocation
const confirmRevoke = async () => {
  if (!appToRevoke.value) return
  
  loading.value = true
  revokingId.value = appToRevoke.value.id
  
  try {
    const success = await api.revokeAuthorization(appToRevoke.value.id)
    
    if (success) {
      // remove from local list
      authorizations.value = authorizations.value.filter(
        auth => auth.application_id !== appToRevoke.value?.id
      )
      
      toast.success(`access revoked for ${appToRevoke.value.name}`)
      showConfirmDialog.value = false
      appToRevoke.value = null
    } else {
      error.value = api.error.value || 'failed to revoke authorization'
    }
  } catch (err: any) {
    error.value = err.message || 'failed to revoke authorization'
  } finally {
    loading.value = false
    revokingId.value = null
  }
}

// cancel revocation
const cancelRevoke = () => {
  showConfirmDialog.value = false
  appToRevoke.value = null
}

// format date
const formatDate = (dateString: string) => {
  if (!dateString) return 'unknown'
  
  try {
    const date = new Date(dateString)
    return date.toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric'
    })
  } catch {
    return 'unknown'
  }
}

// go back to profile (or wherever user came from)
const goBack = () => {
  router.back()
}

// load data on mount
onMounted(() => {
  loadAuthorizations()
})
</script> 