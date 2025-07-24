<template>
  <div class="auth-callback">
    <AuthBackground />
    <div class="container">
      <AuthCard>
        <template #header>
          <h1 class="text-center text-2xl font-bold mb-4">Authentication</h1>
        </template>
        
        <div v-if="loading" class="loading flex flex-col items-center justify-center py-8">
          <div class="spinner mb-4"></div>
          <p class="text-gray-300">Processing your login...</p>
        </div>
        
        <div v-else-if="error" class="error flex flex-col items-center justify-center py-4">
          <div class="bg-red-900/30 p-4 rounded-lg mb-4 w-full">
            <h2 class="text-red-400 font-semibold mb-2">Authentication Error</h2>
            <p class="text-gray-300 mb-4">{{ error }}</p>
          </div>
          <button @click="goToLogin" class="btn-primary w-full">Return to Login</button>
          
          <!-- Special case for phone_number attribute error -->

        </div>
      </AuthCard>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { Hub } from 'aws-amplify/utils'
import { fetchUserAttributes } from 'aws-amplify/auth'
import authService from '@/services/authService'
import { useApi } from '@/composables/useApi'

const router = useRouter()
const route = useRoute()
const api = useApi()

const loading = ref(true)
const error = ref('')
const appName = ref('')
const channelId = ref('')

// Function to handle successful authentication
const handleSuccessfulAuth = async () => {
  try {
    // After OAuth redirect, Amplify should have processed the callback
    // Get the current session which now includes OAuth tokens
    const tokens = await authService.getCurrentSession()
    if (!tokens) {
      console.log('Waiting for OAuth tokens to be processed...')
      // Retry after a brief moment
      await new Promise(resolve => setTimeout(resolve, 500))
      const retryTokens = await authService.getCurrentSession()
      if (!retryTokens) {
        throw new Error('Failed to get authentication tokens after OAuth')
      }
      return retryTokens
    }

    // Check if user needs to complete their profile
    const needsProfileCompletion = await authService.checkNeedsProfileCompletion()
    
    if (needsProfileCompletion) {
      console.log('User needs to complete their profile')
      
      // In Amplify v6, we need to fetch user attributes separately
      try {
        const attributes = await fetchUserAttributes()
        
        // Redirect to profile completion page
        router.replace({
          name: 'CompleteProfile',
          query: {
            required_attributes: 'phone_number',
            application_name: appName.value,
            channel_id: channelId.value,
            redirect_url: route.query.redirect_url as string,
            email: attributes.email || '',
            given_name: attributes.given_name || '',
            family_name: attributes.family_name || ''
          }
        })
        return
      } catch (attrError: any) {
        console.error('Error fetching user attributes:', attrError)
        throw new Error('Failed to get user attributes')
      }
    }
    
    // Check if user is authorized for this application
    const authCheck = await api.checkAppUser(tokens.idToken, appName.value)
    
    // If user is not authorized, create the app-user relationship
    if (!authCheck || !authCheck.authorized) {
      await api.authorizeApplication({
        application_id: appName.value,
        granted_scopes: ['profile', 'orders'],
        action: 'approve'
      }, tokens.idToken)
    }
    
    // Get redirect URL from query params or use default
    const redirectUrl = route.query.redirect_url as string || '/'
    
    // If redirecting to client app, include auth tokens
    if (redirectUrl.includes('8080') || redirectUrl.includes('client')) {
      // Build redirect URL with tokens for client app
      const tokenParams = new URLSearchParams({
        access_token: tokens.accessToken,
        id_token: tokens.idToken,
        refresh_token: tokens.refreshToken || '',
        expires_in: '3600' // 1 hour
      })
      
      const finalRedirectUrl = redirectUrl.includes('?') 
        ? `${redirectUrl}&${tokenParams.toString()}`
        : `${redirectUrl}?${tokenParams.toString()}`
      
      console.log('Redirecting to client app with tokens:', finalRedirectUrl)
      window.location.href = finalRedirectUrl
    } else {
      // Standard redirect
      window.location.href = redirectUrl
    }
  } catch (err: any) {
    console.error('Error during authentication:', err)
    error.value = err.message || 'Failed to process your login. Please try again.'
    loading.value = false
  }
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
      console.log('Custom OAuth state:', payload.data)
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
