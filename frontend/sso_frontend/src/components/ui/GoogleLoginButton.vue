<template>
  <button 
    @click="loginWithGoogle" 
    class="flex items-center justify-center w-full px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-md shadow-sm hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
  >
    <img src="@/assets/google-icon.svg" alt="Google" class="w-5 h-5 mr-2" />
    Sign in with Google
  </button>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { AuthService } from '@/services/authService'
import { useToast } from 'vue-toastification'

const route = useRoute()
const router = useRouter()
const authService = new AuthService()
const toast = useToast()
const isLoading = ref(false)

const loginWithGoogle = async () => {
  try {
    isLoading.value = true
    
    // Get application name and channel ID from route query OR use environment defaults
    const appName = (route.query.application_name as string) || import.meta.env.VITE_DEFAULT_APPLICATION_NAME || ''
    const channelId = (route.query.channel_id as string) || import.meta.env.VITE_DEFAULT_CHANNEL_ID || ''
    const redirectUrl = route.query.redirect_url as string || ''
    
    console.log('Starting Google OAuth login flow with Amplify')
    console.log('Application:', appName, '(from URL or env default)')
    console.log('Channel:', channelId, '(from URL or env default)')
    console.log('Redirect URL:', redirectUrl)
    
    // Validate we have required parameters (should always have them now with env defaults)
    if (!appName || !channelId) {
      console.error('Missing required OAuth parameters even with env defaults:', { appName, channelId })
      toast.error('OAuth configuration error. Please check environment variables.')
      isLoading.value = false
      return
    }
    
    // Store OAuth parameters in sessionStorage so they survive the OAuth redirect
    if (appName) sessionStorage.setItem('oauth_application_name', String(appName))
    if (channelId) sessionStorage.setItem('oauth_channel_id', String(channelId))
    if (redirectUrl) sessionStorage.setItem('oauth_redirect_url', String(redirectUrl))
    
    // Use Amplify's federated sign-in with Google
    await authService.signInWithGoogle()
  } catch (error) {
    console.error('Error during Google login:', error)
    toast.error('Failed to sign in with Google. Please try again.')
    isLoading.value = false
  }
}
</script>

<style scoped>
/* Add any custom styles here */
</style>