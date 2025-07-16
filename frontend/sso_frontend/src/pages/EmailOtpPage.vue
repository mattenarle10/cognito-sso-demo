<template>
  <div class="otp-container">
    <div class="otp-card">
      <!-- Header -->
      <div class="header">
        <h1>Verify Your Email</h1>
        <p v-if="appName">to continue to {{ appName }}</p>
        <p class="otp-info">We've sent a verification code to {{ email }}</p>
      </div>

      <!-- OTP Verification Form -->
      <form @submit.prevent="handleOtpVerification" class="otp-form">
        <BaseInput
          id="otp"
          type="text"
          label="Verification Code"
          placeholder="Enter 6-digit code"
          v-model="otpCode"
          :required="true"
          :error="errors.otp"
        />

        <BaseButton
          type="submit"
          :loading="loading"
          :disabled="!otpCode"
          style="width: 100%; margin-top: 1rem;"
        >
          Verify Email
        </BaseButton>
      </form>

      <div class="otp-footer">
        <button 
          type="button" 
          @click="resendOtp" 
          :disabled="loading || resendCooldown > 0"
          class="resend-link"
        >
          {{ resendCooldown > 0 ? `Resend in ${resendCooldown}s` : 'Resend code' }}
        </button>
      </div>

      <!-- Back to Registration -->
      <div class="footer">
        <p>
          Need to change your email?
          <router-link :to="registerLink" class="link">Back to registration</router-link>
        </p>
      </div>

      <!-- Error Display -->
      <div v-if="error" class="error-message">
        {{ error }}
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import BaseInput from '../components/ui/BaseInput.vue'
import BaseButton from '../components/ui/BaseButton.vue'
import { useApi } from '../composables/useApi'

const route = useRoute()
const router = useRouter()
const api = useApi()

// reactive state
const otpCode = ref('')
const loading = ref(false)
const error = ref('')
const errors = ref<Record<string, string>>({})
const resendCooldown = ref(0)

// get params from route
const email = computed(() => route.query.email as string)
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
    errors.value.otp = 'verification code is required'
    return
  }

  if (otpCode.value.length !== 6) {
    errors.value.otp = 'verification code must be 6 digits'
    return
  }

  loading.value = true

  try {
    // todo: implement cognito email verification
    console.log('verifying otp:', {
      email: email.value,
      code: otpCode.value
    })

    // placeholder - replace with actual cognito verification
    await new Promise(resolve => setTimeout(resolve, 1000))
    
    // after successful verification, redirect to login or back to app
    const loginQuery = {
      application_name: appName.value,
      channel_id: channelId.value
    }
    
    router.push({
      name: 'login',
      query: loginQuery
    })

  } catch (err: any) {
    error.value = err.message || 'verification failed. please try again.'
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
    // todo: implement cognito resend confirmation code
    console.log('resending otp to:', email.value)
    
    // placeholder - replace with actual cognito resend
    await new Promise(resolve => setTimeout(resolve, 1000))
    
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
    error.value = err.message || 'failed to resend code. please try again.'
  } finally {
    loading.value = false
  }
}

// lifecycle
onMounted(() => {
  // validate required params
  if (!email.value) {
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

<style scoped>
.otp-container {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: #f5f5f5;
  padding: 1rem;
}

.otp-card {
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  padding: 2rem;
  width: 100%;
  max-width: 400px;
}

.header {
  text-align: center;
  margin-bottom: 2rem;
}

.header h1 {
  font-size: 1.5rem;
  font-weight: 600;
  margin-bottom: 0.5rem;
  color: #1f2937;
}

.header p {
  color: #6b7280;
  margin-bottom: 0.5rem;
}

.otp-info {
  font-size: 0.9rem;
  color: #374151;
  background-color: #f3f4f6;
  padding: 0.75rem;
  border-radius: 6px;
  margin-top: 1rem;
}

.otp-form {
  margin-bottom: 1.5rem;
}

.otp-footer {
  text-align: center;
  margin-bottom: 1.5rem;
}

.resend-link {
  color: #3b82f6;
  text-decoration: underline;
  background: none;
  border: none;
  cursor: pointer;
  font-size: 0.9rem;
}

.resend-link:hover:not(:disabled) {
  color: #2563eb;
}

.resend-link:disabled {
  color: #9ca3af;
  cursor: not-allowed;
  text-decoration: none;
}

.footer {
  text-align: center;
  font-size: 0.9rem;
  color: #6b7280;
}

.link {
  color: #3b82f6;
  text-decoration: none;
}

.link:hover {
  text-decoration: underline;
}

.error-message {
  margin-top: 1rem;
  padding: 0.75rem;
  background-color: #fef2f2;
  border: 1px solid #fecaca;
  border-radius: 6px;
  color: #dc2626;
  font-size: 0.9rem;
}
</style> 