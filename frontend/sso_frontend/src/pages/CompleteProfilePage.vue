<template>
  <AuthBackground>
    <!-- Back Button - Top Left -->
    <div class="fixed top-4 left-4 z-50">
      <AuthButton 
        @click="goBack"
        class="!bg-transparent !border-zinc-700 !text-zinc-400 hover:!text-zinc-300 hover:!bg-zinc-800/50 !text-sm !px-3 !py-2"
      >
        <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18"></path>
        </svg>
        back
      </AuthButton>
    </div>

    <AuthCard wide>
      <!-- Header -->
      <div class="mb-8 text-center">
        <h1 class="text-3xl font-bold tracking-tight mb-2">
          <span class="bg-gradient-to-r from-gray-200 via-gray-100 to-gray-300 bg-clip-text text-transparent">
            complete your profile
          </span>
        </h1>
        <p class="text-zinc-500 text-sm">
          finish setting up your account for the grind
        </p>
      </div>

      <!-- Loading State -->
      <div v-if="loading" class="text-center py-8">
        <div class="inline-block w-8 h-8 border-2 border-zinc-600 border-t-zinc-300 rounded-full animate-spin"></div>
        <p class="mt-4 text-zinc-400">loading your profile...</p>
      </div>

      <!-- Error State -->
      <div v-else-if="error" class="bg-red-500/10 border border-red-500/20 text-red-400 px-4 py-3 rounded-lg text-sm mb-6">
        {{ error }}
      </div>

      <!-- Profile Form -->
      <form v-else @submit.prevent="handleSubmit" class="space-y-6">
        <!-- Name Fields -->
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label class="block text-sm font-medium text-zinc-300 mb-2">First Name</label>
            <div class="relative">
              <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                <svg class="w-4 h-4 text-zinc-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"></path>
                </svg>
              </div>
              <input
                id="given_name"
                type="text"
                placeholder="Enter your first name"
                v-model="formData.given_name"
                readonly
                disabled
                class="w-full pl-10 pr-4 py-3 bg-zinc-800/30 border border-zinc-700/60 rounded-lg text-zinc-400 cursor-not-allowed focus:outline-none"
              />
            </div>
          </div>
          
          <div>
            <label class="block text-sm font-medium text-zinc-300 mb-2">Last Name</label>
            <div class="relative">
              <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                <svg class="w-4 h-4 text-zinc-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"></path>
                </svg>
              </div>
              <input
                id="family_name"
                type="text"
                placeholder="Enter your last name"
                v-model="formData.family_name"
                readonly
                disabled
                class="w-full pl-10 pr-4 py-3 bg-zinc-800/30 border border-zinc-700/60 rounded-lg text-zinc-400 cursor-not-allowed focus:outline-none"
              />
            </div>
          </div>
        </div>
        
        <!-- Phone Number -->
        <!-- Phone Number with +63 prefix -->
        <div>
          <label for="phone_number" class="block text-sm font-medium text-zinc-300 mb-2">Mobile Number *</label>
          <div class="flex">
            <div class="flex-shrink-0 bg-zinc-800/30 border border-zinc-700/60 border-r-0 rounded-l-lg px-3 flex items-center justify-center text-zinc-300 text-sm font-medium">
              +63
            </div>
            <div class="flex-grow relative">
              <input
                id="phone_number"
                type="tel"
                placeholder="9XX XXX XXXX"
                v-model="phoneWithoutCode"
                required
                class="w-full bg-zinc-800/30 border border-zinc-700/60 text-white placeholder:text-zinc-500 focus:border-zinc-400 focus:ring-1 focus:ring-zinc-400 py-3 rounded-r-lg font-light tracking-wide text-sm transition-all duration-200 pl-3 pr-3 relative"
              />
            </div>
          </div>
        </div>
        
        <!-- Email (Read-only) -->
        <div>
          <label class="block text-sm font-medium text-zinc-300 mb-2">
            Email Address
          </label>
          <div class="relative">
            <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
              <svg class="w-4 h-4 text-zinc-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 8l7.89 4.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"></path>
              </svg>
            </div>
            <input
              type="email"
              :value="formData.email"
              readonly
              disabled
              class="w-full pl-10 pr-4 py-3 bg-zinc-800/30 border border-zinc-700/60 rounded-lg text-zinc-400 cursor-not-allowed focus:outline-none"
            />
          </div>
        </div>
        
        <!-- Gender -->
        <div>
          <label class="block text-sm font-medium text-zinc-300 mb-3">
            Gender *
          </label>
          <div class="flex gap-6">
            <label class="flex items-center cursor-pointer">
              <input
                type="radio"
                value="male"
                v-model="formData.gender"
                class="sr-only"
              />
              <div class="relative">
                <div class="w-4 h-4 border-2 border-zinc-600 rounded-full transition-all"
                     :class="formData.gender === 'male' ? 'border-zinc-400 bg-zinc-400' : 'hover:border-zinc-500'"></div>
                <div v-if="formData.gender === 'male'" class="absolute top-1 left-1 w-2 h-2 bg-zinc-900 rounded-full"></div>
              </div>
              <span class="ml-3 text-zinc-300">Male</span>
            </label>
            <label class="flex items-center cursor-pointer">
              <input
                type="radio"
                value="female"
                v-model="formData.gender"
                class="sr-only"
              />
              <div class="relative">
                <div class="w-4 h-4 border-2 border-zinc-600 rounded-full transition-all"
                     :class="formData.gender === 'female' ? 'border-zinc-400 bg-zinc-400' : 'hover:border-zinc-500'"></div>
                <div v-if="formData.gender === 'female'" class="absolute top-1 left-1 w-2 h-2 bg-zinc-900 rounded-full"></div>
              </div>
              <span class="ml-3 text-zinc-300">Female</span>
            </label>
          </div>
        </div>
        
        <!-- Marketing Consent -->
        <div class="bg-zinc-800/30 border border-zinc-700/40 rounded-lg p-4">
          <label class="flex items-start cursor-pointer">
            <input
              type="checkbox"
              v-model="formData.accepts_marketing"
              class="sr-only"
            />
            <div class="relative mt-1">
              <div class="w-4 h-4 border-2 border-zinc-600 rounded transition-all"
                   :class="formData.accepts_marketing ? 'border-zinc-400 bg-zinc-400' : 'hover:border-zinc-500'"></div>
              <svg v-if="formData.accepts_marketing" class="absolute top-0 left-0 w-4 h-4 text-zinc-900" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"></path>
              </svg>
            </div>
            <div class="ml-3">
              <span class="text-zinc-300 text-sm">
                I would like to receive marketing communications and promotional offers
              </span>
            </div>
          </label>
        </div>
        
        <!-- Submit Button -->
        <AuthButton
          type="submit"
          :disabled="isSubmitting"
          :loading="isSubmitting"
          class="w-full"
        >
          {{ isSubmitting ? 'completing profile...' : 'complete profile' }}
        </AuthButton>
      </form>
    </AuthCard>

    <!-- Consent Screen Modal -->
    <ConsentScreen
      v-if="showConsentScreen"
      :application-name="applicationName"
      :application-id="applicationName"
      :id-token="idToken"
      @approved="handleConsentApproved"
      @denied="handleConsentDenied"
      @error="handleConsentError"
    />
  </AuthBackground>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted, watch } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useApi } from '../composables/useApi'
import { useToast } from 'vue-toastification'
import { updateUserAttributes } from 'aws-amplify/auth'
import authService from '../services/authService'
import ConsentScreen from '../components/ConsentScreen.vue'
import AuthBackground from '../components/ui/AuthBackground.vue'
import AuthCard from '../components/ui/AuthCard.vue'
import AuthButton from '../components/ui/AuthButton.vue'
import AuthInput from '../components/ui/AuthInput.vue'

const route = useRoute()
const router = useRouter()
const api = useApi()
const toast = useToast()

// State
const loading = ref(false)
const isSubmitting = ref(false)
const showConsentScreen = ref(false)
const idToken = ref('')
const sessionId = ref(route.query.session_id as string || '')
const applicationName = ref(route.query.application_name as string || '')
const channelId = ref(route.query.channel_id as string || '')
const redirectUrl = ref(route.query.redirect_url as string || '/')
const error = ref('')

// Form data
const formData = reactive({
  given_name: '',
  family_name: '',
  phone_number: '',
  email: '',
  gender: 'male',
  accepts_marketing: false
})

// Phone number handling with country code
const phoneWithoutCode = ref('')

// Update full phone number when phoneWithoutCode changes
watch(phoneWithoutCode, (newValue) => {
  formData.phone_number = `+63${newValue.replace(/\D/g, '')}`
})

// Helper function to parse JWT token
function parseJwt(token: string) {
  try {
    const base64Url = token.split('.')[1]
    const base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/')
    const jsonPayload = decodeURIComponent(atob(base64).split('').map(function(c) {
      return '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2)
    }).join(''))
    return JSON.parse(jsonPayload)
  } catch (e) {
    console.error('error parsing jwt token:', e)
    return {}
  }
}

// Load user data on mount
const loadUserData = async () => {
  loading.value = true
  error.value = ''
  
  try {
    // Try to get user data from session tokens instead of fetchUserAttributes
    const session = await authService.getCurrentSession()
    if (session && session.idToken) {
      const tokenPayload = parseJwt(session.idToken)
      console.log('Token payload:', tokenPayload)
      
      // Pre-populate form with token data
      // Handle name splitting - Google OAuth often provides just 'name' field
      const fullName = tokenPayload.name || ''
      const nameParts = fullName.split(' ')
      
      formData.given_name = tokenPayload.given_name || nameParts[0] || ''
      formData.family_name = tokenPayload.family_name || (nameParts.length > 1 ? nameParts.slice(1).join(' ') : '')
      formData.phone_number = tokenPayload.phone_number || ''
      formData.email = tokenPayload.email || ''
      formData.gender = tokenPayload['custom:gender'] || ''
      formData.accepts_marketing = tokenPayload['custom:accepts_marketing'] === 'true'
      
      console.log('User data loaded from token:', formData)
    } else {
      // Fallback: try to get from localStorage
      const storedAttributes = localStorage.getItem('temp_user_attributes')
      if (storedAttributes) {
        const attributes = JSON.parse(storedAttributes)
        
        // Handle name splitting for localStorage data too
        const fullName = attributes.name || ''
        const nameParts = fullName.split(' ')
        
        formData.given_name = attributes.given_name || nameParts[0] || ''
        formData.family_name = attributes.family_name || (nameParts.length > 1 ? nameParts.slice(1).join(' ') : '')
        formData.phone_number = attributes.phone_number || ''
        formData.email = attributes.email || ''
        formData.gender = attributes['custom:gender'] || ''
        formData.accepts_marketing = attributes['custom:accepts_marketing'] === 'true'
        
        console.log('User data loaded from localStorage:', attributes)
      } else {
        error.value = 'No user session found. Please try logging in again.'
      }
    }
  } catch (err: any) {
    console.error('Error loading user data:', err)
    error.value = err.message || 'Failed to load user data'
  } finally {
    loading.value = false
  }
}

// Go back function
const goBack = () => {
  router.back()
}

// Submit form
const handleSubmit = async () => {
  try {
    isSubmitting.value = true
    error.value = ''
    
    // Validate phone number
    if (!/^\+[1-9]\d{6,14}$/.test(formData.phone_number)) {
      throw new Error('Please enter a valid phone number')
    }
    
    // Prepare attributes to update
    const attributesToUpdate: Record<string, string> = {
      phone_number: formData.phone_number,
      'custom:gender': formData.gender, // Use custom:gender as the attribute name
      'custom:accepts_marketing': formData.accepts_marketing ? 'true' : 'false',
      'custom:needs_profile_completion': 'false' // Remove the profile completion flag
    }
    
    console.log('Updating user attributes:', attributesToUpdate)
    
    // Check if we have session_id in URL params
    if (!sessionId.value) {
      throw new Error('No session ID found in URL parameters')
    }
    
    // Get session and tokens from SSO backend using session ID
    const sessionData = await api.getSession(sessionId.value)
    if (!sessionData || !sessionData.tokens) {
      throw new Error('Failed to get session data from backend')
    }
    
    // Format tokens as expected by the API
    const formattedTokens = {
      id_token: sessionData.tokens.id_token,
      access_token: sessionData.tokens.access_token
    }
    
    console.log('Tokens obtained from session ID for profile update')
    
    // Update user attributes using the API service
    const success = await api.updateUserProfile(attributesToUpdate, formattedTokens)
    
    if (!success) {
      throw new Error('Failed to update profile')
    }
    
    console.log('Profile updated successfully')
    toast.success('Profile updated successfully!')
    
    // Store the id_token for consent screen
    idToken.value = sessionData.tokens.id_token
    
    // Check if user needs to authorize the application
    const authCheck = await api.checkAppUser(sessionData.tokens.id_token, applicationName.value)
    
    if (!authCheck || !authCheck.authorized) {
      // Show consent screen
      showConsentScreen.value = true
    } else {
      // User is already authorized - redirect to application
      await handleRedirect()
    }
  } catch (err: any) {
    console.error('Error updating profile:', err)
    error.value = err.message || 'Failed to update profile. Please try again.'
    toast.error('Failed to update profile')
  } finally {
    isSubmitting.value = false
  }
}

// Consent screen handlers
const handleConsentApproved = async () => {
  try {
    console.log('Consent approved, redirecting to application')
    showConsentScreen.value = false
    
    // Redirect to application after consent approval
    await handleRedirect()
  } catch (err: any) {
    console.error('Error during consent approval:', err)
    error.value = err.message || 'Authorization failed'
    toast.error('Authorization failed')
  }
}

const handleConsentDenied = () => {
  console.log('Consent denied')
  showConsentScreen.value = false
  error.value = 'You declined to authorize this application.'
  toast.error('Authorization denied')
}

const handleConsentError = (message: string) => {
  console.error('Consent error:', message)
  showConsentScreen.value = false
  error.value = message || 'An error occurred during authorization.'
  toast.error('Authorization failed')
}

// Handle redirect to application
const handleRedirect = async () => {
  try {
    // Show success toast
    toast.success('Profile completed successfully!')
    
    // Use the existing session_id that was passed from AuthCallback
    if (sessionId.value) {
      console.log('Redirecting to client app with session ID:', sessionId.value)
      // Short delay to allow toast to be seen
      setTimeout(() => {
        // Use provided redirect URL or fall back to default from environment variables
        const defaultRedirectUrl = import.meta.env.VITE_DEFAULT_REDIRECT_URL || 'http://localhost:8080'
        const finalRedirectUrl = redirectUrl.value || defaultRedirectUrl
        window.location.href = `${finalRedirectUrl}?session_id=${sessionId.value}`
      }, 1000)
    } else {
      throw new Error('No session ID available for redirect')
    }
  } catch (err: any) {
    console.error('Error during redirect:', err)
    error.value = err.message || 'Failed to complete redirect'
  }
}

// Initialize on mount
onMounted(() => {
  loadUserData()
})
</script>

<style scoped>
/* Add any custom styles here */
</style>