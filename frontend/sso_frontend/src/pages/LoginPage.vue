<template>
  <div class="login-container">
    <div class="login-card">
      <!-- Header -->
      <div class="header">
        <h1>Sign In</h1>
        <p v-if="appName">to continue to {{ appName }}</p>
      </div>

      <!-- Login Form -->
      <form @submit.prevent="handleLogin" class="login-form">
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
          id="password"
          type="password"
          label="Password"
          placeholder="Enter your password"
          v-model="formData.password"
          :required="true"
          :error="errors.password"
        />

        <BaseButton
          type="submit"
          :loading="loading"
          :disabled="!isFormValid"
          style="width: 100%; margin-top: 1rem;"
        >
          Sign In
        </BaseButton>
      </form>

      <!-- Register Link -->
      <div class="footer">
        <p>
          Don't have an account?
          <router-link :to="registerLink" class="link">Sign up</router-link>
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
import type { LoginCredentials } from '../types/auth'
import { cognitoService } from '../services/cognitoService'
import { useApi } from '../composables/useApi'

// Form data
const formData = ref<LoginCredentials>({
  email: '',
  password: ''
})

// State
const loading = ref(false)
const error = ref('')
const errors = ref<Record<string, string>>({})

// Route handling for URL parameters
const route = useRoute()
const router = useRouter()
const api = useApi()
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
  return formData.value.email && formData.value.password
})

const registerLink = computed(() => {
  const query = route.query
  return { name: 'register', query }
})

// Methods
const handleLogin = async () => {
  loading.value = true
  error.value = ''
  errors.value = {}

  try {
    // cognito authentication with application context
    const tokens = await cognitoService.signIn({
      email: formData.value.email,
      password: formData.value.password,
      applicationName: appName.value,
      channelId: channelId.value
    })

         // create session with sso backend
     const sessionResponse = await api.initSession(tokens, appName.value)

     // redirect back to client app with session_id
     if (sessionResponse) {
       const redirectUrl = route.query.redirect_url as string || 'http://localhost:8080'
       window.location.href = `${redirectUrl}?session_id=${sessionResponse.session_id}`
     } else {
       throw new Error('failed to create session')
     }
    
  } catch (err: any) {
    error.value = err.message || 'login failed'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.login-container {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 1rem;
}

.login-card {
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

.login-form {
  margin-bottom: 1.5rem;
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