<template>
  <AuthBackground>
    <AuthCard>
      <!-- Header -->
      <div class="mb-8 text-center">
        <h1 class="text-3xl font-bold tracking-tight mb-2">
          <span class="bg-gradient-to-r from-gray-200 via-gray-100 to-gray-300 bg-clip-text text-transparent">
            processing authentication
          </span>
        </h1>
        <p class="text-zinc-500 text-sm">
          setting up your grind account
        </p>
      </div>
      
      <!-- Loading State -->
      <div v-if="loading" class="text-center py-8">
        <div class="inline-block w-8 h-8 border-2 border-zinc-600 border-t-zinc-300 rounded-full animate-spin"></div>
        <p class="mt-4 text-zinc-400">processing your google login...</p>
      </div>
      
      <!-- Error State -->
      <div v-else-if="error" class="text-center">
        <div class="bg-red-500/10 border border-red-500/20 text-red-400 px-4 py-3 rounded-lg text-sm mb-6">
          <h2 class="font-semibold mb-2">Authentication Error</h2>
          <p class="text-zinc-300">{{ error }}</p>
        </div>
        <AuthButton @click="goToLogin" class="w-full">
          return to login
        </AuthButton>
      </div>
      
      <!-- Success State (if needed) -->
      <div v-else class="text-center py-8">
        <div class="inline-block w-8 h-8 border-2 border-green-600 border-t-green-300 rounded-full animate-spin"></div>
        <p class="mt-4 text-zinc-400">authentication successful, redirecting...</p>
      </div>
    </AuthCard>

    <!-- Consent Screen Modal -->
    <ConsentScreen 
      v-if="showConsentScreen"
      :application-id="appName"
      :application-name="appName"
      :id-token="userTokens?.id_token"
      @approved="handleConsentApproved"
      @denied="handleConsentDenied"
      @error="handleConsentError"
    />
  </AuthBackground>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { Hub } from 'aws-amplify/utils'
import authService from '../services/oauthService'
import { useApi } from '../composables/useApi'
import { useAdminCheck } from '../composables/useAdminCheck.ts'
import ConsentScreen from '../components/ConsentScreen.vue'
import { useToast } from 'vue-toastification'
import AuthBackground from '../components/ui/AuthBackground.vue'
import AuthCard from '../components/ui/AuthCard.vue'
import AuthButton from '../components/ui/AuthButton.vue'

const router = useRouter()
const route = useRoute()
const api = useApi()
const toast = useToast()
const { checkIsAdmin, redirectToAdminPortalIfAdmin } = useAdminCheck()

// Admin portal URL - should match the deployed admin portal URL
const ADMIN_PORTAL_URL = import.meta.env.VITE_ADMIN_PORTAL_URL || 'http://localhost:5174'

// Enable debug mode for detailed logging
const isDebug = import.meta.env.VITE_OAUTH_DEBUG === 'true' || import.meta.env.DEV

// Component state
const loading = ref(true)
const error = ref('')
const appName = ref('')
const channelId = ref('')
const showConsentScreen = ref(false)
const userTokens = ref<any>(null)
const isAdminUser = ref(false)

// Helper function for debug logging
function logDebug(message: string, data?: any) {
  if (isDebug) {
    console.log(`[OAUTH:DEBUG] ${message}`, data || '')
  }
}

// Function to handle successful authentication 
const handleSuccessfulAuth = async () => {
  try {
    // First, check if user is an admin and store the result
    const tokens = await authService.getCurrentSession()
    if (tokens?.idToken?.toString()) {
      // Store tokens for later use
      localStorage.setItem('id_token', tokens.idToken.toString())
      // Check if user is an admin
      isAdminUser.value = await checkIsAdmin(tokens.idToken.toString())
      
      // If admin, redirect to admin portal instead of continuing the flow
      if (isAdminUser.value) {
        console.log('Admin user detected, redirecting to admin portal')
        toast.success('Welcome, Admin! Redirecting to admin portal...')
        // Short delay to allow toast to be seen
        setTimeout(() => {
          window.location.href = ADMIN_PORTAL_URL
        }, 1500)
        return
      }
    }
    
    // Continue with regular user flow
    // Get application info from OAuth custom state or fallback methods
    let localAppName = ''
    let localChannelId = ''
    let localRedirectUrl = ''
    
    // First, try to get from OAuth custom state (new method)
    try {
      // Listen for custom OAuth state from Amplify Hub
      const customStateStr = route.query.state as string
      if (customStateStr) {
        // OAuth state might contain our custom data
        console.log('OAuth state received:', customStateStr)
      }
      
      // Check if we have custom state in sessionStorage (set by Hub listener)
      if (customStateStr) {
        const parsed = JSON.parse(customStateStr)
        localAppName = parsed.application_name || ''
        localChannelId = parsed.channel_id || ''
        localRedirectUrl = parsed.redirect_url || ''
        console.log('Retrieved from custom state:', { appName: localAppName, channelId: localChannelId, redirectUrl: localRedirectUrl })
      }
    } catch (e) {
      console.log('Failed to parse custom state:', e)
    }
    
    // Second fallback: check route query parameters
    if (!localAppName || !localChannelId) {
      localAppName = route.query.application_name as string || ''
      localChannelId = route.query.channel_id as string || ''
      localRedirectUrl = route.query.redirect_url as string || ''
    }
    
    // Final fallback: check sessionStorage
    if (!localAppName || !localChannelId) {
      localAppName = sessionStorage.getItem('oauth_application_name') || ''
      localChannelId = sessionStorage.getItem('oauth_channel_id') || ''
      localRedirectUrl = sessionStorage.getItem('oauth_redirect_url') || ''
    }
    
    // Last resort: check if we're on a page with URL parameters (like LoginPage)
    if (!localAppName || !localChannelId) {
      console.log('Trying to get parameters from current URL...')
      const urlParams = new URLSearchParams(window.location.search)
      localAppName = urlParams.get('application_name') || ''
      localChannelId = urlParams.get('channel_id') || ''
      localRedirectUrl = urlParams.get('redirect_url') || ''
      console.log('URL parameters found:', { appName: localAppName, channelId: localChannelId, redirectUrl: localRedirectUrl })
    }
    
    // Final fallback: use environment defaults
    if (!localAppName || !localChannelId) {
      console.log('Using environment variable defaults...')
      localAppName = localAppName || import.meta.env.VITE_DEFAULT_APPLICATION_NAME || ''
      localChannelId = localChannelId || import.meta.env.VITE_DEFAULT_CHANNEL_ID || ''
      console.log('Environment defaults:', { appName: localAppName, channelId: localChannelId })
    }
    
    // Update refs for ConsentScreen
    appName.value = localAppName
    channelId.value = localChannelId
    
    if (!appName.value || !channelId.value) {
      console.error('All parameter retrieval methods failed:')
      console.error('Route query:', route.query)
      console.error('SessionStorage:', {
        appName: sessionStorage.getItem('oauth_application_name'),
        channelId: sessionStorage.getItem('oauth_channel_id'),
        customState: sessionStorage.getItem('oauth_custom_state')
      })
      throw new Error('Missing application or channel information. Please restart the login process.')
    }

    console.log('Processing Google OAuth for:', { appName: localAppName, channelId: localChannelId, redirectUrl: localRedirectUrl })

    // Clean up sessionStorage since we have the parameters
    sessionStorage.removeItem('oauth_application_name')
    sessionStorage.removeItem('oauth_channel_id')
    sessionStorage.removeItem('oauth_redirect_url')

    console.log('Processing Google OAuth for:', { appName: localAppName, channelId: localChannelId, redirectUrl: localRedirectUrl })
    
    try {
      console.log('[OAUTH:Flow] Starting Google OAuth process with params:', { 
        appName: localAppName, 
        channelId: localChannelId,
        hasRedirectUrl: !!localRedirectUrl
      })
      
      const result = await authService.processGoogleOAuth(localAppName, localChannelId, localRedirectUrl)
      console.log('[OAUTH:Flow] OAuth process completed with result type:', result ? Object.keys(result) : 'null')
      
      // Check if consent is required (only returned when profile is complete but user not authorized)
      if ('status' in result && result.status === 'consent_required') {
        // User needs to authorize the application first
        console.log('[OAUTH:Flow] User consent required - showing consent screen')
        showConsentScreen.value = true
        userTokens.value = result.tokens
        // Store redirect URL for later use
        if (localRedirectUrl) {
          localStorage.setItem('temp_redirect_url', localRedirectUrl)
        }
        return
      }
      
      // Check if profile completion is needed (this is checked first in the new flow)
      if (result.needsProfileCompletion) {
        // User needs to complete their profile
        console.log('[OAUTH:Flow] User needs to complete profile - redirecting to profile completion')
        
        // Store tokens and session info for profile completion
        localStorage.setItem('temp_session_id', result.sessionId)
        localStorage.setItem('temp_user_attributes', JSON.stringify(result.userAttributes))
        
        // Navigate to profile completion
        await router.push({
          name: 'CompleteProfile',
          query: {
            session_id: result.sessionId,
            redirect_url: localRedirectUrl || '',
            provider: 'google' // Add provider info for profile completion page
          }
        })
      } else {
        // User is fully authenticated, redirect to client app
        console.log('User fully authenticated, redirecting to client app')
        
        if (localRedirectUrl) {
          const finalUrl = `${localRedirectUrl}?session_id=${result.sessionId}`
          console.log('Redirecting to:', finalUrl)
          window.location.href = finalUrl
        } else {
          // Fallback: redirect to dashboard or home
          await router.push({ name: 'Dashboard' })
        }
      }
    } catch (err: any) {
      console.error('[OAUTH:Error]', err)
      // Provide more detailed error information
      if (err.name === 'UserNotFoundError' || err.message?.includes('USER_NOT_FOUND')) {
        console.error('[OAUTH:Error] User not found in DynamoDB - this is likely due to OAuth user not being created')
        error.value = 'Your Google account was authenticated but not registered in our system. Please try again or contact support.'
      } else if (err.name === 'TokenValidationError' || err.message?.includes('token')) {
        console.error('[OAUTH:Error] Token validation failed')
        error.value = 'Authentication token validation failed. Please try signing in again.'
      } else {
        error.value = err.message || 'Google OAuth authentication failed'
      }
      
      // Log detailed diagnostic information
      console.log('[OAUTH:Diagnostics] Error context:', {
        appName: localAppName,
        channelId: localChannelId,
        hasRedirectUrl: !!localRedirectUrl,
        errorType: err.name,
        errorMessage: err.message
      })
    } finally {
      loading.value = false
    }
  } catch (error: any) {
    console.error('Google OAuth process failed:', error)
    error.value = error.message || 'Google OAuth authentication failed'
  } finally {
    loading.value = false
  }
}

// Consent Screen Handlers
const handleConsentApproved = async () => {
  console.log('User approved consent, continuing OAuth flow...')
  showConsentScreen.value = false
  loading.value = true
  
  try {
    // Now that user has authorized, try to initialize session again
    const sessionResponse = await api.initSession(userTokens.value, appName.value)
    if (!sessionResponse) {
      throw new Error('Failed to initialize session with SSO backend')
    }

    console.log('Session initialized:', sessionResponse.session_id)

    // For Google OAuth users, always go to CompleteProfile page
    // since they need to complete their phone number and other details
    console.log('Redirecting to CompleteProfile page')
    
    // Store session info for CompleteProfile page
    localStorage.setItem('temp_session_id', sessionResponse.session_id)
    
    // Get redirect URL for after profile completion
    const redirectUrl = localStorage.getItem('temp_redirect_url') || ''
    
    // Navigate to profile completion
    await router.push({
      name: 'CompleteProfile',
      query: {
        session_id: sessionResponse.session_id,
        redirect_url: redirectUrl
      }
    })
    
  } catch (error: any) {
    console.error('Post-consent flow failed:', error)
    toast.error(error.message || 'Failed to complete authorization')
    error.value = error.message || 'Authorization failed'
  } finally {
    loading.value = false
  }
}

const handleConsentDenied = () => {
  console.log('User denied consent')
  showConsentScreen.value = false
  toast.error('Authorization was denied')
  goToLogin()
}

const handleConsentError = (message: string) => {
  console.error('Consent error:', message)
  showConsentScreen.value = false
  toast.error(message || 'Authorization failed')
  error.value = message || 'Authorization failed'
}

// Function to navigate back to login
const goToLogin = () => {
  router.push('/')
}

onMounted(() => {
  // Get application name and channel ID from route params or query
  appName.value = route.params.application_name as string || route.query.application_name as string || ''
  channelId.value = route.params.channel_id as string || route.query.channel_id as string || ''
  
  // Listen for auth events from Amplify
  const unsubscribe = Hub.listen('auth', ({ payload }) => {
    const { event } = payload
    
    if (event === 'signedIn') {
      console.log('User signed in')
      handleSuccessfulAuth()
    } else if (event === 'signedOut') {
      console.log('User signed out')
    } else if (event === 'customOAuthState') {
      console.log('Custom OAuth state received:', payload.data)
      // Store custom state in sessionStorage for later retrieval
      if (payload.data) {
        sessionStorage.setItem('oauth_custom_state', payload.data)
      }
    } else if (event === 'signInWithRedirect_failure') {
      console.error('User sign in failed:', payload.data)
      error.value = 'Sign in failed. Please try again.'
      loading.value = false
    }
  })
  
  // Check if we have an error in the URL
  if (route.query.error) {
    error.value = `Authentication error: ${route.query.error_description || route.query.error}`
    loading.value = false
    return
  }
  
  // Check if we're already authenticated (for handling browser refresh)
  authService.getCurrentUser()
    .then(user => {
      if (user) {
        console.log('User is already authenticated')
        handleSuccessfulAuth()
      } else {
        // This will be handled by the Hub listener when Amplify completes the OAuth flow
        console.log('Waiting for authentication to complete...')
      }
    })
    .catch((err: any) => {
      console.error('Error checking authentication status:', err)
      error.value = err.message || 'Failed to check authentication status'
      loading.value = false
    })
  
  // Cleanup listener when component unmounts
  return () => {
    unsubscribe()
  }
})
</script>

<style scoped>
.auth-callback {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 100vh;
  padding: 1rem;
}

.loading, .error {
  text-align: center;
  max-width: 400px;
  padding: 2rem;
  border-radius: 8px;
  background-color: #2a2a2a;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.spinner {
  border: 4px solid rgba(255, 255, 255, 0.1);
  border-radius: 50%;
  border-top: 4px solid #3498db;
  width: 40px;
  height: 40px;
  margin: 0 auto 1rem;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.btn-primary {
  background-color: #3498db;
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 4px;
  cursor: pointer;
  margin-top: 1rem;
}

.btn-primary:hover {
  background-color: #2980b9;
}
</style>
