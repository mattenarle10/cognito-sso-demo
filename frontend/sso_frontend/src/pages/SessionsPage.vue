<template>
  <AuthBackground>
    <AuthCard wide>
      <!-- Header -->
      <div class="mb-8 text-center">
        <h1 class="text-3xl font-bold tracking-tight mb-2">
          <span class="bg-gradient-to-r from-gray-200 via-gray-100 to-gray-300 bg-clip-text text-transparent">
            Active Sessions
          </span>
        </h1>
        <p class="text-zinc-500 text-sm">
          manage your active login sessions across devices
        </p>
      </div>

      <!-- Loading State -->
      <div v-if="loading" class="text-center py-8">
        <div class="inline-block w-8 h-8 border-2 border-zinc-600 border-t-zinc-300 rounded-full animate-spin"></div>
        <p class="mt-4 text-zinc-400">loading your sessions...</p>
      </div>

      <!-- Error State -->
      <div v-else-if="error" class="bg-red-500/10 border border-red-500/20 text-red-400 px-4 py-3 rounded-lg text-sm mb-6">
        {{ error }}
      </div>

      <!-- Empty State -->
      <div v-else-if="activeSessions.length === 0" class="text-center py-12">
        <div class="w-16 h-16 bg-zinc-800 rounded-full mx-auto mb-4 flex items-center justify-center">
          <svg class="w-8 h-8 text-zinc-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.75 17L9 20l-1 1h8l-1-1-.75-3M3 13h18M5 17h14a2 2 0 002-2V5a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"></path>
          </svg>
        </div>
        <h3 class="text-lg font-medium text-zinc-300 mb-2">no active sessions</h3>
        <p class="text-zinc-500 text-sm">you don't have any active sessions</p>
      </div>

      <!-- Sessions List -->
      <div v-else class="space-y-4 max-h-[500px] overflow-y-auto pr-2">
        <div 
          v-for="session in activeSessions" 
          :key="session.session_id"
          class="bg-zinc-900/60 border border-zinc-700/60 rounded-lg p-6 hover:bg-zinc-800/60 transition-all duration-200 shadow-sm hover:shadow-md"
          :class="{ 'border-green-500/30': session.is_current }"
        >
          <div class="flex items-start justify-between">
            <div class="flex-1">
              <div class="flex items-center gap-3 mb-2">
                <div class="w-12 h-12 bg-gradient-to-br from-zinc-800 to-zinc-900 border border-zinc-700/50 rounded-xl flex items-center justify-center shadow-inner">
                  <!-- Device icon based on device info -->
                  <svg v-if="session.device_info?.device?.toLowerCase().includes('mobile')" class="w-6 h-6 text-zinc-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 18h.01M8 21h8a2 2 0 002-2V5a2 2 0 00-2-2H8a2 2 0 00-2 2v14a2 2 0 002 2z"></path>
                  </svg>
                  <svg v-else-if="session.device_info?.device?.toLowerCase().includes('tablet')" class="w-6 h-6 text-zinc-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 18h.01M7 21h10a2 2 0 002-2V5a2 2 0 00-2-2H7a2 2 0 00-2 2v14a2 2 0 002 2z"></path>
                  </svg>
                  <svg v-else class="w-6 h-6 text-zinc-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.75 17L9 20l-1 1h8l-1-1-.75-3M3 13h18M5 17h14a2 2 0 002-2V5a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"></path>
                  </svg>
                </div>
                <div>
                  <h3 class="font-medium text-zinc-200 flex items-center gap-2">
                    {{ session.application_name || 'Unknown Application' }}
                    <span v-if="session.is_current" class="bg-green-500/20 text-green-400 text-xs px-2 py-0.5 rounded-full">current</span>
                  </h3>
                  <p class="text-sm text-zinc-400">
                    {{ formatDeviceInfo(session) }}
                  </p>
                  <p v-if="session.token_type" class="text-xs text-zinc-500 mt-1">
                    Token type: {{ session.token_type }}
                  </p>
                </div>
              </div>
              
              <div class="flex flex-wrap items-center gap-x-4 gap-y-2 text-xs text-zinc-500">
                <span class="flex items-center gap-1">
                  <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"></path>
                  </svg>
                  created: {{ formatDate(session.created_at) }}
                </span>
                <span class="flex items-center gap-1">
                  <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z"></path>
                  </svg>
                  expires: {{ formatDate(session.expires_at) }}
                </span>
                <span v-if="session.device_info?.ip_address" class="flex items-center gap-1">
                  <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 12a9 9 0 01-9 9m9-9a9 9 0 00-9-9m9 9H3m9 9a9 9 0 01-9-9m9 9c1.657 0 3-4.03 3-9s-1.343-9-3-9m0 18c-1.657 0-3-4.03-3-9s1.343-9 3-9m-9 9a9 9 0 019-9"></path>
                  </svg>
                  ip: {{ session.device_info.ip_address }}
                </span>
                <span v-if="session.session_id" class="flex items-center gap-1">
                  <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 7a2 2 0 012 2m4 0a6 6 0 01-7.743 5.743L11 17H9v2H7v2H4a1 1 0 01-1-1v-2.586a1 1 0 01.293-.707l5.964-5.964A6 6 0 1121 9z"></path>
                  </svg>
                  id: {{ session.session_id.substring(0, 8) }}...
                </span>
              </div>
            </div>

            <AuthButton
              v-if="!session.is_current"
              @click="handleRevoke(session.session_id)"
              :disabled="revokingId === session.session_id"
              size="sm"
              variant="danger"
              class="whitespace-nowrap"
            >
              <span v-if="revokingId === session.session_id" class="flex items-center gap-2">
                <span class="inline-block w-3 h-3 border-2 border-zinc-600 border-t-zinc-300 rounded-full animate-spin"></span>
                revoking...
              </span>
              <span v-else>revoke session</span>
            </AuthButton>
            <div v-else class="px-4 py-2 text-sm text-zinc-400">
              current session
            </div>
          </div>
        </div>
      </div>

      <!-- Back Button -->
      <div class="mt-8 pt-6 border-t border-zinc-800/50">
        <AuthButton 
          @click="goBack"
          class="!bg-transparent !border-zinc-700 !text-zinc-400 hover:!text-zinc-300 hover:!bg-zinc-800/50 !text-sm !px-4 !py-2"
        >
          <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18"></path>
          </svg>
          back to account
        </AuthButton>
      </div>
    </AuthCard>

    <!-- Confirmation Dialog -->
    <div v-if="showConfirmDialog" class="fixed inset-0 bg-black/70 backdrop-blur-sm flex items-center justify-center z-50">
      <div class="bg-zinc-900 border border-zinc-700 rounded-lg p-6 max-w-md w-full shadow-xl">
        <h3 class="text-xl font-medium text-zinc-200 mb-2">Revoke Session</h3>
        <p class="text-zinc-400 mb-6">
          Are you sure you want to revoke this session? This will immediately log out the device associated with this session.
        </p>
        
        <div class="flex gap-3">
          <AuthButton
            @click="confirmRevoke"
            :loading="loading"
            class="flex-1 !bg-red-600 hover:!bg-red-700 !text-white !py-2 !px-4"
          >
            <span v-if="loading">revoking...</span>
            <span v-else>revoke session</span>
          </AuthButton>
          <AuthButton
            @click="cancelRevoke"
            :disabled="loading"
            class="flex-1 !bg-zinc-700 hover:!bg-zinc-600 !text-zinc-300 !py-2 !px-4"
          >
            cancel
          </AuthButton>
        </div>
      </div>
    </div>
  </AuthBackground>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useApi } from '../composables/useApi'
import { useToast } from 'vue-toastification'
import AuthBackground from '../components/ui/AuthBackground.vue'
import AuthCard from '../components/ui/AuthCard.vue'
import AuthButton from '../components/ui/AuthButton.vue'
import type { UserSession } from '../types/api'

// composables
const router = useRouter()
const route = useRoute()
const api = useApi()
const toast = useToast()

// state
const activeSessions = ref<UserSession[]>([])
const expiredSessions = ref<UserSession[]>([])
const loading = ref(false)
const error = ref('')
const revokingId = ref<string | null>(null)
const showConfirmDialog = ref(false)
const sessionToRevoke = ref<string | null>(null)
const currentTokens = ref<any>(null)

// load user sessions
const loadSessions = async () => {
  loading.value = true
  error.value = ''
  
  try {
    // check if we have session_id in url params
    const sessionId = route.query.session_id as string
    
    if (sessionId) {
      // get session and tokens from sso backend
      const sessionData = await api.getSession(sessionId)
      if (sessionData && sessionData.tokens) {
        currentTokens.value = sessionData.tokens
      } else {
        error.value = 'failed to get session data - please try logging in again'
        return
      }
    } else {
      error.value = 'no session found - please access through your application'
      return
    }
    
    // get user sessions with proper tokens
    const result = await api.getUserSessions(currentTokens.value?.id_token)
    if (result) {
      console.log('Session data from API:', result)
      
      // Update to handle the new response format
      activeSessions.value = result.sessions.active || []
      expiredSessions.value = result.sessions.expired || []
      
      console.log('Active sessions:', activeSessions.value)
      
      // Mark current session
      const currentSessionId = route.query.session_id as string
      if (currentSessionId) {
        activeSessions.value = activeSessions.value.map(session => {
          if (session.session_id === currentSessionId) {
            return { ...session, is_current: true }
          }
          return session
        })
      }
    } else {
      error.value = api.error.value || 'failed to load sessions'
    }
  } catch (err: any) {
    console.error('Error loading sessions:', err)
    error.value = err.message || 'failed to load sessions'
  } finally {
    loading.value = false
  }
}

// handle revoke button click
const handleRevoke = (sessionId: string) => {
  sessionToRevoke.value = sessionId
  showConfirmDialog.value = true
}

// confirm revocation
const confirmRevoke = async () => {
  if (!sessionToRevoke.value) return
  
  loading.value = true
  revokingId.value = sessionToRevoke.value
  
  try {
    console.log('Revoking session ID:', sessionToRevoke.value)
    console.log('Using token:', currentTokens.value?.id_token)
    
    const success = await api.revokeUserSession(sessionToRevoke.value, currentTokens.value?.id_token)
    
    if (success) {
      console.log('Successfully revoked session')
      // remove from local list
      activeSessions.value = activeSessions.value.filter(
        session => session.session_id !== sessionToRevoke.value
      )
      
      toast.success('Session revoked successfully')
      showConfirmDialog.value = false
      sessionToRevoke.value = null
    } else {
      console.error('Failed to revoke session:', api.error.value)
      error.value = api.error.value || 'failed to revoke session'
    }
  } catch (err: any) {
    console.error('Error in revoke session:', err)
    error.value = err.message || 'failed to revoke session'
  } finally {
    loading.value = false
    revokingId.value = null
  }
}

// cancel revocation
const cancelRevoke = () => {
  showConfirmDialog.value = false
  sessionToRevoke.value = null
}

// format date
const formatDate = (dateString: string | undefined) => {
  if (!dateString) return 'unknown'
  
  try {
    const date = new Date(dateString)
    return date.toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    })
  } catch {
    return 'unknown'
  }
}

// format device info
const formatDeviceInfo = (session: UserSession) => {
  const info = session.device_info
  if (!info) return 'Unknown device'
  
  const parts = []
  if (info.browser) parts.push(info.browser)
  if (info.os) parts.push(info.os)
  if (info.device) parts.push(info.device)
  
  // If we don't have any device info, show session ID as a fallback
  if (parts.length === 0 && session.session_id) {
    return `Session ID: ${session.session_id.substring(0, 8)}...`
  }
  
  return parts.join(' • ') || 'Unknown device'
}

// go back to manage account page
const goBack = () => {
  const sessionId = route.query.session_id as string
  if (sessionId) {
    router.push(`/manage-account?session_id=${sessionId}`)
  } else {
    router.push('/manage-account')
  }
}

// load data on mount
onMounted(() => {
  loadSessions()
})
</script>
