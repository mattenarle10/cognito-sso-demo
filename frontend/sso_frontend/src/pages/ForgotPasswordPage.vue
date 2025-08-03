<template>
  <AuthBackground>
    <AuthCard>
      <!-- Header with enhanced styling -->
      <div class="mb-8 relative text-center">
        <div class="absolute -top-10 -right-10 w-40 h-40 bg-gradient-to-br from-zinc-800/30 to-zinc-900/30 rounded-full blur-3xl"></div>
        <h1 class="text-4xl lg:text-5xl font-bold tracking-tight mb-4 relative">
          <span class="bg-gradient-to-r from-gray-200 via-gray-100 to-gray-300 bg-clip-text text-transparent relative inline-block">Forgot Password</span>
        </h1>
        <p class="text-zinc-500 font-light tracking-wide">Enter your email address to receive a password reset code.</p>
      </div>

      <!-- Form with enhanced styling -->
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

        <!-- Error message -->
        <div v-if="error" class="bg-red-500/10 border border-red-500/20 text-red-400 px-4 py-3 rounded-lg text-sm">
          {{ error }}
        </div>

        <!-- Success message -->
        <div v-if="success" class="bg-green-500/10 border border-green-500/20 text-green-400 px-4 py-3 rounded-lg text-sm">
          {{ success }}
        </div>

        <!-- Submit button -->
        <div class="flex justify-center">
          <AuthButton
            type="submit"
            :loading="loading"
            :disabled="!isEmailValid || loading"
            class="w-full md:w-2/3"
          >
            Send Reset Code
            <ArrowRightIcon :size="16" class="ml-1 transition-transform duration-200" />
          </AuthButton>   
        </div>
      </form>

      <!-- Footer with enhanced styling -->
      <div class="mt-6 pt-5 border-t border-zinc-800/50 relative">
        <!-- Border texture -->
        <div class="absolute top-0 left-0 right-0 h-[1px] bg-gradient-to-r from-transparent via-zinc-700/30 to-transparent" />
        <p class="text-center text-zinc-400 text-sm">
          Remember your password?
          <router-link
            to="/login"
            class="text-zinc-200 hover:text-white font-medium underline underline-offset-2 decoration-zinc-600 hover:decoration-zinc-400 transition-all duration-200 inline-flex items-center gap-1"
          >
            Back to login
            <ArrowLeftIcon :size="10" class="opacity-60" />
          </router-link>
        </p>
      </div>
    </AuthCard>
  </AuthBackground>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { MailIcon, ArrowRightIcon, ArrowLeftIcon } from 'lucide-vue-next'
import { useToast } from 'vue-toastification'

// Component setup
const router = useRouter()
const toast = useToast()

// Form data
const email = ref('')
const loading = ref(false)
const error = ref('')
const success = ref('')
const errors = ref<Record<string, string>>({})

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

    // TODO: Replace with actual Cognito forgotPassword API call
    // For now, we'll simulate the API call with a timeout
    await new Promise(resolve => setTimeout(resolve, 1500))
    
    // Show success message
    success.value = 'Reset code sent to your email. You will be redirected shortly.'
    
    // Show success toast
    toast.success('Password reset code sent!')
    
    // Redirect to reset-password page after a short delay
    setTimeout(() => {
      router.push({
        path: '/reset-password',
        query: { email: email.value }
      })
    }, 2000)
  } catch (err: any) {
    error.value = err.message || 'Failed to send reset code. Please try again.'
  } finally {
    loading.value = false
  }
}
</script>
