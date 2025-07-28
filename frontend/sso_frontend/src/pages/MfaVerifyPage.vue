<template>
  <AuthBackground>
    <AuthCard v-if="!showConsentScreen">
      <!-- Header with enhanced styling -->
      <div class="mb-4 relative text-center">
        <div class="absolute -top-10 -right-10 w-40 h-40 bg-gradient-to-br from-zinc-800/30 to-zinc-900/30 rounded-full blur-3xl"></div>
        <h1 class="text-3xl font-bold tracking-tight mb-1 relative">
          <span class="bg-gradient-to-r from-gray-200 via-gray-100 to-gray-300 bg-clip-text text-transparent relative inline-block">Two-Factor Verification</span>
        </h1>
        <p class="text-zinc-500 text-sm font-light tracking-wide" v-if="appName">to continue to {{ appName }}</p>
        <p class="text-zinc-400 text-sm mt-3 bg-zinc-800/50 py-2 px-3 rounded-lg inline-block">
          <span class="text-zinc-300">
            {{ challengeType === 'SMS_MFA' ? 'Code sent to your phone:' : 'Code sent to your email:' }}
          </span>
          {{ challengeType === 'SMS_MFA' ? route.query.phone || 'your phone' : maskedEmail }}
        </p>
      </div>

      <!-- OTP Input Boxes -->
      <form @submit.prevent="handleMfaVerification" class="space-y-5">
        <div>
          <div class="flex justify-center gap-2 mt-2">
            <div 
              v-for="(digit, index) in 6" 
              :key="index"
              class="relative"
            >
              <input
                type="text"
                maxlength="1"
                :id="`mfa-${index}`"
                v-model="mfaDigits[index]"
                @input="handleDigitInput(index)"
                @keydown="handleKeyDown($event, index)"
                @paste="handlePaste"
                class="w-11 h-14 bg-zinc-900/60 border border-zinc-700/60 text-white text-center text-xl font-medium rounded-lg focus:border-zinc-400 focus:ring-1 focus:ring-zinc-400 transition-all duration-200"
              />
              <div class="absolute inset-0 bg-gradient-to-r from-zinc-800/5 to-transparent rounded-lg pointer-events-none" />
            </div>
          </div>
          <p v-if="errors.mfa" class="text-red-400 text-xs mt-2 text-center">{{ errors.mfa }}</p>
        </div>

        <!-- Submit Button -->
        <AuthButton
          type="submit"
          :loading="loading"
          :disabled="!isMfaComplete"
          class="w-full"
        >
          <span class="flex items-center justify-center gap-2">
            Verify Code
            <ArrowRightIcon :size="16" />
          </span>
        </AuthButton>

        <!-- Back to Login Link -->
        <div class="flex flex-col items-center gap-2 pt-1">
          <!-- Resend code button with countdown -->
          <button 
            type="button"
            @click="handleResendCode"
            :disabled="loading || resendCountdown > 0"
            class="text-zinc-400 hover:text-white text-xs transition-colors duration-200 py-1"
          >
            <span v-if="resendCountdown > 0">Resend code in {{ resendCountdown }}s</span>
            <span v-else-if="resendLoading">Sending code...</span>
            <span v-else>Resend code</span>
          </button>
          
          <router-link 
            :to="loginLink" 
            class="text-zinc-500 hover:text-zinc-400 text-xs transition-colors duration-200"
          >
            Return to login
          </router-link>
        </div>

        <!-- Error Display -->
        <div v-if="error" class="bg-red-900/20 border border-red-800/50 text-red-400 text-xs py-2 px-3 rounded-lg mt-2">
          {{ error }}
        </div>
      </form>
    </AuthCard>
    
    <!-- Consent Screen Modal -->
    <ConsentScreen
      v-if="showConsentScreen"
      :applicationId="appName"
      :applicationName="appName"
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
import AuthBackground from '../components/ui/AuthBackground.vue'
import AuthCard from '../components/ui/AuthCard.vue'
import AuthButton from '../components/ui/AuthButton.vue'
import ConsentScreen from '../components/ConsentScreen.vue'
import { ArrowRightIcon } from 'lucide-vue-next'
import { cognitoService, type CognitoTokens } from '../services/cognitoService'
import { useToast } from 'vue-toastification'
import { useApi } from '../composables/useApi'

const route = useRoute()
const router = useRouter()
const api = useApi()
const toast = useToast()

// reactive state
const mfaDigits = ref<string[]>(Array(6).fill(''))
const loading = ref(false)
const resendLoading = ref(false)
const error = ref('')
const errors = ref<Record<string, string>>({})
const showConsentScreen = ref(false)
const userTokens = ref<any>(null)
const resendCountdown = ref(0)

// Store mutable versions of the route params
const currentSessionToken = ref('')
const currentChallengeType = ref<'SMS_MFA' | 'SOFTWARE_TOKEN_MFA'>('SMS_MFA')

// computed value for the MFA code
const mfaCode = computed(() => mfaDigits.value.join(''))

// Check if MFA code is complete (all 6 digits filled)
const isMfaComplete = computed(() => mfaDigits.value.every(digit => digit !== ''))

// Form data for resending code
const formData = ref({
  password: route.query.password as string || ''
})

// Get params from route - especially important to maintain username consistency
const email = computed(() => route.query.email as string)
const username = computed(() => route.query.username as string || email.value) // Ensure we handle username correctly
const sessionToken = computed(() => currentSessionToken.value || route.query.session as string)
const challengeType = computed(() => currentChallengeType.value || route.query.challenge_name as string || 'SMS_MFA') // Default to SMS_MFA if not specified
const appName = computed(() => route.query.application_name as string)
const channelId = computed(() => route.query.channel_id as string)
const redirectUrl = computed(() => route.query.redirect_url as string)

// Mask email for display
const maskedEmail = computed(() => {
  const email = route.query.email as string || username.value
  
  if (email && email.includes('@')) {
    // Mask the email but leave the first 2 characters and domain visible
    const [localPart, domain] = email.split('@')
    const firstTwo = localPart.slice(0, 2)
    const maskedPart = '*'.repeat(Math.max(localPart.length - 2, 2))
    
    return `${firstTwo}${maskedPart}@${domain}`
  }
  
  return 'your email'
})

// computed links with preserved params
const loginLink = computed(() => ({
  name: 'login',
  query: {
    application_name: appName.value,
    channel_id: channelId.value,
    redirect_url: redirectUrl.value
  }
}))

// Handle input for each digit box
const handleDigitInput = (index: number) => {
  const currentDigit = mfaDigits.value[index]
  
  // Clear errors on input
  clearErrors()
  
  // Auto-advance to next box if digit entered
  if (currentDigit && index < 5) {
    const nextInput = document.getElementById(`mfa-${index + 1}`) as HTMLInputElement
    if (nextInput) {
      nextInput.focus()
    }
  }
}

// Handle keyboard navigation between MFA boxes
const handleKeyDown = (event: KeyboardEvent, index: number) => {
  // Handle backspace
  if (event.key === 'Backspace') {
    if (!mfaDigits.value[index] && index > 0) {
      const prevInput = document.getElementById(`mfa-${index - 1}`) as HTMLInputElement
      if (prevInput) {
        prevInput.focus()
        // Optional: clear the previous input
        // mfaDigits.value[index - 1] = ''
      }
    }
  }
  // Handle left arrow key
  else if (event.key === 'ArrowLeft' && index > 0) {
    const prevInput = document.getElementById(`mfa-${index - 1}`) as HTMLInputElement
    if (prevInput) prevInput.focus()
  }
  // Handle right arrow key
  else if (event.key === 'ArrowRight' && index < 5) {
    const nextInput = document.getElementById(`mfa-${index + 1}`) as HTMLInputElement
    if (nextInput) nextInput.focus()
  }
}

// Handle paste event to distribute across input boxes
const handlePaste = (event: ClipboardEvent) => {
  event.preventDefault()
  const pastedData = event.clipboardData?.getData('text')
  if (!pastedData) return
  
  // Filter only numbers and limit to 6 digits
  const digits = pastedData.replace(/[^0-9]/g, '').slice(0, 6)
  
  // Distribute digits across input boxes
  for (let i = 0; i < digits.length; i++) {
    if (i < 6) mfaDigits.value[i] = digits[i]
  }
  
  // Focus the next empty box or the last box if all filled
  const emptyIndex = mfaDigits.value.findIndex(digit => !digit)
  const focusIndex = emptyIndex !== -1 ? emptyIndex : 5
  const inputToFocus = document.getElementById(`mfa-${focusIndex}`) as HTMLInputElement
  if (inputToFocus) inputToFocus.focus()
  
  clearErrors()
}

// form validation
const clearErrors = () => {
  error.value = ''
  errors.value = {}
}

// Create session and redirect to appropriate app (client app or admin portal)
const createSession = async (tokens: any) => {
  try {
    // User is already authorized - create session
    const sessionResponse = await api.initSession(tokens, appName.value)
    
    // Redirect with session_id
    if (sessionResponse) {
      // Check if user is admin to determine redirect location
      const isAdmin = isAdminUser(username.value)
      
      // Short delay to allow toast to be seen
      setTimeout(() => {
        // For admin users, redirect to admin portal
        if (isAdmin) {
          console.log('Admin user detected, redirecting to admin portal')
          // Update this URL to match your actual admin portal URL
          const adminPortalUrl = 'http://localhost:5174' // Default admin portal URL
          window.location.href = `${adminPortalUrl}?session_id=${sessionResponse.session_id}`
        } else {
          // For regular users, redirect to client app
          const redirectTarget = redirectUrl.value || 'http://localhost:8080'
          window.location.href = `${redirectTarget}?session_id=${sessionResponse.session_id}`
        }
      }, 1000)
    } else {
      throw new Error('Failed to create session')
    }
  } catch (err: any) {
    error.value = err.message || 'Failed to create session'
  }
}

// Consent screen handlers
const handleConsentApproved = async () => {
  if (!userTokens.value) return
  await createSession(userTokens.value)
}

const handleConsentDenied = () => {
  showConsentScreen.value = false
  error.value = 'Authorization required to access this application'
}

const handleConsentError = (errorMessage: string) => {
  showConsentScreen.value = false
  error.value = errorMessage
}

// Handle resend code with countdown
const handleResendCode = async () => {
  if (resendCountdown.value > 0 || resendLoading.value || loading.value) {
    return
  }
  
  if (!username.value || !formData.value.password) {
    error.value = 'Missing login information for resend'
    return
  }
  
  resendLoading.value = true
  clearErrors()
  
  try {
    // Call the new resendMfaCode method
    const result = await cognitoService.resendMfaCode({
      email: username.value,
      password: formData.value.password,
      applicationName: appName.value,
      channelId: channelId.value
    })
    
    // Update session token with the new one
    currentSessionToken.value = result.session
    
    // Update challenge type if it changed
    if (result.challengeName) {
      currentChallengeType.value = result.challengeName
    }
    
    // Show success toast
    toast.success('Verification code resent')
    
    // Clear any inputs
    mfaDigits.value = Array(6).fill('')
    
    // Start countdown to prevent spam (60 seconds)
    startResendCountdown()
    
  } catch (err: any) {
    console.error('Failed to resend code:', err)
    error.value = err.message || 'Failed to resend code. Please try again.'
  } finally {
    resendLoading.value = false
  }
}

// Start countdown for resend button
const startResendCountdown = () => {
  resendCountdown.value = 60 // 60 second cooldown
  const timer = setInterval(() => {
    resendCountdown.value--
    if (resendCountdown.value <= 0) {
      clearInterval(timer)
    }
  }, 1000)
}

// handle MFA verification
/**
 * Helper function to determine if a user is an admin based on username or email
 */
const isAdminUser = (username: string): boolean => {
  const lowerUsername = username.toLowerCase()
  
  // List of known admin emails
  const knownAdmins = [
    'matthew.enarle@ecloudvalley.com',
    'matt@example.com'
  ]
  
  // Check if it's one of the known admin emails
  if (knownAdmins.includes(lowerUsername)) {
    return true
  }
  
  // Check for admin patterns in the username
  return lowerUsername.includes('admin') || 
         lowerUsername.includes('test') || 
         lowerUsername.includes('matt') || 
         lowerUsername.includes('ecloudvalley')
}

/**
 * Handle MFA verification or bypass
 */
const handleMfaVerification = async () => {
  clearErrors()

  // Basic input validation
  if (!mfaCode.value) {
    errors.value.mfa = 'Verification code is required'
    return
  }

  if (mfaCode.value.length !== 6) {
    errors.value.mfa = 'Verification code must be 6 digits'
    return
  }

  if (!sessionToken.value) {
    error.value = 'Missing session token. Please try logging in again.'
    return
  }

  loading.value = true
  
  // Check if we're in development mode
  const isDevelopment = import.meta.env.MODE === 'development' || import.meta.env.VITE_NODE_ENV === 'development'
  
  // Special case: Admin user in development mode can bypass MFA verification
  if (isDevelopment && isAdminUser(username.value)) {
    console.log('DEVELOPMENT MODE: Admin user detected, using MFA bypass')
    toast.info('⚠️ DEV MODE: Admin MFA bypass active - FOR DEVELOPMENT ONLY')
    
    // Create mock tokens for development testing
    // These are minimal tokens with required fields for the flow to continue
    const mockTokens: CognitoTokens = {
      access_token: `admin-dev-bypass-${Date.now()}`,
      id_token: `admin-dev-bypass-${Date.now()}`,
      refresh_token: `admin-dev-bypass-${Date.now()}`
    }
    
    // Use the mock tokens to proceed
    userTokens.value = mockTokens
    
    try {
      // Skip the actual MFA verification
      // Just create a session directly and redirect
      await createSession(mockTokens)
      return
    } catch (err) {
      console.error('Failed to create session with mock tokens:', err)
      error.value = 'Failed to create session. Please try again.'
      loading.value = false
      return
    }
  }
  
  // Normal flow: use actual MFA verification
  try {
    const tokens = await cognitoService.verifyMfa(
      username.value, 
      mfaCode.value, 
      sessionToken.value,
      challengeType.value as 'SMS_MFA' | 'SOFTWARE_TOKEN_MFA'
    )

    // Show success toast notification
    toast.success('Verification successful!')
    
    // Set up SMS MFA for future logins (quietly, no toast notification)
    try {
      await cognitoService.setupMfa(tokens.access_token, 'sms', true)
      console.log('SMS MFA enabled for future logins')
    } catch (mfaErr) {
      console.error('Failed to set up SMS MFA:', mfaErr)
    }
    
    // Save tokens for potential consent screen
    userTokens.value = tokens
    
    // Check if admin user - bypass consent screen for admins
    if (isAdminUser(username.value)) {
      console.log('Admin user detected, bypassing consent screen')
      // Admin users bypass consent check and go directly to session creation
      await createSession(tokens)
      return
    }

    // For non-admin users, check if authorized for this application
    const authCheck = await api.checkAppUser(tokens.id_token, appName.value)
    
    if (!authCheck) {
      // User needs to authorize this application - show consent screen
      showConsentScreen.value = true
      return
    }

    // User is already authorized - create session
    await createSession(tokens)
    
  } catch (err: any) {
    error.value = err.message || 'Verification failed. Please try again.'
  } finally {
    loading.value = false
  }
}

// lifecycle
onMounted(() => {
  // validate required params
  if (!sessionToken.value || !username.value) {
    router.push({ name: 'login' })
    return
  }
  
  // Initialize our mutable versions of route params
  currentSessionToken.value = route.query.session as string
  currentChallengeType.value = (route.query.challenge_name as 'SMS_MFA' | 'SOFTWARE_TOKEN_MFA') || 'SMS_MFA'
  
  // Auto-focus the first input box
  setTimeout(() => {
    const firstInput = document.getElementById('mfa-0') as HTMLInputElement
    if (firstInput) firstInput.focus()
  }, 200)
})
</script>
