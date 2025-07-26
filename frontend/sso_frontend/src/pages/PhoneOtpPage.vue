<template>
  <AuthBackground>
    <AuthCard>
      <!-- Header with enhanced styling -->
      <div class="mb-4 relative text-center">
        <div class="absolute -top-10 -right-10 w-40 h-40 bg-gradient-to-br from-zinc-800/30 to-zinc-900/30 rounded-full blur-3xl"></div>
        <h1 class="text-3xl font-bold tracking-tight mb-1 relative">
          <span class="bg-gradient-to-r from-gray-200 via-gray-100 to-gray-300 bg-clip-text text-transparent relative inline-block">Verify Your Phone</span>
        </h1>
        <p class="text-zinc-500 text-sm font-light tracking-wide" v-if="appName">to continue to {{ appName }}</p>
        <p class="text-zinc-400 text-sm mt-3 bg-zinc-800/50 py-2 px-3 rounded-lg inline-block">
          <span class="text-zinc-300">Code sent to:</span> {{ phone }}
        </p>
      </div>

      <!-- OTP Input Boxes -->
      <form @submit.prevent="handleOtpVerification" class="space-y-5">
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
                :id="`otp-${index}`"
                v-model="otpDigits[index]"
                @input="handleDigitInput(index)"
                @keydown="handleKeyDown($event, index)"
                @paste="handlePaste"
                class="w-11 h-14 bg-zinc-900/60 border border-zinc-700/60 text-white text-center text-xl font-medium rounded-lg focus:border-zinc-400 focus:ring-1 focus:ring-zinc-400 transition-all duration-200"
              />
              <div class="absolute inset-0 bg-gradient-to-r from-zinc-800/5 to-transparent rounded-lg pointer-events-none" />
            </div>
          </div>
          <p v-if="errors.otp" class="text-red-400 text-xs mt-2 text-center">{{ errors.otp }}</p>
        </div>

        <!-- Submit Button -->
        <AuthButton
          type="submit"
          :loading="loading"
          :disabled="!isOtpComplete"
          class="w-full"
        >
          <span class="flex items-center justify-center gap-2">
            Verify Phone
            <ArrowRightIcon :size="16" />
          </span>
        </AuthButton>

        <!-- Resend and Back Links -->
        <div class="flex flex-col items-center gap-2 pt-1">
          <button 
            type="button" 
            @click="resendOtp" 
            :disabled="loading || resendCooldown > 0"
            class="text-zinc-400 hover:text-zinc-300 text-sm transition-colors duration-200 flex items-center gap-1.5"
          >
            <RefreshCwIcon v-if="resendCooldown === 0" :size="14" />
            <span v-if="resendCooldown > 0">Resend in {{ resendCooldown }}s</span>
            <span v-else>Resend code</span>
          </button>
          
          <router-link 
            :to="registerLink" 
            class="text-zinc-500 hover:text-zinc-400 text-xs transition-colors duration-200"
          >
            Need to change your phone?
          </router-link>
        </div>

        <!-- Error Display -->
        <div v-if="error" class="bg-red-900/20 border border-red-800/50 text-red-400 text-xs py-2 px-3 rounded-lg mt-2">
          {{ error }}
        </div>
      </form>
    </AuthCard>
  </AuthBackground>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import AuthBackground from '../components/ui/AuthBackground.vue'
import AuthCard from '../components/ui/AuthCard.vue'
import AuthButton from '../components/ui/AuthButton.vue'
import { ArrowRightIcon, RefreshCwIcon } from 'lucide-vue-next'
import { useApi } from '../composables/useApi'
import { cognitoService } from '../services/cognitoService'
import { useToast } from 'vue-toastification'

const route = useRoute()
const router = useRouter()
const api = useApi()
const toast = useToast()

// reactive state
const otpDigits = ref<string[]>(Array(6).fill(''))
const loading = ref(false)
const error = ref('')
const errors = ref<Record<string, string>>({})
const resendCooldown = ref(0)

// computed
const otpCode = computed(() => otpDigits.value.join(''))

// Check if OTP is complete (all 6 digits filled)
const isOtpComplete = computed(() => otpDigits.value.every(digit => digit !== ''))

// Handle input for each digit box
const handleDigitInput = (index: number) => {
  // Clear any existing errors
  clearErrors()
  
  // Auto-focus next input box when a digit is entered
  if (otpDigits.value[index] && index < 5) {
    const nextInput = document.getElementById(`otp-${index + 1}`) as HTMLInputElement
    if (nextInput) nextInput.focus()
  }
}

// Handle keyboard navigation between OTP boxes
const handleKeyDown = (event: KeyboardEvent, index: number) => {
  // Handle backspace key
  if (event.key === 'Backspace') {
    if (!otpDigits.value[index] && index > 0) {
      const prevInput = document.getElementById(`otp-${index - 1}`) as HTMLInputElement
      if (prevInput) {
        prevInput.focus()
        // Optional: clear the previous input
        // otpDigits.value[index - 1] = ''
      }
    }
  }
  // Handle left arrow key
  else if (event.key === 'ArrowLeft' && index > 0) {
    const prevInput = document.getElementById(`otp-${index - 1}`) as HTMLInputElement
    if (prevInput) prevInput.focus()
  }
  // Handle right arrow key
  else if (event.key === 'ArrowRight' && index < 5) {
    const nextInput = document.getElementById(`otp-${index + 1}`) as HTMLInputElement
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
    if (i < 6) otpDigits.value[i] = digits[i]
  }
  
  // Focus the next empty box or the last box if all filled
  const emptyIndex = otpDigits.value.findIndex(digit => !digit)
  const focusIndex = emptyIndex !== -1 ? emptyIndex : 5
  const inputToFocus = document.getElementById(`otp-${focusIndex}`) as HTMLInputElement
  if (inputToFocus) inputToFocus.focus()
  
  clearErrors()
}

// get params from route
const email = computed(() => route.query.email as string)
const phone = computed(() => route.query.phone as string)
const appName = computed(() => route.query.application_name as string)
const channelId = computed(() => route.query.channel_id as string)

// computed links with preserved params
const registerLink = computed(() => ({
  name: 'register',
  query: {
    application_name: appName.value,
    channel_id: channelId.value
  }
}))

let resendTimer: number | null = null

// form validation
const clearErrors = () => {
  errors.value = {}
  error.value = ''
}

// handle otp verification
const handleOtpVerification = async () => {
  clearErrors()

  if (!otpCode.value) {
    errors.value.otp = 'Verification code is required'
    return
  }

  if (otpCode.value.length !== 6) {
    errors.value.otp = 'Verification code must be 6 digits'
    return
  }

  loading.value = true

  try {
    await cognitoService.confirmSignUpWithPhone({
      email: email.value,
      phone: phone.value,
      code: otpCode.value,
      applicationName: appName.value,
      channelId: channelId.value
    })

    // Show success toast
    toast.success('Phone number verified successfully!')

    // Only redirect to login if confirmation succeeded
    const loginQuery = {
      application_name: appName.value,
      channel_id: channelId.value,
      verified: 'true'
    }
    router.push({
      name: 'login',
      query: loginQuery
    })
  } catch (err: any) {
    if (err.message && err.message.toLowerCase().includes('already confirmed')) {
      error.value = 'Your phone is already confirmed. Please log in.'
    } else {
      error.value = err.message || 'Verification failed. Please try again.'
    }
  } finally {
    loading.value = false
  }
}

// handle resend otp
const resendOtp = async () => {
  if (resendCooldown.value > 0) return
  
  clearErrors()
  loading.value = true

  try {
    // cognito resend confirmation code for phone
    await cognitoService.resendPhoneConfirmationCode(phone.value, email.value)
    
    // Show success toast
    toast.info(`Verification code sent to ${phone.value}`)
    
    // start cooldown timer
    resendCooldown.value = 30
    resendTimer = window.setInterval(() => {
      resendCooldown.value--
      if (resendCooldown.value <= 0 && resendTimer) {
        clearInterval(resendTimer)
        resendTimer = null
      }
    }, 1000)

  } catch (err: any) {
    error.value = err.message || 'Failed to resend code. Please try again.'
  } finally {
    loading.value = false
  }
}

// lifecycle
onMounted(() => {
  // validate required params
  if (!phone.value || !email.value) {
    router.push({ name: 'register' })
    return
  }
})

onUnmounted(() => {
  if (resendTimer) {
    clearInterval(resendTimer)
  }
})
</script>
