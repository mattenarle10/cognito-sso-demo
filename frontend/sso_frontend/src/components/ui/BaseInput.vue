<template>
  <div class="mb-4">
    <label v-if="label" :for="id" class="block text-sm font-medium text-gray-700 mb-1">
      {{ label }}
    </label>
    <input
      :id="id"
      :type="type"
      :placeholder="placeholder"
      :value="modelValue"
      :required="required"
      class="input-field"
      @input="$emit('update:modelValue', ($event.target as HTMLInputElement).value)"
    />
    <p v-if="error" class="mt-1 text-sm text-red-600">{{ error }}</p>
  </div>
</template>

<script setup lang="ts">
interface Props {
  id: string
  type?: string
  label?: string
  placeholder?: string
  modelValue: string
  required?: boolean
  error?: string
}

withDefaults(defineProps<Props>(), {
  type: 'text',
  required: false
})

defineEmits<{
  'update:modelValue': [value: string]
}>()
</script> 