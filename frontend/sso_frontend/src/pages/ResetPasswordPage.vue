<template>
  <AuthBackground>
    <AuthCard>
      <!-- Header with standard styling -->
      <div class="mb-4 relative text-center">
        <div class="absolute -top-10 -right-10 w-40 h-40 bg-gradient-to-br from-zinc-800/30 to-zinc-900/30 rounded-full blur-3xl"></div>
        <h1 class="text-3xl font-bold tracking-tight mb-1 relative">
          <span class="bg-gradient-to-r from-gray-200 via-gray-100 to-gray-300 bg-clip-text text-transparent relative inline-block">Reset Password</span>
        </h1>
        <p class="text-zinc-500 text-sm font-light tracking-wide" v-if="appName">to continue to {{ appName }}</p>
        <p v-if="isAdminReset" class="text-zinc-400 text-sm mt-2 bg-zinc-800/50 py-2 px-3 rounded-lg inline-block">
          <span class="text-zinc-300">Admin reset:</span> Enter the verification code from your email
        </p>
        <p class="text-zinc-400 text-sm mt-3 bg-zinc-800/50 py-2 px-3 rounded-lg inline-block">
          <span class="text-zinc-300">Code sent to:</span> {{ email }}
        </p>
      </div>

      <!-- Form with standard styling -->
      <form @submit.prevent="handleResetPassword" class="space-y-5">
        <!-- Verification Code Input Boxes -->
        <div>
          <label for="code" class="block text-sm font-medium text-zinc-400 mb-1">Verification Code</label>
          <div class="flex justify-center gap-2 mt-2">
            <div 
              v-for="(_, index) in 6" 
              :key="index"
              class="relative"
            >
              <input
                type="text"
                maxlength="1"
                :id="`reset-code-${index}`"
                v-model="codeDigits[index]"
                @input="handleCodeInput(index)"
                @keydown="handleKeyDown($event, index)"
                @paste="handlePaste"
                class="w-11 h-14 bg-zinc-900/60 border border-zinc-700/60 text-white text-center text-xl font-medium rounded-lg focus:border-zinc-400 focus:ring-1 focus:ring-zinc-400 transition-all duration-200"
              />
              <div class="absolute inset-0 bg-gradient-to-r from-zinc-800/5 to-transparent rounded-lg pointer-events-none" />
            </div>
          </div>
          <p v-if="errors.code" class="text-red-400 text-xs mt-2 text-center">{{ errors.code }}</p>
        </div>

        <!-- New Password -->
        <AuthInput
          id="password"
          type="password"
          label="New Password"
          placeholder="••••••••"
          v-model="password"
          :required="true"
          :error="errors.password"
        >
          <template #icon>
            <LockIcon :size="14" class="text-zinc-500" />
          </template>
        </AuthInput>

        <!-- Password Validation Requirements -->
        <div class="bg-zinc-800/50 rounded-lg p-3 border border-zinc-700/50">
          <p class="text-sm text-zinc-400 mb-2">Password requirements:</p>
          <div class="grid grid-cols-1 md:grid-cols-2 gap-x-4 gap-y-1">
            <div class="flex items-center">
              <div :class="passwordHasMinLength ? 'text-green-500' : 'text-zinc-600'" class="mr-2">
                <CheckIcon v-if="passwordHasMinLength" :size="14" />
                <XIcon v-else :size="14" />
              </div>
              <span :class="passwordHasMinLength ? 'text-zinc-300' : 'text-zinc-500'" class="text-xs">At least 8 characters</span>
            </div>
            <div class="flex items-center">
              <div :class="passwordHasUppercase ? 'text-green-500' : 'text-zinc-600'" class="mr-2">
                <CheckIcon v-if="passwordHasUppercase" :size="14" />
                <XIcon v-else :size="14" />
              </div>
              <span :class="passwordHasUppercase ? 'text-zinc-300' : 'text-zinc-500'" class="text-xs">One uppercase letter</span>
            </div>
            <div class="flex items-center">
              <div :class="passwordHasLowercase ? 'text-green-500' : 'text-zinc-600'" class="mr-2">
                <CheckIcon v-if="passwordHasLowercase" :size="14" />
                <XIcon v-else :size="14" />
              </div>
              <span :class="passwordHasLowercase ? 'text-zinc-300' : 'text-zinc-500'" class="text-xs">One lowercase letter</span>
            </div>
            <div class="flex items-center">
              <div :class="passwordHasNumber ? 'text-green-500' : 'text-zinc-600'" class="mr-2">
                <CheckIcon v-if="passwordHasNumber" :size="14" />
                <XIcon v-else :size="14" />
              </div>
              <span :class="passwordHasNumber ? 'text-zinc-300' : 'text-zinc-500'" class="text-xs">One number</span>
            </div>
            <div class="flex items-center">
              <div :class="passwordHasSpecial ? 'text-green-500' : 'text-zinc-600'" class="mr-2">
                <CheckIcon v-if="passwordHasSpecial" :size="14" />
                <XIcon v-else :size="14" />
              </div>
              <span :class="passwordHasSpecial ? 'text-zinc-300' : 'text-zinc-500'" class="text-xs">One special character</span>
            </div>
          </div>
        </div>

        <!-- Confirm Password -->
        <AuthInput
          id="confirmPassword"
          type="password"
          label="Confirm Password"
          placeholder="••••••••"
          v-model="confirmPassword"
          :required="true"
          :error="errors.confirmPassword"
        >
          <template #icon>
            <LockIcon :size="14" class="text-zinc-500" />
          </template>
        </AuthInput>

        <!-- Submit Button -->
        <AuthButton
          type="submit"
          :loading="loading"
          :disabled="!isFormValid || loading"
          class="w-full"
        >
          <span class="flex items-center justify-center gap-2">
            Reset Password
            <ArrowRightIcon :size="16" />
          </span>
        </AuthButton>

        <!-- Back and resend links -->
        <div class="flex flex-col items-center gap-2 pt-1">
          <router-link 
            to="/forgot-password"
            class="text-zinc-500 hover:text-zinc-400 text-xs transition-colors duration-200"
          >
            Request a new code
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
import { ref, computed, onMounted, nextTick } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { LockIcon, CheckIcon, XIcon, ArrowRightIcon } from 'lucide-vue-next'
import { useToast } from 'vue-toastification'
import AuthBackground from '../components/ui/AuthBackground.vue'
import AuthCard from '../components/ui/AuthCard.vue'
import AuthInput from '../components/ui/AuthInput.vue'
import AuthButton from '../components/ui/AuthButton.vue'
import { cognitoService } from '../services/cognitoService'

// Component setup
const route = useRoute()
const router = useRouter()
const toast = useToast()

// Get params from route
const appName = computed(() => route.query.application_name as string)
const channelId = computed(() => route.query.channel_id as string)
const redirectUrl = computed(() => route.query.redirect_url as string)

// Form data
const email = ref('')
const codeDigits = ref<string[]>(Array(6).fill(''))
const password = ref('')
const confirmPassword = ref('')
const loading = ref(false)
const error = ref('')
const success = ref('')
const errors = ref<Record<string, string>>({})

// Computed property to check if this is an admin-initiated reset
const isAdminReset = computed(() => route.query.admin_reset === 'true')

// On component mount, get query params from URL and set up form
onMounted(() => {
  email.value = route.query.email as string || ''
  
  // We don't need to show a toast here since we already show one in LoginPage.vue
  // The visual indicator in the UI is sufficient
  
  // Focus first input field
  nextTick(() => {
    const firstInput = document.getElementById('reset-code-0') as HTMLInputElement
    if (firstInput) {
      firstInput.focus()
    }
  })
})

// Password validation computed properties
const passwordHasMinLength = computed(() => password.value.length >= 8)
const passwordHasUppercase = computed(() => /[A-Z]/.test(password.value))
const passwordHasLowercase = computed(() => /[a-z]/.test(password.value))
const passwordHasNumber = computed(() => /[0-9]/.test(password.value))
const passwordHasSpecial = computed(() => /[!@#$%^&*(),.?":{}|<>]/.test(password.value))

const passwordIsValid = computed(() => 
  passwordHasMinLength.value && 
  passwordHasUppercase.value && 
  passwordHasLowercase.value && 
  passwordHasNumber.value && 
  passwordHasSpecial.value
)

const isFormValid = computed(() => {
  const verificationCode = codeDigits.value.join('').trim()
  return email.value && verificationCode.length === 6 && passwordIsValid.value && password.value === confirmPassword.value
})

// Methods for verification code input handling
const handleCodeInput = (index: number) => {
  const value = codeDigits.value[index]
  
  // Only allow numbers
  if (!/^\d*$/.test(value)) {
    codeDigits.value[index] = ''
    return
  }
  
  // Move to next input
  if (value && index < 5) {
    const nextInput = document.getElementById(`reset-code-${index + 1}`) as HTMLInputElement
    if (nextInput) nextInput.focus()
  }
}

const handleKeyDown = (event: KeyboardEvent, index: number) => {
  // If backspace is pressed and current input is empty, focus previous input
  if (event.key === 'Backspace' && !codeDigits.value[index] && index > 0) {
    const prevInput = document.getElementById(`reset-code-${index - 1}`) as HTMLInputElement
    if (prevInput) prevInput.focus()
  }
}

const handlePaste = (event: ClipboardEvent) => {
  event.preventDefault()
  const pasteData = event.clipboardData?.getData('text')
  if (!pasteData || !/^\d+$/.test(pasteData)) return
  
  // Fill in as many digits as we can
  const digits = pasteData.slice(0, 6).split('')
  codeDigits.value = [...digits, ...Array(6 - digits.length).fill('')]
  
  // Focus on appropriate input
  if (digits.length < 6) {
    const nextInput = document.getElementById(`reset-code-${digits.length}`) as HTMLInputElement
    if (nextInput) nextInput.focus()
  }
}

// Form submission
const handleResetPassword = async () => {
  // Reset error state
  error.value = ''
  success.value = ''
  errors.value = {}
  
  // Validate form
  if (!email.value) {
    errors.value.email = 'Email address is required'
    return
  }
  
  const verificationCode = codeDigits.value.join('').trim()
  if (verificationCode.length !== 6) {
    errors.value.code = 'Please enter the 6-digit verification code'
    return
  }
  
  if (!passwordIsValid.value) {
    errors.value.password = 'Password does not meet all requirements'
    return
  }
  
  if (password.value !== confirmPassword.value) {
    errors.value.confirmPassword = 'Passwords do not match'
    return
  }
  
  try {
    loading.value = true
    
    // Call Cognito confirmForgotPassword API
    await cognitoService.confirmForgotPassword({
      email: email.value,
      code: verificationCode,
      newPassword: password.value,
      applicationName: appName.value,
      channelId: channelId.value
    })
    
    // Show success message
    success.value = 'Password successfully reset. Redirecting to login...'
    
    // Show success toast
    toast.success('Password successfully reset!')
    
    // Redirect to login page after a short delay
    setTimeout(() => {
      router.push({
        path: '/login',
        query: { 
          verified: 'password_reset',
          application_name: appName.value,
          channel_id: channelId.value,
          redirect_url: redirectUrl.value
        }
      })
    }, 2000)
  } catch (err: any) {
    // Check if this is a password reuse error
    if (err.message && err.message.includes('cannot reuse a previous password')) {
      error.value = err.message
      // Reset password fields to allow the user to enter a new password
      password.value = ''
      confirmPassword.value = ''
      // Focus on password field
      nextTick(() => {
        document.getElementById('password')?.focus()
      })
    } else {
      error.value = err.message || 'Failed to reset password. Please try again.'
    }
  } finally {
    loading.value = false
  }
}
</script>
