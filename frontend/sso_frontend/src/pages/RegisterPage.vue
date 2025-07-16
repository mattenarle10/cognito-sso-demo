<template>
  <div class="register-container">
    <div class="register-card">
      <!-- Header -->
      <div class="header">
        <h1>Create Account</h1>
        <p v-if="appName">to continue to {{ appName }}</p>
      </div>

      <!-- Registration Form -->
      <form v-if="step === 'register'" @submit.prevent="handleRegister" class="register-form">
        <BaseInput
          id="email"
          type="email"
          label="Email"
          placeholder="Enter your email"
          v-model="formData.email"
          :required="true"
          :error="errors.email"
        />

        <BaseInput
          id="phone"
          type="tel"
          label="Phone Number"
          placeholder="Enter your phone number"
          v-model="formData.phone"
          :required="true"
          :error="errors.phone"
        />

        <BaseInput
          id="name"
          type="text"
          label="Full Name"
          placeholder="Enter your full name"
          v-model="formData.name"
          :required="true"
          :error="errors.name"
        />

        <div class="form-group">
          <label for="gender" class="form-label">Gender</label>
          <select 
            id="gender" 
            v-model="formData.gender" 
            class="input-field"
            required
          >
            <option value="">Select gender</option>
            <option value="male">Male</option>
            <option value="female">Female</option>
            <option value="other">Other</option>
            <option value="prefer-not-to-say">Prefer not to say</option>
          </select>
          <p v-if="errors.gender" class="error-text">{{ errors.gender }}</p>
        </div>

        <BaseInput
          id="password"
          type="password"
          label="Password"
          placeholder="Enter your password"
          v-model="formData.password"
          :required="true"
          :error="errors.password"
        />

        <div class="checkbox-group">
          <label class="checkbox-label">
            <input 
              type="checkbox" 
              v-model="formData.accepts_marketing"
              class="checkbox"
            />
            <span>I agree to receive marketing communications</span>
          </label>
        </div>

        <BaseButton
          type="submit"
          :loading="loading"
          :disabled="!isFormValid"
          style="width: 100%; margin-top: 1rem;"
        >
          Create Account
        </BaseButton>
      </form>

      <!-- OTP Verification Form -->
      <div v-if="step === 'otp'" class="otp-form">
        <div class="otp-header">
          <h2>Verify Your Email</h2>
          <p>We've sent a verification code to {{ formData.email }}</p>
        </div>

        <form @submit.prevent="handleOtpVerification">
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
            :disabled="loading"
            class="resend-link"
          >
            Resend code
          </button>
        </div>
      </div>

      <!-- Login Link -->
      <div class="footer">
        <p>
          Already have an account?
          <router-link :to="loginLink" class="link">Sign in</router-link>
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
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import BaseInput from '../components/ui/BaseInput.vue'
import BaseButton from '../components/ui/BaseButton.vue'
import type { RegisterData } from '../types/auth'
import { cognitoService } from '../services/cognitoService'

// Form data
const formData = ref<RegisterData>({
  email: '',
  phone: '',
  name: '',
  gender: '',
  password: '',
  accepts_marketing: false
})

// State
const loading = ref(false)
const error = ref('')
const errors = ref<Record<string, string>>({})
const step = ref<'register' | 'otp'>('register')
const otpCode = ref('')

// Route handling for URL parameters
const route = useRoute()
const router = useRouter()
const appName = ref('')
const channelId = ref('')

// URL parameters from client app redirect
onMounted(() => {
  appName.value = route.query.application_name as string || ''
  channelId.value = route.query.channel_id as string || ''
  
  // todo: validate app/channel with backend
  console.log('App:', appName.value, 'Channel:', channelId.value)
})

// Computed
const isFormValid = computed(() => {
  return formData.value.email && 
         formData.value.phone && 
         formData.value.name && 
         formData.value.gender && 
         formData.value.password
})

const loginLink = computed(() => {
  const query = route.query
  return { name: 'login', query }
})

// Methods
const handleRegister = async () => {
  loading.value = true
  error.value = ''
  errors.value = {}

  try {
    // cognito registration
    await cognitoService.signUp({
      email: formData.value.email,
      password: formData.value.password,
      phone: formData.value.phone,
      name: formData.value.name,
      gender: formData.value.gender,
      acceptsMarketing: formData.value.accepts_marketing || false
    })
    
    // redirect to separate otp page
    router.push({
      name: 'email-otp',
      query: {
        email: formData.value.email,
        application_name: appName.value,
        channel_id: channelId.value
      }
    })
    
  } catch (err: any) {
    error.value = err.message || 'Registration failed'
  } finally {
    loading.value = false
  }
}

const handleOtpVerification = async () => {
  loading.value = true
  error.value = ''
  errors.value = {}

  try {
    // todo: implement cognito otp verification
    console.log('OTP verification:', otpCode.value)
    
    // placeholder - will implement cognito confirmation here
    await new Promise(resolve => setTimeout(resolve, 1000))
    
    // after successful verification, proceed with login flow
    
  } catch (err: any) {
    error.value = err.message || 'OTP verification failed'
  } finally {
    loading.value = false
  }
}

const resendOtp = async () => {
  loading.value = true
  error.value = ''

  try {
    // todo: implement resend otp
    console.log('Resending OTP')
    await new Promise(resolve => setTimeout(resolve, 1000))
    
  } catch (err: any) {
    error.value = err.message || 'Failed to resend code'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.register-container {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 1rem;
}

.register-card {
  background: white;
  padding: 2rem;
  border-radius: 0.5rem;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  width: 100%;
  max-width: 400px;
}

.header {
  text-align: center;
  margin-bottom: 2rem;
}

.header h1 {
  font-size: 1.5rem;
  font-weight: bold;
  margin-bottom: 0.5rem;
}

.header p {
  color: #6b7280;
  font-size: 0.875rem;
}

.register-form {
  margin-bottom: 1.5rem;
}

.form-group {
  margin-bottom: 1rem;
}

.form-label {
  display: block;
  font-size: 0.875rem;
  font-weight: 500;
  color: #374151;
  margin-bottom: 0.25rem;
}

.error-text {
  margin-top: 0.25rem;
  font-size: 0.875rem;
  color: #dc2626;
}

.checkbox-group {
  margin: 1rem 0;
}

.checkbox-label {
  display: flex;
  align-items: center;
  font-size: 0.875rem;
  color: #374151;
}

.checkbox {
  margin-right: 0.5rem;
}

.otp-form {
  margin-bottom: 1.5rem;
}

.otp-header {
  text-align: center;
  margin-bottom: 1.5rem;
}

.otp-header h2 {
  font-size: 1.25rem;
  font-weight: bold;
  margin-bottom: 0.5rem;
}

.otp-header p {
  color: #6b7280;
  font-size: 0.875rem;
}

.otp-footer {
  text-align: center;
  margin-top: 1rem;
}

.resend-link {
  background: none;
  border: none;
  color: #2563eb;
  font-size: 0.875rem;
  cursor: pointer;
  text-decoration: underline;
}

.resend-link:hover {
  color: #1d4ed8;
}

.resend-link:disabled {
  color: #9ca3af;
  cursor: not-allowed;
}

.footer {
  text-align: center;
  font-size: 0.875rem;
}

.link {
  color: #2563eb;
  text-decoration: none;
}

.link:hover {
  text-decoration: underline;
}

.error-message {
  margin-top: 1rem;
  padding: 0.75rem;
  background: #fef2f2;
  color: #dc2626;
  border-radius: 0.375rem;
  font-size: 0.875rem;
}
</style> 