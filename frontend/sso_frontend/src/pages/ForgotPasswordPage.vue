<template>
  <AuthBackground>
    <AuthCard>
      <!-- Header with enhanced styling -->
      <div class="mb-4 relative text-center">
        <div class="absolute -top-10 -right-10 w-40 h-40 bg-gradient-to-br from-zinc-800/30 to-zinc-900/30 rounded-full blur-3xl"></div>
        <h1 class="text-3xl font-bold tracking-tight mb-1 relative">
          <span class="bg-gradient-to-r from-gray-200 via-gray-100 to-gray-300 bg-clip-text text-transparent relative inline-block">Forgot Password</span>
        </h1>
        <p class="text-zinc-500 text-sm font-light tracking-wide" v-if="appName">to continue to {{ appName }}</p>
      </div>

      <!-- Form with standard styling -->
      <form @submit.prevent="handleForgotPassword" class="space-y-5">
        <AuthInput
          id="email"
          type="email"
          label="Email Address"
          placeholder="your@email.com"
          v-model="email"
          :required="true"
          :error="errors.email"
        >
          <template #icon>
            <MailIcon :size="14" class="text-zinc-500" />
          </template>
        </AuthInput>

        <!-- Submit Button -->
        <AuthButton
          type="submit"
          :loading="loading"
          :disabled="!isEmailValid || loading"
          class="w-full"
        >
          <span class="flex items-center justify-center gap-2">
            Send Reset Code
            <ArrowRightIcon :size="16" />
          </span>
        </AuthButton>

        <!-- Back to Login Link -->
        <div class="flex flex-col items-center gap-2 pt-1">
          <router-link 
            to="/login" 
            class="text-zinc-500 hover:text-zinc-400 text-xs transition-colors duration-200"
          >
            Return to login
          </router-link>
        </div>

        <!-- Error Display -->
        <div v-if="error" class="bg-red-900/20 border border-red-800/50 text-red-400 text-xs py-2 px-3 rounded-lg mt-2">
          {{ error }}
        </div>

        <!-- Success message -->
        <div v-if="success" class="bg-green-900/20 border border-green-800/50 text-green-400 text-xs py-2 px-3 rounded-lg mt-2">
          {{ success }}
        </div>
      </form>
    </AuthCard>
  </AuthBackground>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { MailIcon, ArrowRightIcon } from 'lucide-vue-next'
import { useToast } from 'vue-toastification'
import AuthBackground from '../components/ui/AuthBackground.vue'
import AuthCard from '../components/ui/AuthCard.vue'
import AuthInput from '../components/ui/AuthInput.vue'
import AuthButton from '../components/ui/AuthButton.vue'
import { cognitoService } from '../services/cognitoService'

// Component setup
const router = useRouter()
const route = useRoute()
const toast = useToast()

// Form data
const email = ref('')
const loading = ref(false)
const error = ref('')
const success = ref('')
const errors = ref<Record<string, string>>({})

// Get params from route
const appName = computed(() => route.query.application_name as string)
const channelId = computed(() => route.query.channel_id as string)
const redirectUrl = computed(() => route.query.redirect_url as string)

// Computed
const isEmailValid = computed(() => {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
  return emailRegex.test(email.value)
})

// Methods
const handleForgotPassword = async () => {
  // Reset state
  error.value = ''
  success.value = ''
  errors.value = {}
  
  // Validate email
  if (!isEmailValid.value) {
    errors.value.email = 'Please enter a valid email address'
    return
  }

  try {
    loading.value = true

    // First check if the email exists in Cognito
    try {
      // Call Cognito forgotPassword API
      await cognitoService.forgotPassword({
        email: email.value,
        applicationName: appName.value,
        channelId: channelId.value
      })
      
      // If we get here, the email exists in Cognito
      // Show success message
      success.value = 'Reset code sent to your email. You will be redirected shortly.'
      
      // Show success toast
      toast.success('Password reset code sent!')
      
      // Redirect to reset-password page after a short delay
      setTimeout(() => {
        router.push({
          path: '/reset-password',
          query: { 
            email: email.value,
            application_name: appName.value,
            channel_id: channelId.value,
            redirect_url: redirectUrl.value
          }
        })
      }, 2000)
    } catch (cognitoError: any) {
      // Check if the error is UserNotFoundException
      if (cognitoError.name === 'UserNotFoundException' || 
          cognitoError.message?.toLowerCase().includes('user not found')) {
        error.value = 'No account found with this email address. Please check your email or sign up.'
      } else {
        // For other errors, pass through to the outer catch block
        throw cognitoError
      }
    }
  } catch (err: any) {
    error.value = err.message || 'Failed to send reset code. Please try again.'
  } finally {
    loading.value = false
  }
}
</script>
