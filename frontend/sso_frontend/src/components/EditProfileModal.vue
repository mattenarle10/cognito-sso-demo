<template>
  <!-- Modal Backdrop -->
  <div class="fixed inset-0 bg-black/70 backdrop-blur-sm flex items-center justify-center z-50" @click.self="handleCancel">
    <AuthCard>
      <!-- Header -->
      <div class="mb-6 text-center">
        <h2 class="text-2xl font-bold tracking-tight mb-2">
          <span class="bg-gradient-to-r from-gray-200 via-gray-100 to-gray-300 bg-clip-text text-transparent">
            edit profile
          </span>
        </h2>
        <p class="text-zinc-500 text-sm">
          update your display name
        </p>
      </div>

      <!-- Form -->
      <form @submit.prevent="handleSave" class="space-y-5">
        <!-- First Name -->
        <AuthInput
          id="firstName"
          type="text"
          label="First Name"
          placeholder="enter your first name"
          v-model="formData.firstName"
          :required="true"
          :error="errors.firstName"
        >
          <template #icon>
            <svg class="w-4 h-4 text-zinc-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"></path>
            </svg>
          </template>
        </AuthInput>

        <!-- Last Name -->
        <AuthInput
          id="lastName"
          type="text"
          label="Last Name"
          placeholder="enter your last name"
          v-model="formData.lastName"
          :required="true"
          :error="errors.lastName"
        >
          <template #icon>
            <svg class="w-4 h-4 text-zinc-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"></path>
            </svg>
          </template>
        </AuthInput>

        <!-- Error message -->
        <div v-if="error" class="bg-red-500/10 border border-red-500/20 text-red-400 px-4 py-3 rounded-lg text-sm">
          {{ error }}
        </div>

        <!-- Buttons -->
        <div class="flex gap-3 pt-2">
          <AuthButton
            type="button"
            @click="handleCancel"
            :disabled="saving"
            class="flex-1 !bg-transparent !border-zinc-700 !text-zinc-400 hover:!text-zinc-300 hover:!bg-zinc-800/50"
          >
            cancel
          </AuthButton>
          
          <AuthButton
            type="submit"
            :loading="saving"
            :disabled="!isFormValid || saving"
            class="flex-1"
          >
            <span v-if="saving">saving...</span>
            <span v-else>save changes</span>
          </AuthButton>
        </div>
      </form>
    </AuthCard>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useApi } from '../composables/useApi'
import { useToast } from 'vue-toastification'
import AuthCard from './ui/AuthCard.vue'
import AuthButton from './ui/AuthButton.vue'
import AuthInput from './ui/AuthInput.vue'

// Props
interface Props {
  currentName?: string
  tokens: any
}

const props = defineProps<Props>()

// Emits
const emit = defineEmits<{
  save: [newName: string]
  cancel: []
}>()

// Composables
const api = useApi()
const toast = useToast()

// Form state
const formData = ref({
  firstName: '',
  lastName: ''
})

const saving = ref(false)
const error = ref('')
const errors = ref<Record<string, string>>({})

// Computed
const isFormValid = computed(() => {
  return formData.value.firstName.trim().length > 0 && 
         formData.value.lastName.trim().length > 0
})

const fullName = computed(() => {
  return `${formData.value.firstName.trim()} ${formData.value.lastName.trim()}`.trim()
})

// Methods
const validateForm = () => {
  errors.value = {}
  
  if (!formData.value.firstName.trim()) {
    errors.value.firstName = 'first name is required'
  } else if (formData.value.firstName.trim().length > 50) {
    errors.value.firstName = 'first name cannot exceed 50 characters'
  } else if (!/^[a-zA-Z\s\-'\.]+$/.test(formData.value.firstName.trim())) {
    errors.value.firstName = 'first name contains invalid characters'
  }
  
  if (!formData.value.lastName.trim()) {
    errors.value.lastName = 'last name is required'
  } else if (formData.value.lastName.trim().length > 50) {
    errors.value.lastName = 'last name cannot exceed 50 characters'
  } else if (!/^[a-zA-Z\s\-'\.]+$/.test(formData.value.lastName.trim())) {
    errors.value.lastName = 'last name contains invalid characters'
  }
  
  if (fullName.value.length > 100) {
    errors.value.firstName = 'combined name cannot exceed 100 characters'
  }
  
  return Object.keys(errors.value).length === 0
}

const handleSave = async () => {
  error.value = ''
  
  if (!validateForm()) {
    return
  }
  
  saving.value = true
  
  try {
    const updates = {
      name: fullName.value
    }
    
    const success = await api.updateUserProfile(updates, props.tokens)
    
    if (success) {
      toast.success('profile updated successfully!')
      emit('save', fullName.value)
    } else {
      error.value = api.error.value || 'failed to update profile'
    }
    
  } catch (err: any) {
    error.value = err.message || 'failed to update profile'
  } finally {
    saving.value = false
  }
}

const handleCancel = () => {
  emit('cancel')
}

// Initialize form with current name
onMounted(() => {
  if (props.currentName) {
    const nameParts = props.currentName.split(' ')
    formData.value.firstName = nameParts[0] || ''
    formData.value.lastName = nameParts.slice(1).join(' ') || ''
  }
})
</script> 