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
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { MailIcon, LockIcon, ArrowRightIcon } from 'lucide-vue-next'
import type { LoginCredentials } from '../types/auth'
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

    // check if user is authorized for this application
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
    
    // authorization was already created by the consent screen
    // now create session with the authorized user
    const sessionResponse = await api.initSession(userTokens.value, appName.value)
    
    toast.success('Welcome to The Grind!')
    
    // redirect back to client app with session_id
    if (sessionResponse) {
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