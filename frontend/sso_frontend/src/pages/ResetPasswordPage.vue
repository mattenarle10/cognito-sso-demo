<template>
  <AuthBackground>
    <AuthCard>
      <!-- Header with enhanced styling -->
      <div class="mb-8 relative text-center">
        <div class="absolute -top-10 -right-10 w-40 h-40 bg-gradient-to-br from-zinc-800/30 to-zinc-900/30 rounded-full blur-3xl"></div>
        <h1 class="text-4xl lg:text-5xl font-bold tracking-tight mb-4 relative">
          <span class="bg-gradient-to-r from-gray-200 via-gray-100 to-gray-300 bg-clip-text text-transparent relative inline-block">Reset Password</span>
        </h1>
        <p class="text-zinc-500 font-light tracking-wide">Enter the verification code sent to your email and create a new password.</p>
      </div>

      <!-- Form with enhanced styling -->
      <form @submit.prevent="handleResetPassword" class="space-y-5">
        <!-- Email display (readonly) -->
        <AuthInput
          id="email"
          type="email"
          label="Email Address"
          v-model="email"
          :required="true"
          :disabled="true"
          class="cursor-not-allowed opacity-70"
          readonly
        >
          <template #icon>
            <MailIcon :size="14" class="text-zinc-500" />
          </template>
        </AuthInput>

        <!-- Verification Code -->
        <div>
          <label for="code" class="block text-sm font-medium text-zinc-400 mb-1">Verification Code</label>
          <div class="flex items-center justify-center space-x-2">
            <template v-for="(_, index) in 6" :key="index">
              <input
                type="text"
                maxlength="1"
                v-model="codeDigits[index]"
                @input="handleCodeInput(index, $event)"
                @keydown="handleKeyDown($event, index)"
                @paste="handlePaste"
                class="w-12 h-12 rounded-lg bg-zinc-800/80 border border-zinc-700/80 text-center text-xl font-medium text-white focus:ring-2 focus:ring-blue-500/70 focus:border-blue-500/70 focus:outline-none transition-all duration-200"
                :class="{ 'border-red-500': errors.code }"
                ref="codeInputRefs"
              />
            </template>
          </div>
          <p v-if="errors.code" class="mt-1 text-sm text-red-400">{{ errors.code }}</p>
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
            :disabled="!isFormValid || loading"
            class="w-full md:w-2/3"
          >
            Reset Password
            <ArrowRightIcon :size="16" class="ml-1 transition-transform duration-200" />
          </AuthButton>   
        </div>
      </form>

      <!-- Footer with enhanced styling -->
      <div class="mt-6 pt-5 border-t border-zinc-800/50 relative">
        <!-- Border texture -->
        <div class="absolute top-0 left-0 right-0 h-[1px] bg-gradient-to-r from-transparent via-zinc-700/30 to-transparent" />
        <p class="text-center text-zinc-400 text-sm">
          <router-link
            to="/forgot-password"
            class="text-zinc-200 hover:text-white font-medium underline underline-offset-2 decoration-zinc-600 hover:decoration-zinc-400 transition-all duration-200 inline-flex items-center gap-1"
          >
            <ArrowLeftIcon :size="10" class="opacity-60" />
            Request a new code
          </router-link>
        </p>
      </div>
    </AuthCard>
  </AuthBackground>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, nextTick } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { MailIcon, LockIcon, CheckIcon, XIcon, ArrowRightIcon, ArrowLeftIcon } from 'lucide-vue-next'
import { useToast } from 'vue-toastification'

// Component setup
const route = useRoute()
const router = useRouter()
const toast = useToast()
const codeInputRefs = ref<HTMLInputElement[]>([])

// Form data
const email = ref('')
const codeDigits = ref<string[]>(Array(6).fill(''))
const password = ref('')
const confirmPassword = ref('')
const loading = ref(false)
const error = ref('')
const success = ref('')
const errors = ref<Record<string, string>>({})

// On component mount, set email from query param
onMounted(() => {
  email.value = route.query.email as string || ''
  
  // Focus first input field
  nextTick(() => {
    if (codeInputRefs.value[0]) {
      codeInputRefs.value[0].focus()
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
const handleCodeInput = (index: number, event: Event) => {
  const target = event.target as HTMLInputElement
  const value = target.value
  
  // Only allow numbers
  if (!/^\d*$/.test(value)) {
    codeDigits.value[index] = ''
    return
  }
  
  // Move to next input
  if (value && index < 5) {
    codeInputRefs.value[index + 1]?.focus()
  }
}

const handleKeyDown = (event: KeyboardEvent, index: number) => {
  // Move to previous input on backspace if current input is empty
  if (event.key === 'Backspace' && !codeDigits.value[index] && index > 0) {
    codeInputRefs.value[index - 1]?.focus()
  }
}

const handlePaste = (event: ClipboardEvent) => {
  event.preventDefault()
  
  const pastedData = event.clipboardData?.getData('text')
  if (!pastedData) return
  
  // Extract digits from pasted data
  const digits = pastedData.replace(/\D/g, '').split('').slice(0, 6)
  
  // Fill in available digits
  digits.forEach((digit, index) => {
    if (index < 6) {
      codeDigits.value[index] = digit
    }
  })
  
  // Focus the next empty input or the last one if all filled
  const nextEmptyIndex = codeDigits.value.findIndex(d => !d)
  if (nextEmptyIndex >= 0) {
    codeInputRefs.value[nextEmptyIndex]?.focus()
  } else {
    codeInputRefs.value[5]?.focus()
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
    
    // TODO: Replace with actual Cognito confirmForgotPassword API call
    // For now, we'll simulate the API call with a timeout
    await new Promise(resolve => setTimeout(resolve, 1500))
    
    // Show success message
    success.value = 'Password successfully reset. Redirecting to login...'
    
    // Show success toast
    toast.success('Password successfully reset!')
    
    // Redirect to login page after a short delay
    setTimeout(() => {
      router.push({
        path: '/login',
        query: { verified: 'password_reset' }
      })
    }, 2000)
  } catch (err: any) {
    error.value = err.message || 'Failed to reset password. Please try again.'
  } finally {
    loading.value = false
  }
}
</script>
