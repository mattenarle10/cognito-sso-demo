<template>
  <AuthBackground>
    <AuthCard>
      <div class="text-center mb-8">
        <h1 class="text-3xl font-bold mb-2 bg-gradient-to-r from-gray-200 via-gray-100 to-gray-300 bg-clip-text text-transparent">The Grind.</h1>
        <p class="text-zinc-500">Complete your profile</p>
      </div>
      
      <div v-if="error" class="bg-red-500/10 border border-red-500/20 text-red-400 px-4 py-3 rounded-lg text-sm mb-4">
        {{ error }}
      </div>
      
      <form @submit.prevent="submitForm" class="space-y-4">
        <!-- First Name and Last Name in 2 columns -->
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label for="given_name" class="block text-sm font-medium text-zinc-400 mb-1">First Name</label>
            <input 
              id="given_name" 
              v-model="formData.given_name" 
              type="text" 
              required
              class="w-full px-3 py-2 bg-zinc-800/50 border border-zinc-700 rounded-md focus:outline-none focus:ring-1 focus:ring-blue-500 text-white"
            />
          </div>
          <div>
            <label for="family_name" class="block text-sm font-medium text-zinc-400 mb-1">Last Name</label>
            <input 
              id="family_name" 
              v-model="formData.family_name" 
              type="text" 
              required
              class="w-full px-3 py-2 bg-zinc-800/50 border border-zinc-700 rounded-md focus:outline-none focus:ring-1 focus:ring-blue-500 text-white"
            />
          </div>
        </div>
        
        <!-- Phone Number -->
        <div>
          <label for="phone_number" class="block text-sm font-medium text-zinc-400 mb-1">Mobile Number</label>
          <div class="relative">
            <span class="absolute inset-y-0 left-0 flex items-center pl-3 text-zinc-500">+</span>
            <input 
              id="phone_number" 
              v-model="formData.phone_number" 
              type="tel" 
              required
              placeholder="1234567890 (no spaces or dashes)"
              class="w-full pl-7 pr-3 py-2 bg-zinc-800/50 border border-zinc-700 rounded-md focus:outline-none focus:ring-1 focus:ring-blue-500 text-white"
            />
          </div>
          <p class="text-xs text-zinc-500 mt-1">Format: Country code + number (e.g., 12025550123)</p>
        </div>
        
        <!-- Email (readonly) -->
        <div>
          <label for="email" class="block text-sm font-medium text-zinc-400 mb-1">Email Address</label>
          <input 
            id="email" 
            v-model="formData.email" 
            type="email" 
            readonly
            class="w-full px-3 py-2 bg-zinc-800/80 border border-zinc-700 rounded-md text-zinc-400 cursor-not-allowed"
          />
        </div>
        
        <!-- Gender Selection -->
        <div>
          <label class="block text-sm font-medium text-zinc-400 mb-1">Gender</label>
          <div class="flex space-x-4">
            <label class="inline-flex items-center">
              <input type="radio" v-model="formData.gender" value="Male" class="form-radio text-blue-500" />
              <span class="ml-2 text-zinc-300">Male</span>
            </label>
            <label class="inline-flex items-center">
              <input type="radio" v-model="formData.gender" value="Female" class="form-radio text-blue-500" />
              <span class="ml-2 text-zinc-300">Female</span>
            </label>
          </div>
        </div>
        
        <!-- Marketing Consent -->
        <div class="flex items-start">
          <div class="flex items-center h-5">
            <input 
              id="marketing" 
              v-model="formData.accepts_marketing" 
              type="checkbox"
              class="h-4 w-4 text-blue-600 border-zinc-700 rounded focus:ring-blue-500 focus:ring-offset-zinc-800"
            />
          </div>
          <div class="ml-3 text-sm">
            <label for="marketing" class="text-zinc-300">I agree to receive marketing communications</label>
          </div>
        </div>
        
        <div class="pt-2">
          <button 
            type="submit" 
            class="w-full bg-blue-600 hover:bg-blue-700 text-white py-2 px-4 rounded-md transition duration-200 flex items-center justify-center"
            :disabled="isSubmitting"
          >
            <span v-if="isSubmitting" class="inline-block w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin mr-2"></span>
            {{ isSubmitting ? 'Updating Profile...' : 'Complete Profile' }}
          </button>
        </div>
      </form>
    </AuthCard>
    
    <!-- Consent Screen Modal -->
    <ConsentScreen
      v-if="showConsentScreen"
      :applicationId="applicationName"
      :applicationName="applicationName"
      :idToken="idToken"
      @approved="handleConsentApproved"
      @denied="handleConsentDenied"
      @error="handleConsentError"
    />
  </AuthBackground>
</template>

<script setup lang="ts">
import { ref, reactive, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useToast } from 'vue-toastification'
import { fetchUserAttributes } from 'aws-amplify/auth'
import authService, { type UserAttributes } from '@/services/authService'
import { useApi } from '@/composables/useApi'
import AuthBackground from '@/components/ui/AuthBackground.vue'
import AuthCard from '@/components/ui/AuthCard.vue'
import ConsentScreen from '@/components/ConsentScreen.vue'

const route = useRoute()
const router = useRouter()
const toast = useToast()
const api = useApi()

const error = ref('')
const isSubmitting = ref(false)
const showConsentScreen = ref(false)
const idToken = ref('')
const applicationName = ref(route.query.application_name as string || '')
const channelId = ref(route.query.channel_id as string || '')
const redirectUrl = ref(route.query.redirect_url as string || '/')

// Form data
const formData = reactive({
  given_name: '',
  family_name: '',
  phone_number: '',
  email: '',
  gender: 'Male',
  accepts_marketing: false
})

// Function to load user data
const loadUserData = async () => {
  try {
    // In Amplify v6, we need to fetch attributes separately
    const attributes = await fetchUserAttributes()
    
    // Pre-fill form with existing user data
    formData.given_name = attributes.given_name || route.query.given_name as string || ''
    formData.family_name = attributes.family_name || route.query.family_name as string || ''
    formData.phone_number = attributes.phone_number || ''
    formData.email = attributes.email || route.query.email as string || ''
    
    // If phone number is the placeholder, clear it
    if (formData.phone_number === '+00000000000') {
      formData.phone_number = ''
    }
  } catch (error: any) {
    console.error('Error loading user data:', error)
    toast.error('Failed to load user data')
  }
}

onMounted(async () => {
  try {
    // Get current authenticated user and session
    const user = await authService.getCurrentUser()
    const session = await authService.getCurrentSession()
    
    if (!user || !session) {
      error.value = 'Authentication error. Please try logging in again.'
      return
    }
    
    // Store the ID token for later use
    idToken.value = session.idToken
    
    // Load user data and fetch attributes
    await loadUserData()
    
    try {
      // In Amplify v6, we need to fetch attributes separately
      const userAttributes = await fetchUserAttributes()
      
      // Pre-fill gender if available
      if (userAttributes['custom:gender']) {
        formData.gender = userAttributes['custom:gender']
      }
      
      // Pre-fill marketing preference if available
      if (userAttributes['custom:accepts_marketing'] === 'true') {
        formData.accepts_marketing = true
      }
      
      console.log('User attributes loaded:', userAttributes)
      console.log('Form data initialized:', formData)
    } catch (attrError) {
      console.error('Error fetching user attributes:', attrError)
    }
  } catch (err) {
    console.error('Error initializing profile form:', err)
    error.value = 'Failed to load your profile information. Please try logging in again.'
  }
})

// Form submission
const submitForm = async () => {
  try {
    isSubmitting.value = true
    error.value = ''
    
    // Validate phone number format
    if (!formData.phone_number.startsWith('+')) {
      formData.phone_number = '+' + formData.phone_number
    }
    
    // Validate phone number
    if (!/^\+[1-9]\d{6,14}$/.test(formData.phone_number)) {
      throw new Error('Please enter a valid phone number with country code')
    }
    
    // Prepare attributes to update
    const attributesToUpdate: UserAttributes = {
      phone_number: formData.phone_number,
      'custom:gender': formData.gender,
      'custom:accepts_marketing': formData.accepts_marketing ? 'true' : 'false',
      'custom:needs_profile_completion': 'false' // Remove the profile completion flag
    }
    
    console.log('Updating user attributes:', attributesToUpdate)
    
    // Update user attributes using Amplify
    const success = await authService.updateUserAttributes(attributesToUpdate)
    
    if (!success) {
      throw new Error('Failed to update profile')
    }
    
    console.log('Profile updated successfully')
    toast.success('Profile updated successfully!')
    
    // Check if user is authorized for this application
    const session = await authService.getCurrentSession()
    if (!session) {
      throw new Error('Failed to get authentication session')
    }
    
    const authCheck = await api.checkAppUser(session.idToken, applicationName.value)
    
    if (!authCheck || !authCheck.authorized) {
      // Show consent screen
      showConsentScreen.value = true
    } else {
      // User is already authorized - redirect to application
      handleRedirect()
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
    showConsentScreen.value = false
    
    // Get current session
    const session = await authService.getCurrentSession()
    if (!session) {
      throw new Error('Failed to get authentication session')
    }
    
    // Create app-user relationship
    await api.authorizeApplication({
      application_id: applicationName.value,
      granted_scopes: ['profile', 'orders'],
      action: 'approve'
    }, session.idToken)
    
    // Redirect to application
    handleRedirect()
  } catch (err: any) {
    console.error('Error during consent approval:', err)
    error.value = err.message || 'Authorization failed'
  }
}

const handleConsentDenied = () => {
  showConsentScreen.value = false
  error.value = 'You declined to authorize this application.'
}

const handleConsentError = (err: string) => {
  showConsentScreen.value = false
  error.value = err || 'An error occurred during authorization.'
}

// Handle redirect to application
const handleRedirect = async () => {
  try {
    // Get current session
    const session = await authService.getCurrentSession()
    if (!session) {
      throw new Error('Failed to get authentication session')
    }
    
    // Create session with the tokens
    const sessionResponse = await api.initSession(
      {
        id_token: session.idToken,
        access_token: session.accessToken,
        refresh_token: session.refreshToken
      },
      applicationName.value
    )
    
    // Show success toast
    toast.success('Profile completed successfully!')
    
    // Redirect back to client app with session_id
    if (sessionResponse && sessionResponse.session_id) {
      // Short delay to allow toast to be seen
      setTimeout(() => {
        window.location.href = `${redirectUrl.value}?session_id=${sessionResponse.session_id}`
      }, 1000)
    } else {
      throw new Error('Failed to create session')
    }
  } catch (err: any) {
    console.error('Error during redirect:', err)
    error.value = err.message || 'Failed to initialize session'
  }
}
</script>

<style scoped>
/* Add any custom styles here */
</style>