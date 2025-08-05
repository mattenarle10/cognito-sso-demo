<template>
  <AuthBackground>
    <AuthCard>
      <!-- Header with enhanced styling -->
      <div class="mb-8 relative text-center">
        <div class="absolute -top-10 -right-10 w-40 h-40 bg-gradient-to-br from-zinc-800/30 to-zinc-900/30 rounded-full blur-3xl"></div>
        <h1 class="text-4xl lg:text-5xl font-bold tracking-tight mb-4 relative">
          <span class="bg-gradient-to-r from-gray-200 via-gray-100 to-gray-300 bg-clip-text text-transparent relative inline-block">Password Reset</span>
        </h1>
        <p class="text-zinc-500 font-light tracking-wide">
          An administrator has reset your password. Please create a new password to continue.
        </p>
      </div>

      <!-- Form with enhanced styling -->
      <form @submit.prevent="handleSubmit" class="space-y-5">
        <AuthInput
          id="newPassword"
          type="password"
          ref="passwordInput"
          label="New Password"
          placeholder="••••••••"
          v-model="formData.newPassword"
          :required="true"
          :error="errors.newPassword"
        >
          <template #icon>
            <LockIcon :size="14" class="text-zinc-500" />
          </template>
          <template #hint>
            <div class="text-xs text-zinc-500">
              Password must have at least 8 characters with uppercase, lowercase, numbers and symbols
            </div>
          </template>
        </AuthInput>

        <AuthInput
          id="confirmPassword"
          type="password"
          label="Confirm Password"
          placeholder="••••••••"
          v-model="formData.confirmPassword"
          :required="true"
          :error="errors.confirmPassword"
        >
          <template #icon>
            <LockIcon :size="14" class="text-zinc-500" />
          </template>
        </AuthInput>

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
            Set New Password
            <ArrowRightIcon :size="16" class="ml-1 transition-transform duration-200" />
          </AuthButton>   
        </div> 
      </form>
    </AuthCard>
  </AuthBackground>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ArrowRightIcon, LockIcon } from 'lucide-vue-next'
import AuthBackground from '../components/ui/AuthBackground.vue'
import AuthCard from '../components/ui/AuthCard.vue'
import AuthInput from '../components/ui/AuthInput.vue'
import AuthButton from '../components/ui/AuthButton.vue'
import { cognitoService } from '../services/cognitoService'
import { useApi } from '../composables/useApi'
import { useToast } from 'vue-toastification'

const toast = useToast()
const route = useRoute()
const router = useRouter()
const passwordInput = ref<HTMLInputElement | null>(null)

// Form data
const formData = ref({
  newPassword: '',
  confirmPassword: ''
})

// Validation and errors
const errors = ref({
  newPassword: '',
  confirmPassword: ''
})

const loading = ref(false)
const error = ref('')

// Session data from route
const email = ref(route.query.email as string || '')
const session = ref(route.query.session as string || '')
const applicationName = ref(route.query.application_name as string || '')
const channelId = ref(route.query.channel_id as string || '')
const redirectUrl = ref(route.query.redirect_url as string || '')

// Password validation
const validatePassword = (password: string) => {
  // Check length
  if (password.length < 8) {
    return {
      valid: false,
      message: 'Password must be at least 8 characters long'
    }
  }

  // Check for uppercase letter
  if (!/[A-Z]/.test(password)) {
    return {
      valid: false,
      message: 'Password must contain at least one uppercase letter'
    }
  }

  // Check for lowercase letter
  if (!/[a-z]/.test(password)) {
    return {
      valid: false,
      message: 'Password must contain at least one lowercase letter'
    }
  }

  // Check for number
  if (!/[0-9]/.test(password)) {
    return {
      valid: false,
      message: 'Password must contain at least one number'
    }
  }

  // Check for special character
  if (!/[^A-Za-z0-9]/.test(password)) {
    return {
      valid: false,
      message: 'Password must contain at least one special character'
    }
  }

  // All checks passed
  return {
    valid: true,
    message: 'Password meets all requirements'
  }
}

// Check form validity
const isFormValid = computed(() => {
  return formData.value.newPassword && 
         formData.value.confirmPassword && 
         formData.value.newPassword === formData.value.confirmPassword &&
         validatePassword(formData.value.newPassword).valid
})

onMounted(() => {
  // Check if we have the required email parameter
  if (!email.value) {
    error.value = 'Missing email information. Please return to the login page.'
  }
  
  // Note: We don't require session anymore as we handle both session-based and code-based flows
})

// Get verification code from query params (for code-based flow)
const verificationCode = ref(route.query.code as string || '')

// Handle form submission
const handleSubmit = async () => {
  // Clear any previous errors
  errors.value.newPassword = ''
  errors.value.confirmPassword = ''
  error.value = ''

  // Validate passwords match
  if (formData.value.newPassword !== formData.value.confirmPassword) {
    errors.value.confirmPassword = 'Passwords do not match'
    return
  }

  // Validate password strength
  const passwordValidation = validatePassword(formData.value.newPassword)
  if (!passwordValidation.valid) {
    errors.value.newPassword = passwordValidation.message
    return
  }

  try {
    loading.value = true
    let tokens = null
    
    // Determine which flow to use based on available parameters
    if (session.value) {
      // Session-based flow (NEW_PASSWORD_REQUIRED challenge)
      console.log('[ForcePasswordReset] Using session-based flow with NEW_PASSWORD_REQUIRED challenge')
      tokens = await cognitoService.respondToNewPasswordRequired({
        email: email.value,
        session: session.value,
        newPassword: formData.value.newPassword,
        applicationName: applicationName.value,
        channelId: channelId.value
      })
    } else if (verificationCode.value) {
      // Code-based flow (ForgotPassword flow)
      console.log('[ForcePasswordReset] Using code-based flow with verification code')
      await cognitoService.confirmForgotPassword({
        email: email.value,
        code: verificationCode.value,
        newPassword: formData.value.newPassword,
        applicationName: applicationName.value,
        channelId: channelId.value
      })
      // No tokens returned from confirmForgotPassword, user will need to log in again
    } else {
      // No session or code - initiate forgot password flow
      console.log('[ForcePasswordReset] No session or code available, initiating forgot password flow')
      await cognitoService.forgotPassword({
        email: email.value,
        applicationName: applicationName.value,
        channelId: channelId.value
      })
      
      toast.info('A verification code has been sent to your email. Please check your inbox and enter the code to reset your password.')
      
      // Redirect to the regular reset password page
      router.push({
        name: 'reset-password',
        query: {
          email: email.value,
          application_name: applicationName.value,
          channel_id: channelId.value,
          redirect_url: redirectUrl.value
        }
      })
      return
    }

    // Show success message
    toast.success('Password has been successfully updated!')

    // If we have a redirect URL and application name, initialize a session
    if (redirectUrl.value && applicationName.value) {
      try {
        const api = useApi()
        const sessionResponse = await api.initSession(tokens, applicationName.value)
        
        // Redirect back to client app with session_id
        if (sessionResponse && sessionResponse.session_id) {
          setTimeout(() => {
            window.location.href = `${redirectUrl.value}?session_id=${sessionResponse.session_id}`
          }, 1000)
          return
        }
      } catch (err: any) {
        console.error('Session initialization error:', err)
        // Continue with normal login flow if session init fails
      }
    }

    // If no redirect URL or session init failed, redirect to home/dashboard
    setTimeout(() => {
      router.push('/')
    }, 1000)

  } catch (err: any) {
    console.error('Password reset error:', err)
    
    // Clear password fields
    formData.value.newPassword = ''
    formData.value.confirmPassword = ''
    
    // Focus on password field
    setTimeout(() => {
      passwordInput.value?.focus()
    }, 100)
    
    // Display error
    error.value = err.message || 'Failed to update password. Please try again.'
  } finally {
    loading.value = false
  }
}

// Hook to validate password complexity as user types
const validatePasswordComplexity = () => {
  if (formData.value.newPassword) {
    const validation = validatePassword(formData.value.newPassword)
    if (!validation.valid) {
      errors.value.newPassword = validation.message
    } else {
      errors.value.newPassword = ''
    }
  }
}
</script>

<style scoped>
/* All styles are handled with Tailwind classes */
</style>
