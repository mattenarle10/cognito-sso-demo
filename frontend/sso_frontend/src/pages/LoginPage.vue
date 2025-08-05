<template>
  <AuthBackground>
    <AuthCard>
      <!-- Header with enhanced styling -->
      <div class="mb-8 relative text-center">
        <div class="absolute -top-10 -right-10 w-40 h-40 bg-gradient-to-br from-zinc-800/30 to-zinc-900/30 rounded-full blur-3xl"></div>
        <h1 class="text-4xl lg:text-5xl font-bold tracking-tight mb-4 relative">
          <span class="bg-gradient-to-r from-gray-200 via-gray-100 to-gray-300 bg-clip-text text-transparent relative inline-block">The Grind.</span>
        </h1>
        <p class="text-zinc-500 font-light tracking-wide" v-if="appName">Continue with your brewed account. </p>

        <p class="text-zinc-500 font-light tracking-wide" v-else>Continue with your brewed account. </p>
      </div>

      <!-- Form with enhanced styling -->
      <form @submit.prevent="handleLogin" class="space-y-5">
        <AuthInput
          id="email"
          type="email"
          label="Email Address"
          placeholder="your@email.com"
          v-model="formData.email"
          :required="true"
          :error="errors.email"
        >
          <template #icon>
            <MailIcon :size="14" class="text-zinc-500" />
          </template>
        </AuthInput>

        <AuthInput
          id="password"
          type="password"
          label="Password"
          placeholder="••••••••"
          v-model="formData.password"
          :required="true"
          :error="errors.password"
        >
          <template #icon>
            <LockIcon :size="14" class="text-zinc-500" />
          </template>
        </AuthInput>

        <!-- Forgot password link -->
        <div class="flex justify-end -mt-2">
          <router-link 
            to="/forgot-password"
            class="text-sm text-zinc-400 hover:text-zinc-200 transition-colors duration-200 font-medium"
          >
            Forgot password?
          </router-link>
        </div>


        <!-- Error message -->
        <div v-if="error" class="bg-red-500/10 border border-red-500/20 text-red-400 px-4 py-3 rounded-lg text-sm">
          {{ error }}
        </div>

        <!-- Submit button with enhanced styling -->
        <div class="flex justify-center">
          <AuthButton
            type="submit"
            :loading="loading"
            :disabled="!isFormValid || loading"
            class="w-full md:w-2/3"
          >
            Login
            <ArrowRightIcon :size="16" class="ml-1 transition-transform duration-200" />
          </AuthButton>   
        </div> 
      </form>
      
          <!-- Divider with text -->
  <div class="flex items-center my-6">
    <div class="flex-grow border-t border-zinc-700/40"></div>
    <span class="mx-4 text-zinc-500 text-xs uppercase tracking-widest">or continue with</span>
    <div class="flex-grow border-t border-zinc-700/40"></div>
  </div>

  <!-- Google Login Button centered -->
  <div class="flex justify-center">
    <GoogleLoginButton />
  </div>


      <!-- Footer with enhanced styling -->
      <div class="mt-6 pt-5 border-t border-zinc-800/50 relative">
        <!-- Border texture -->
        <div class="absolute top-0 left-0 right-0 h-[1px] bg-gradient-to-r from-transparent via-zinc-700/30 to-transparent" />
        <p class="text-center text-zinc-400 text-sm">
          Don't have an account?
          <router-link
            :to="registerLink"
            class="text-zinc-200 hover:text-white font-medium underline underline-offset-2 decoration-zinc-600 hover:decoration-zinc-400 transition-all duration-200 inline-flex items-center gap-1"
          >
            Create your account
            <ArrowRightIcon :size="10" class="opacity-60" />
          </router-link>
        </p>
      </div>
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
import GoogleLoginButton from '../components/ui/GoogleLoginButton.vue'
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { MailIcon, LockIcon, ArrowRightIcon } from 'lucide-vue-next'
import type { LoginCredentials, MfaChallenge, CognitoTokens, AuthResult } from '../types/auth'
import { cognitoService } from '../services/cognitoService'
import { useApi } from '../composables/useApi'
import AuthBackground from '../components/ui/AuthBackground.vue'
import AuthCard from '../components/ui/AuthCard.vue'
import AuthInput from '../components/ui/AuthInput.vue'
import AuthButton from '../components/ui/AuthButton.vue'
import ConsentScreen from '../components/ConsentScreen.vue'
import { useToast } from 'vue-toastification'

// Form data
const formData = ref<LoginCredentials>({
  email: '',
  password: ''
})

// State
const loading = ref(false)
const error = ref('')
const errors = ref<Record<string, string>>({})
const showConsentScreen = ref(false)
const userTokens = ref<any>(null)

// Route handling for URL parameters
const route = useRoute()
const router = useRouter()
const api = useApi()
const toast = useToast()
const appName = ref('')
const channelId = ref('')

// URL parameters from client app redirect
onMounted(() => {
  appName.value = route.query.application_name as string || ''
  channelId.value = route.query.channel_id as string || ''
  
  // Check if user just verified their email
  if (route.query.verified === 'true') {
    toast.success('Email verified! Welcome to The Grind.')
  }
  
  // todo: validate app/channel with backend
  console.log('App:', appName.value, 'Channel:', channelId.value)
})

// Computed
const isFormValid = computed(() => {
  return formData.value.email && formData.value.password
})

const registerLink = computed(() => {
  const query = route.query
  return { name: 'register', query }
})

/**
 * Helper function to determine if a user is an admin based on username or email
 */
const isAdminUser = (username: string): boolean => {
  const lowerUsername = username.toLowerCase()
  
  // List of known admin emails - ONLY these emails should be admins
  const knownAdmins = [
    'matthew.enarle@ecloudvalley.com',
  ]
  
  // ONLY check against the explicit list of admin emails
  // No pattern matching to avoid false positives
  return knownAdmins.includes(lowerUsername)
}

// Methods
const handleLogin = async () => {
  loading.value = true
  error.value = ''

  // DEVELOPMENT ONLY - Store password for potential MFA bypass
  const isDevelopment = import.meta.env.MODE === 'development' || import.meta.env.VITE_NODE_ENV === 'development'
  
  if (isDevelopment) {
    // Only store password temporarily in dev environment for MFA bypass
    localStorage.setItem('dev_password', formData.value.password)
    console.log('DEV MODE: Temporarily storing password for MFA bypass')
    
    // Set a timeout to clear the password after 5 minutes
    setTimeout(() => {
      localStorage.removeItem('dev_password')
      console.log('DEV MODE: Cleared temporary password')
    }, 5 * 60 * 1000) // 5 minutes
  }

  try {
    const result = await cognitoService.signIn({
      email: formData.value.email,
      password: formData.value.password,
      applicationName: appName.value,
      channelId: channelId.value
    })

    // Check if NEW_PASSWORD_REQUIRED challenge is required (admin forced reset)
    if ('challengeName' in result && result.challengeName === 'NEW_PASSWORD_REQUIRED') {
      console.log('[Login] NEW_PASSWORD_REQUIRED challenge detected - redirecting to forced password reset')
      
      // Redirect to forced password reset page
      router.push({
        name: 'force-password-reset',
        query: {
          email: formData.value.email,
          session: result.session,
          application_name: appName.value,
          channel_id: channelId.value,
          redirect_url: route.query.redirect_url as string
        }
      })
      return
    }
    
    // Check if MFA verification is required
    if ('challengeName' in result && (result.challengeName === 'SMS_MFA' || result.challengeName === 'SOFTWARE_TOKEN_MFA')) {
      // Determine the destination for the code (phone or email)
      const destination = result.challengeParameters?.['CODE_DELIVERY_DESTINATION'] || ''
      
      // Redirect to MFA verification page with required parameters
      router.push({
        name: 'mfa-verify',
        query: {
          username: formData.value.email,
          email: formData.value.email, // Also pass email for consistency
          session: result.session,
          challenge_name: result.challengeName, // Pass the specific challenge type
          application_name: appName.value,
          channel_id: channelId.value,
          redirect_url: route.query.redirect_url as string,
          phone: result.challengeName === 'SMS_MFA' ? destination : undefined
        }
      })
      return
    }
    
    // If we get here, standard authentication without MFA
    const tokens = result as any // The result contains tokens
    
    // Store tokens in localStorage immediately after login
    // This ensures they're available throughout the flow
    if (tokens.id_token) localStorage.setItem('id_token', tokens.id_token)
    if (tokens.access_token) localStorage.setItem('access_token', tokens.access_token)
    if (tokens.refresh_token) localStorage.setItem('refresh_token', tokens.refresh_token)

    // Check if user is admin - THIS CHECK MUST COME FIRST
    // This must override any URL parameters
    if (isAdminUser(formData.value.email)) {
      console.log('%c ADMIN USER DETECTED - OVERRIDE ALL OTHER LOGIC', 'background: #ff0000; color: white; font-size: 20px;')
      console.log('Current URL:', window.location.href)
      console.log('Query params:', route.query)
      
      // For admin users, we use the admin-portal application ID instead of client app
      const adminAppId = 'admin-portal'
      
      try {
        // Create session using the admin-portal application ID
        console.log('Creating admin session with application ID:', adminAppId)
        const sessionResponse = await api.initSession(tokens, adminAppId)
        console.log('Admin session response:', sessionResponse)

        if (sessionResponse && sessionResponse.session_id) {
          // Log success with session ID
          console.log('%c ADMIN SESSION CREATED SUCCESSFULLY', 'background: #00ff00; color: black; font-size: 20px;')
          console.log('Session ID:', sessionResponse.session_id)
          
          // Admin portal URL - must be absolute URL
          const adminPortalUrl = 'http://localhost:5174'
          const redirectUrl = `${adminPortalUrl}?session_id=${sessionResponse.session_id}`
          
          console.log('%c REDIRECTING TO ADMIN PORTAL NOW', 'background: #0000ff; color: white; font-size: 20px;')
          console.log('Redirect URL:', redirectUrl)
          
          // Show success toast
          toast.success('Admin login successful!')
          
          // Give the toast time to appear before redirecting
          setTimeout(() => {
            try {
              // Use a hard redirect for cleanest experience
              window.location.replace(redirectUrl)
            } catch (error) {
              console.error('Redirect error:', error)
              // Fallback to window.location.href
              window.location.href = redirectUrl
            }
          }, 1000)
          
          return // Stop execution here
        } else {
          console.error('No session ID returned from API')
          throw new Error('Failed to create admin session - no session ID returned')
        }
      } catch (err) {
        console.error('Admin session creation error:', err)
        error.value = 'Admin login failed. Please make sure the admin-portal application is set up in DynamoDB.'
      }
      return
    }

    // For non-admin users, check if authorized for this application
    const authCheck = await api.checkAppUser(tokens.id_token, appName.value)
    
    if (!authCheck) {
      // user needs to authorize this application - show consent screen
      showConsentScreen.value = true
      userTokens.value = tokens
      loading.value = false
      return
    }

    // user is already authorized - create session
    const sessionResponse = await api.initSession(tokens, appName.value)

    // Show success toast notification
    toast.success('Welcome back to The Grind!')
    
    // redirect back to client app with session_id
    if (sessionResponse) {
      // Short delay to allow toast to be seen
      setTimeout(() => {
        const redirectUrl = route.query.redirect_url as string || 'http://localhost:8080'
        window.location.href = `${redirectUrl}?session_id=${sessionResponse.session_id}`
      }, 1000)
    } else {
      throw new Error('failed to create session')
    }
    
  } catch (err: any) {
    error.value = err.message || 'login failed'
  } finally {
    loading.value = false
  }
}

// consent screen handlers
const handleConsentApproved = async (scopes: string[]) => {
  try {
    loading.value = true
    showConsentScreen.value = false
    
    // small delay to ensure authorization record is fully created
    await new Promise(resolve => setTimeout(resolve, 500))
    
    // We don't need to refresh tokens before creating session
    // The backend will automatically refresh tokens when creating a new session
    // if they're expired or about to expire
    let tokens = userTokens.value
    
    // authorization was already created by the consent screen
    // now create session with the potentially refreshed tokens
    const sessionResponse = await api.initSession(tokens, appName.value)
    
    toast.success('Welcome to The Grind!')
    
    // redirect back to client app with session_id
    if (sessionResponse && sessionResponse.session_id) {
      setTimeout(() => {
        const redirectUrl = route.query.redirect_url as string || 'http://localhost:8080'
        window.location.href = `${redirectUrl}?session_id=${sessionResponse.session_id}`
      }, 1000)
    } else {
      throw new Error('failed to create session')
    }
  } catch (err: any) {
    error.value = err.message || 'authorization failed'
  } finally {
    loading.value = false
  }
}

const handleConsentDenied = () => {
  showConsentScreen.value = false
  error.value = 'authorization required to access this application'
}

const handleConsentError = (errorMessage: string) => {
  showConsentScreen.value = false
  error.value = errorMessage
}
</script>

<style>
/* All styles are now handled with Tailwind classes */
</style> 