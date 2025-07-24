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
    
    // Get application name and channel ID from route params or query
    const appName = route.params.application_name || route.query.application_name || ''
    const channelId = route.params.channel_id || route.query.channel_id || ''
    
    console.log('Starting Google OAuth login flow with Amplify')
    console.log('Application:', appName)
    console.log('Channel:', channelId)
    
    // Check if user is already signed in
    try {
      const currentUser = await authService.getCurrentUser()
      if (currentUser) {
        console.log('User already signed in, redirecting...')
        // Redirect to dashboard or original destination
        const redirectUrl = route.query.redirect_url as string
        if (redirectUrl) {
          window.location.href = redirectUrl
        } else {
          router.push('/dashboard')
        }
        return
      }
    } catch (e) {
      // Not signed in, proceed with Google login
    }
    
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