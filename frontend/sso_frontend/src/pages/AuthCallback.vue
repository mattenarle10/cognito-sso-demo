<template>
  <AuthBackground>
    <AuthCard>
      <div class="text-center mb-8">
        <h1 class="text-3xl font-bold mb-2 bg-gradient-to-r from-gray-200 via-gray-100 to-gray-300 bg-clip-text text-transparent">The Grind.</h1>
        <p class="text-zinc-500">Signing in with Google...</p>
      </div>
      
      <div v-if="loading" class="flex flex-col items-center gap-4 py-8">
        <span class="loader" />
        <span class="text-zinc-400">Processing your login...</span>
      </div>
      
      <div v-else-if="error" class="bg-red-500/10 border border-red-500/20 text-red-400 px-4 py-3 rounded-lg text-sm">
        <p class="mb-2">{{ error }}</p>
        <div class="mt-4 text-center">
          <router-link to="/login" class="text-zinc-200 hover:text-white underline underline-offset-2">
            Go back to login
          </router-link>
        </div>
      </div>
    </AuthCard>
    
    <!-- Consent Screen Modal -->
    <ConsentScreen
      v-if="showConsentScreen"
      :applicationId="appName"
      :applicationName="appName"
      :idToken="tokens?.id_token"
      @approved="handleConsentApproved"
      @denied="handleConsentDenied"
      @error="handleConsentError"
    />
  </AuthBackground>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import axios from 'axios'
import { useToast } from 'vue-toastification'
import { useApi } from '../composables/useApi'
import AuthBackground from '../components/ui/AuthBackground.vue'
import AuthCard from '../components/ui/AuthCard.vue'
import ConsentScreen from '../components/ConsentScreen.vue'

const loading = ref(true)
const error = ref('')
const route = useRoute()
const router = useRouter()
const toast = useToast()
const api = useApi()

// State for consent screen
const showConsentScreen = ref(false)
const tokens = ref<any>(null)

// Get application info from query params or defaults
const appName = ref(route.query.application_name as string || import.meta.env.VITE_DEFAULT_APPLICATION_NAME)
const channelId = ref(route.query.channel_id as string || import.meta.env.VITE_DEFAULT_CHANNEL_ID)

// Cognito OAuth config
const cognitoDomain = import.meta.env.VITE_COGNITO_DOMAIN
const clientId = import.meta.env.VITE_COGNITO_CLIENT_ID
const redirectUri = `${window.location.origin}/auth/callback`

onMounted(async () => {
  // Check for error parameters from Cognito
  if (route.query.error) {
    const errorDesc = route.query.error_description as string || ''
    
    // Check specifically for the 'attributes required' error
    if (errorDesc.includes('attributes required')) {
      // Extract required attributes from error message
      const requiredAttributes = errorDesc.match(/\[(.*?)\]/)?.[1].split(',').map((attr: string) => attr.trim()) || []
      
      // Redirect to complete profile with required attributes
      router.replace({ 
        name: 'CompleteProfile',
        query: {
          required_attributes: requiredAttributes.join(','),
          application_name: appName.value,
          channel_id: channelId.value,
          redirect_url: route.query.redirect_url as string
        }
      })
      return
    } else {
      // Handle other errors
      error.value = `Authentication error: ${route.query.error_description}`
      loading.value = false
      return
    }
  }
  
  const code = route.query.code
  if (!code) {
    error.value = 'Missing authorization code from Google login.'
    loading.value = false
    return
  }
  
  try {
    // Exchange code for tokens
    const params = new URLSearchParams()
    params.append('grant_type', 'authorization_code')
    params.append('client_id', clientId)
    params.append('code', code as string)
    params.append('redirect_uri', redirectUri)

    const resp = await axios.post(
      `${cognitoDomain}/oauth2/token`,
      params,
      {
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
      }
    )
    
    // Store tokens from the response
    const { access_token, id_token, refresh_token } = resp.data
    tokens.value = { access_token, id_token, refresh_token }
    
    // Check if user is authorized for this application
    const authCheck = await api.checkAppUser(id_token, appName.value)
    
    if (!authCheck) {
      // User needs to authorize this application - show consent screen
      showConsentScreen.value = true
      loading.value = false
      return
    }
    
    // User is already authorized - create session and redirect
    await createSessionAndRedirect()
    
  } catch (e: any) {
    // Check if the error is related to missing attributes
    const errorMsg = e.response?.data?.error_description || e.message
    
    // Check if the error is related to missing attributes
    if (errorMsg.includes('attributes required') && errorMsg.includes('phone_number')) {
      // Redirect to complete profile with required attributes and parameters
      router.replace({ 
        name: 'CompleteProfile',
        query: {
          required_attributes: 'phone_number',
          application_name: appName.value,
          channel_id: channelId.value,
          redirect_url: route.query.redirect_url as string,
          email: route.query.email as string || ''
        }
      })
    } else {
      error.value = 'Failed to sign in with Google. ' + errorMsg
      loading.value = false
    }
  }
})

// Create session and redirect to client app
async function createSessionAndRedirect() {
  try {
    // Create session with the tokens
    const sessionResponse = await api.initSession(tokens.value, appName.value)
    
    // Show success toast
    toast.success('Successfully signed in with Google!')
    
    // Redirect back to client app with session_id
    if (sessionResponse) {
      // Short delay to allow toast to be seen
      setTimeout(() => {
        const redirectUrl = route.query.redirect_url as string || import.meta.env.VITE_DEFAULT_REDIRECT_URL
        window.location.href = `${redirectUrl}?session_id=${sessionResponse.session_id}`
      }, 1000)
    } else {
      throw new Error('Failed to create session')
    }
  } catch (err: any) {
    error.value = err.message || 'Failed to initialize session'
    loading.value = false
  }
}

// Consent screen handlers
const handleConsentApproved = async () => {
  try {
    loading.value = true
    showConsentScreen.value = false
    
    // Small delay to ensure authorization record is fully created
    await new Promise(resolve => setTimeout(resolve, 500))
    
    // Create session with the authorized user
    await createSessionAndRedirect()
  } catch (err: any) {
    error.value = err.message || 'Authorization failed'
    loading.value = false
  }
}

const handleConsentDenied = () => {
  showConsentScreen.value = false
  error.value = 'You declined to authorize this application.'
  loading.value = false
}

const handleConsentError = (err: string) => {
  showConsentScreen.value = false
  error.value = err || 'An error occurred during authorization.'
  loading.value = false
}
</script>

<style scoped>
.loader {
  border: 4px solid #333;
  border-top: 4px solid #fff;
  border-radius: 50%;
  width: 32px;
  height: 32px;
  animation: spin 1s linear infinite;
}
@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}
</style>
