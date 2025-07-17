<template>
  <AuthBackground>
    <AuthCard :wide="true">
      <!-- Header with enhanced styling -->
      <div class="mb-4 relative text-center">
        <div class="absolute -top-10 -right-10 w-40 h-40 bg-gradient-to-br from-zinc-800/30 to-zinc-900/30 rounded-full blur-3xl"></div>
        <h1 class="text-3xl lg:text-4xl font-bold tracking-tight mb-1 relative">
          <span class="bg-gradient-to-r from-gray-200 via-gray-100 to-gray-300 bg-clip-text text-transparent relative inline-block">Join The Grind.</span>
        </h1>
        <p class="text-zinc-500 text-sm font-light tracking-wide" v-if="appName">Create your account to continue brewing</p>
        <p class="text-zinc-500 text-sm font-light tracking-wide" v-else>Create your brewed account to get started</p>
      </div>

      <!-- Registration Form with enhanced styling -->
      <form @submit.prevent="handleRegister" class="space-y-3">
        <div class="grid grid-cols-1 md:grid-cols-2 gap-x-4 gap-y-2.5">
          <!-- First Name Input -->
          <div>
            <AuthInput
              id="firstName"
              type="text"
              label="First Name"
              placeholder="First name"
              v-model="formData.firstName"
              :required="true"
              :error="errors.firstName"
            >
              <template #icon>
                <UserIcon :size="14" class="text-zinc-500" />
              </template>
            </AuthInput>
          </div>

          <!-- Last Name Input -->
          <div>
            <AuthInput
              id="lastName"
              type="text"
              label="Last Name"
              placeholder="Last name"
              v-model="formData.lastName"
              :required="true"
              :error="errors.lastName"
            >
              <template #icon>
                <UserIcon :size="14" class="text-zinc-500" />
              </template>
            </AuthInput>
          </div>

          <!-- Phone Input with Country Code -->
          <div class="col-span-2">
            <label for="phone" class="text-zinc-300 font-medium tracking-wide text-xs block flex items-center gap-2 mb-1.5">
              <PhoneIcon :size="14" class="text-zinc-500" />
              Mobile Number
            </label>
            <div class="flex">
              <div class="flex-shrink-0 bg-zinc-900/80 border border-zinc-700/60 border-r-0 rounded-l-lg h-11 flex items-center px-3 text-zinc-300 text-sm font-medium">
                +63
              </div>
              <div class="flex-grow relative">
                <input
                  id="phone"
                  type="tel"
                  placeholder="9XX XXX XXXX"
                  v-model="phoneWithoutCode"
                  required
                  class="bg-zinc-900/60 border border-zinc-700/60 text-white placeholder:text-zinc-500 focus:border-zinc-400 focus:ring-1 focus:ring-zinc-400 h-10 rounded-lg font-light tracking-wide text-sm transition-all duration-200 pl-3 relative w-full"
                />
                <div class="absolute inset-0 bg-gradient-to-r from-zinc-800/5 to-transparent rounded-r-lg pointer-events-none" />
              </div>
            </div>
            <p v-if="errors.phone" class="text-red-400 text-xs mt-0.5">{{ errors.phone }}</p>
          </div>

          <!-- Email Input -->
          <div class="col-span-2">
            <AuthInput
              id="email"
              type="email"
              label="Email Address"
              placeholder="Email Address"
              v-model="formData.email"
              :required="true"
              :error="errors.email"
            >
              <template #icon>
                <MailIcon :size="14" class="text-zinc-500" />
              </template>
            </AuthInput>
          </div>

          <!-- Gender Select -->
          <div class="col-span-2 flex items-center gap-4">
            <label class="text-zinc-300 font-medium tracking-wide text-xs">
              Gender
            </label>
            <div class="flex gap-4">
              <label class="flex items-center gap-1.5 cursor-pointer group">
                <div class="relative flex items-center">
                  <input
                    type="radio"
                    name="gender"
                    value="male"
                    v-model="formData.gender"
                    required
                    class="peer sr-only"
                  />
                  <div class="w-4 h-4 border border-zinc-700 rounded-full bg-zinc-900/60 peer-checked:bg-zinc-700 peer-checked:border-zinc-600 transition-all duration-200"></div>
                  <div class="absolute w-2 h-2 bg-white rounded-full left-1/2 top-1/2 -translate-x-1/2 -translate-y-1/2 opacity-0 peer-checked:opacity-100 transition-opacity duration-200"></div>
                </div>
                <span class="text-zinc-400 text-xs group-hover:text-zinc-300 transition-colors duration-200">Male</span>
              </label>
              
              <label class="flex items-center gap-1.5 cursor-pointer group">
                <div class="relative flex items-center">
                  <input
                    type="radio"
                    name="gender"
                    value="female"
                    v-model="formData.gender"
                    class="peer sr-only"
                  />
                  <div class="w-4 h-4 border border-zinc-700 rounded-full bg-zinc-900/60 peer-checked:bg-zinc-700 peer-checked:border-zinc-600 transition-all duration-200"></div>
                  <div class="absolute w-2 h-2 bg-white rounded-full left-1/2 top-1/2 -translate-x-1/2 -translate-y-1/2 opacity-0 peer-checked:opacity-100 transition-opacity duration-200"></div>
                </div>
                <span class="text-zinc-400 text-xs group-hover:text-zinc-300 transition-colors duration-200">Female</span>
              </label>
            </div>
            <p v-if="errors.gender" class="text-red-400 text-xs mt-0.5">{{ errors.gender }}</p>
          </div>

          <!-- Password Input with Validation -->
          <div class="col-span-2">
            <label for="password" class="text-zinc-300 font-medium tracking-wide text-xs block flex items-center gap-2 mb-1.5">
              <LockIcon :size="14" class="text-zinc-500" />
              Password
            </label>
            <div class="relative">
<input
                id="password"
                :type="showPassword ? 'text' : 'password'"
                placeholder="Password"
                v-model="formData.password"
                required
                class="bg-zinc-900/60 border border-zinc-700/60 text-white placeholder:text-zinc-500 focus:border-zinc-400 focus:ring-1 focus:ring-zinc-400 h-10 rounded-lg font-light tracking-wide text-sm transition-all duration-200 pl-3 pr-10 relative w-full"
                @input="validatePassword"
              />
              <button 
                type="button" 
                class="absolute inset-y-0 right-0 flex items-center pr-3 cursor-pointer"
                @click="showPassword = !showPassword"
                tabindex="-1"
              >
                <EyeIcon v-if="!showPassword" :size="16" class="text-zinc-500 hover:text-zinc-300 transition-colors" />
                <EyeOffIcon v-else :size="16" class="text-zinc-500 hover:text-zinc-300 transition-colors" />
              </button>
              <div class="absolute inset-0 bg-gradient-to-r from-zinc-800/5 to-transparent rounded-lg pointer-events-none" />
            </div>
            <p v-if="errors.password" class="text-red-400 text-xs mt-0.5">{{ errors.password }}</p>
            
            <!-- Password Requirements -->
            <div class="mt-2 grid grid-cols-1 md:grid-cols-2 gap-x-4 gap-y-1.5">
              <div class="flex items-center gap-1.5">
                <div :class="[passwordValidation.minLength ? 'bg-green-500' : 'bg-zinc-700', 'w-4 h-4 rounded-full flex items-center justify-center transition-colors duration-200']">
                  <CheckIcon v-if="passwordValidation.minLength" :size="10" class="text-black" />
                </div>
                <span class="text-xs text-zinc-400">At least 8 characters</span>
              </div>
              <div class="flex items-center gap-1.5">
                <div :class="[passwordValidation.hasAlphanumeric ? 'bg-green-500' : 'bg-zinc-700', 'w-4 h-4 rounded-full flex items-center justify-center transition-colors duration-200']">
                  <CheckIcon v-if="passwordValidation.hasAlphanumeric" :size="10" class="text-black" />
                </div>
                <span class="text-xs text-zinc-400">Letters and numbers</span>
              </div>
              <div class="flex items-center gap-1.5">
                <div :class="[passwordValidation.hasCapital ? 'bg-green-500' : 'bg-zinc-700', 'w-4 h-4 rounded-full flex items-center justify-center transition-colors duration-200']">
                  <CheckIcon v-if="passwordValidation.hasCapital" :size="10" class="text-black" />
                </div>
                <span class="text-xs text-zinc-400">1 capital letter</span>
              </div>
              <div class="flex items-center gap-1.5">
                <div :class="[passwordValidation.hasSpecial ? 'bg-green-500' : 'bg-zinc-700', 'w-4 h-4 rounded-full flex items-center justify-center transition-colors duration-200']">
                  <CheckIcon v-if="passwordValidation.hasSpecial" :size="10" class="text-black" />
                </div>
                <span class="text-xs text-zinc-400">1 special character</span>
              </div>
            </div>
          </div>

          <!-- Marketing Checkbox -->
          <div class="col-span-2 mt-2">
            <label class="flex items-center gap-2 cursor-pointer group">
              <div class="relative flex items-center">
                <input
                  type="checkbox"
                  v-model="formData.accepts_marketing"
                  class="peer sr-only"
                />
                <div class="w-5 h-5 border border-zinc-700 rounded bg-zinc-900/60 peer-checked:bg-zinc-700 peer-checked:border-zinc-600 transition-all duration-200"></div>
                <CheckIcon :size="12" class="absolute text-white left-1/2 top-1/2 -translate-x-1/2 -translate-y-1/2 opacity-0 peer-checked:opacity-100 transition-opacity duration-200" />
              </div>
              <span class="text-zinc-400 text-sm group-hover:text-zinc-300 transition-colors duration-200">I agree to receive marketing communications</span>
            </label>
          </div>
        </div>

        <!-- Submit Button -->
        <div class="flex justify-center mt-6">
          <AuthButton
            type="submit"
            :loading="loading"
            :disabled="!isFormValid"
            class="w-full sm:w-1/2"
          >
            Create Account
            <ArrowRightIcon :size="16" class="ml-1 transition-transform duration-200" />
          </AuthButton>
        </div>
      </form>

      <!-- Error Display -->
      <div v-if="error" class="mt-4 p-3 bg-red-900/20 border border-red-800/50 rounded-lg text-red-400 text-sm">
        {{ error }}
      </div>

      <!-- Footer with enhanced styling -->
      <div class="mt-6 pt-5 border-t border-zinc-800/50 relative">
        <!-- Border texture -->
        <div class="absolute top-0 left-0 right-0 h-[1px] bg-gradient-to-r from-transparent via-zinc-700/30 to-transparent" />
        <p class="text-center text-zinc-400 text-sm">
          Already have an account?
          <router-link
            :to="loginLink"
            class="text-zinc-200 hover:text-white font-medium underline underline-offset-2 decoration-zinc-600 hover:decoration-zinc-400 transition-all duration-200 inline-flex items-center gap-1"
          >
            Login
            <ArrowRightIcon :size="10" class="opacity-60" />
          </router-link>
        </p>
      </div>
    </AuthCard>
  </AuthBackground>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import AuthBackground from '../components/ui/AuthBackground.vue'
import AuthCard from '../components/ui/AuthCard.vue'
import AuthInput from '../components/ui/AuthInput.vue'
import AuthButton from '../components/ui/AuthButton.vue'
import { MailIcon, LockIcon, UserIcon, PhoneIcon, UsersIcon, ArrowRightIcon, ChevronDownIcon, CheckIcon, EyeIcon, EyeOffIcon } from 'lucide-vue-next'
import type { RegisterData } from '../types/auth'
import { cognitoService } from '../services/cognitoService'

// Form data
const formData = ref<RegisterData & { firstName: string; lastName: string }>({
  email: '',
  phone: '',
  name: '',
  firstName: '',
  lastName: '',
  gender: '',
  password: '',
  accepts_marketing: false
})

// Phone number handling with country code
const phoneWithoutCode = ref('')

// Password handling
const showPassword = ref(false)

// Password validation
const passwordValidation = ref({
  minLength: false,
  hasAlphanumeric: false,
  hasCapital: false,
  hasSpecial: false
})

// State
const loading = ref(false)
const error = ref('')
const errors = ref<Record<string, string>>({})

// Update full phone number when phoneWithoutCode changes
watch(phoneWithoutCode, (newValue) => {
  formData.value.phone = `+63${newValue.replace(/\D/g, '')}`
})

// Update full name when firstName or lastName changes
watch([() => formData.value.firstName, () => formData.value.lastName], () => {
  formData.value.name = `${formData.value.firstName} ${formData.value.lastName}`.trim()
})

// Validate password against requirements
const validatePassword = () => {
  const password = formData.value.password
  
  // Check minimum length (8 characters)
  passwordValidation.value.minLength = password.length >= 8
  
  // Check for alphanumeric (contains both letters and numbers)
  passwordValidation.value.hasAlphanumeric = /[a-zA-Z]/.test(password) && /[0-9]/.test(password)
  
  // Check for at least one capital letter
  passwordValidation.value.hasCapital = /[A-Z]/.test(password)
  
  // Check for at least one special character
  passwordValidation.value.hasSpecial = /[^a-zA-Z0-9]/.test(password)
}

// Route handling for URL parameters
const route = useRoute()
const router = useRouter()
const appName = ref('')
const channelId = ref('')

// URL parameters from client app redirect
onMounted(() => {
  appName.value = route.query.application_name as string || ''
  channelId.value = route.query.channel_id as string || ''
  
  // Initialize password validation
  validatePassword()
  
  // todo: validate app/channel with backend
  console.log('App:', appName.value, 'Channel:', channelId.value)
})

// Computed
const isFormValid = computed(() => {
  const allFieldsFilled = formData.value.email && 
                         formData.value.phone && 
                         formData.value.name && 
                         formData.value.gender && 
                         formData.value.password
  
  const passwordValid = passwordValidation.value.minLength && 
                       passwordValidation.value.hasAlphanumeric && 
                       passwordValidation.value.hasCapital && 
                       passwordValidation.value.hasSpecial
  
  return allFieldsFilled && passwordValid
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
      acceptsMarketing: formData.value.accepts_marketing || false,
      applicationName: appName.value,
      channelId: channelId.value
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
</script>
