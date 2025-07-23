<template>
  <AuthBackground>
    <AuthCard title="Complete Your Profile" subtitle="Please provide the missing information to complete your profile">
      <form @submit.prevent="submitForm" class="mt-6">
        <!-- First Name and Last Name (Two columns) -->
        <div class="grid grid-cols-1 sm:grid-cols-2 gap-4 mb-4">
          <!-- First Name -->
          <div>
            <label for="firstName" class="text-zinc-300 font-medium tracking-wide text-xs block flex items-center gap-2 mb-1.5">
              <UserIcon :size="14" class="text-zinc-500" />
              First Name
            </label>
            <div class="relative">
              <input
                id="firstName"
                type="text"
                v-model="formData.given_name"
                placeholder="First Name"
                readonly
                class="bg-zinc-900/60 border border-zinc-700/60 text-white placeholder:text-zinc-500 focus:border-zinc-400 focus:ring-1 focus:ring-zinc-400 h-10 rounded-lg font-light tracking-wide text-sm transition-all duration-200 px-3 relative w-full opacity-70"
              />
              <div class="absolute inset-0 bg-gradient-to-r from-zinc-800/5 to-transparent rounded-lg pointer-events-none" />
            </div>
          </div>
          
          <!-- Last Name -->
          <div>
            <label for="lastName" class="text-zinc-300 font-medium tracking-wide text-xs block flex items-center gap-2 mb-1.5">
              <UserIcon :size="14" class="text-zinc-500" />
              Last Name
            </label>
            <div class="relative">
              <input
                id="lastName"
                type="text"
                v-model="formData.family_name"
                placeholder="Last Name"
                readonly
                class="bg-zinc-900/60 border border-zinc-700/60 text-white placeholder:text-zinc-500 focus:border-zinc-400 focus:ring-1 focus:ring-zinc-400 h-10 rounded-lg font-light tracking-wide text-sm transition-all duration-200 px-3 relative w-full opacity-70"
              />
              <div class="absolute inset-0 bg-gradient-to-r from-zinc-800/5 to-transparent rounded-lg pointer-events-none" />
            </div>
          </div>
        </div>
        
        <!-- Email Address (Full width) -->
        <div class="mb-4">
          <label for="email" class="text-zinc-300 font-medium tracking-wide text-xs block flex items-center gap-2 mb-1.5">
            <MailIcon :size="14" class="text-zinc-500" />
            Email Address
          </label>
          <div class="relative">
            <input
              id="email"
              type="email"
              v-model="formData.email"
              placeholder="Email Address"
              readonly
              class="bg-zinc-900/60 border border-zinc-700/60 text-white placeholder:text-zinc-500 focus:border-zinc-400 focus:ring-1 focus:ring-zinc-400 h-10 rounded-lg font-light tracking-wide text-sm transition-all duration-200 px-3 relative w-full opacity-70"
            />
            <div class="absolute inset-0 bg-gradient-to-r from-zinc-800/5 to-transparent rounded-lg pointer-events-none" />
          </div>
        </div>
        
        <!-- Phone Number (Full width) -->
        <div class="mb-4">
          <label for="phone" class="text-zinc-300 font-medium tracking-wide text-xs block flex items-center gap-2 mb-1.5">
            <PhoneIcon :size="14" class="text-zinc-500" />
            Mobile Number
          </label>
          <div class="relative">
            <div class="absolute inset-y-0 left-0 flex items-center pl-3 pointer-events-none">
              <span class="text-zinc-400 text-sm">+63</span>
            </div>
            <input
              id="phone"
              type="tel"
              v-model="phoneWithoutCode"
              placeholder="9XX XXX XXXX"
              required
              class="bg-zinc-900/60 border border-zinc-700/60 text-white placeholder:text-zinc-500 focus:border-zinc-400 focus:ring-1 focus:ring-zinc-400 h-10 rounded-lg font-light tracking-wide text-sm transition-all duration-200 pl-12 pr-3 relative w-full"
              @input="validatePhone"
            />
            <div class="absolute inset-0 bg-gradient-to-r from-zinc-800/5 to-transparent rounded-lg pointer-events-none" />
          </div>
          <p v-if="errors.phone" class="text-red-400 text-xs mt-0.5">{{ errors.phone }}</p>
        </div>

        <!-- Marketing Checkbox -->
        <div class="mt-4">
          <label class="flex items-center gap-2 cursor-pointer group">
            <div class="relative flex items-center">
              <input
                type="checkbox"
                v-model="formData.accepts_marketing"
                class="peer sr-only"
              />
              <div class="w-5 h-5 border border-zinc-700 rounded bg-zinc-900/60 peer-checked:bg-zinc-700 peer-checked:border-zinc-600 transition-all duration-200"></div>
              <CheckIcon :size="12" class="absolute text-white left-1/2 top-1/2 -translate-x-1/2 -translate-y-1/2 opacity-0 peer-checked:opacity-100 transition-opacity duration-200" />
            </div>
            <span class="text-zinc-400 text-sm group-hover:text-zinc-300 transition-colors duration-200">I agree to receive marketing communications</span>
          </label>
        </div>

        <!-- Submit Button -->
        <div class="flex justify-center mt-6">
          <AuthButton
            type="submit"
            :loading="loading"
            :disabled="!isFormValid"
            class="w-full sm:w-1/2"
          >
            Complete Profile
            <ArrowRightIcon :size="16" class="ml-1 transition-transform duration-200" />
          </AuthButton>
        </div>
      </form>

      <!-- Error Display -->
      <div v-if="error" class="mt-4 p-3 bg-red-900/20 border border-red-800/50 rounded-lg text-red-400 text-sm">
        {{ error }}
      </div>
    </AuthCard>
    
    <!-- Consent Screen Modal -->
    <ConsentScreen
      v-if="showConsentScreen"
      :applicationId="applicationName"
      :applicationName="applicationName"
      :idToken="userTokens?.id_token"
      @approved="handleConsentApproved"
      @denied="handleConsentDenied"
      @error="handleConsentError"
    />
  </AuthBackground>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useToast } from 'vue-toastification'
import AuthBackground from '../components/ui/AuthBackground.vue'
import AuthCard from '../components/ui/AuthCard.vue'
import AuthButton from '../components/ui/AuthButton.vue'
import { PhoneIcon, ArrowRightIcon, CheckIcon, UserIcon, MailIcon } from 'lucide-vue-next'
import ConsentScreen from '../components/ConsentScreen.vue'
import { useApi } from '../composables/useApi'

// Route and router
const route = useRoute()
const router = useRouter()
const toast = useToast()
const api = useApi()

// Form data
const formData = ref({
  phone: '',
  accepts_marketing: false,
  email: '',
  given_name: '',
  family_name: ''
})

// Phone number handling with country code
const phoneWithoutCode = ref('')

// State
const loading = ref(false)
const error = ref('')
const errors = ref<Record<string, string>>({})

// Consent screen state
const showConsentScreen = ref(false)
const userTokens = ref<any>(null)

// Get query parameters
const applicationName = ref(route.query.application_name as string || import.meta.env.VITE_DEFAULT_APPLICATION_NAME)
const channelId = ref(route.query.channel_id as string || import.meta.env.VITE_DEFAULT_CHANNEL_ID)
const redirectUrl = ref(route.query.redirect_url as string || import.meta.env.VITE_DEFAULT_REDIRECT_URL)

// Update full phone number when phoneWithoutCode changes
const validatePhone = () => {
  const phoneRegex = /^\d{10}$/
  const cleanPhone = phoneWithoutCode.value.replace(/\D/g, '')
  
  if (!cleanPhone) {
    errors.value.phone = 'Phone number is required'
  } else if (!phoneRegex.test(cleanPhone)) {
    errors.value.phone = 'Please enter a valid 10-digit phone number'
  } else {
    delete errors.value.phone
    formData.value.phone = `+63${cleanPhone}`
  }
}

// Check if form is valid
const isFormValid = computed(() => {
  validatePhone()
  return Object.keys(errors.value).length === 0
})

// --- Token handling and user info extraction ---
onMounted(() => {
  // Get token nonce from query params
  const tokenNonce = route.query.token_nonce as string
  
  // Check for query params first (from AuthCallback)
  if (route.query.email) {
    formData.value.email = route.query.email as string
  }
  if (route.query.given_name) {
    formData.value.given_name = route.query.given_name as string
  }
  if (route.query.family_name) {
    formData.value.family_name = route.query.family_name as string
  }
  
  // Retrieve tokens from localStorage
  if (tokenNonce) {
    const tokensRaw = localStorage.getItem(`temp_oauth_tokens_${tokenNonce}`)
    if (tokensRaw) {
      try {
        const tokens = JSON.parse(tokensRaw)
        userTokens.value = tokens
        
        // Decode id_token to get user info if not already set from query params
        const payload = JSON.parse(atob(tokens.id_token.split('.')[1]))
        console.log('Decoded ID token payload:', payload)
        
        // Fill in any missing user info from the token
        if (!formData.value.email && payload.email) {
          formData.value.email = payload.email
        }
        if (!formData.value.given_name && payload.given_name) {
          formData.value.given_name = payload.given_name
        }
        if (!formData.value.family_name && payload.family_name) {
          formData.value.family_name = payload.family_name
        }
      } catch (err) {
        console.error('Error decoding tokens:', err)
        error.value = 'Failed to load authentication tokens.'
      }
    } else {
      error.value = 'Authentication tokens not found. Please try logging in again.'
    }
  } else {
    error.value = 'No authentication token reference found.'
  }
})

// Submit form
const submitForm = async () => {
  validatePhone()
  if (!isFormValid.value) {
    return
  }
  loading.value = true
  error.value = ''
  try {
    if (!userTokens.value) {
      throw new Error('No authentication tokens available.')
    }
    
    // Prepare user attributes to update
    const userAttributes = {
      phone_number: formData.value.phone,
      'custom:needs_profile_completion': 'false', // Remove the profile completion flag
      'custom:accepts_marketing': formData.value.accepts_marketing ? 'true' : 'false'
    }
    
    console.log('Updating user profile with attributes:', userAttributes)
    
    // Call API to update user attributes
    const updated = await api.updateUserProfile(userAttributes, userTokens.value)
    if (!updated) throw new Error('Profile update failed.')
    
    // Remove tokens from localStorage after use
    const tokenNonce = route.query.token_nonce as string
    if (tokenNonce) localStorage.removeItem(`temp_oauth_tokens_${tokenNonce}`)
    
    // Show success message
    toast.success('Profile updated successfully!')
    
    // Show consent screen
    showConsentScreen.value = true
  } catch (e: any) {
    console.error('Profile update error:', e)
    error.value = e.message || 'Failed to update profile'
    loading.value = false
  }
}

// Consent screen handlers
const handleConsentApproved = async (scopes: string[]) => {
  try {
    loading.value = true
    showConsentScreen.value = false
    
    // Small delay to simulate authorization record creation
    await new Promise(resolve => setTimeout(resolve, 500))
    
    // Show success message
    toast.success('Profile completed successfully!')
    
    // Redirect to the client application
    if (redirectUrl.value) {
      window.location.href = redirectUrl.value
    } else {
      router.push({ name: 'login' })
    }
  } catch (err: any) {
    error.value = err.message || 'Authorization failed'
    loading.value = false
  }
}

const handleConsentDenied = () => {
  showConsentScreen.value = false
  error.value = 'You must authorize the application to continue'
  loading.value = false
}

const handleConsentError = (errorMessage: string) => {
  showConsentScreen.value = false
  error.value = errorMessage || 'An error occurred during authorization'
  loading.value = false
}

// This onMounted is now handled in the main onMounted function above
</script>