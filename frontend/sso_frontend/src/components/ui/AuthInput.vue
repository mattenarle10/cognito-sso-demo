<template>
  <div class="auth-input-wrapper mb-1">
    <label
      :for="id"
      class="text-zinc-300 font-medium tracking-wide text-xs block flex items-center gap-2 mb-1.5"
    >
      <slot name="icon"></slot>
      {{ label }}
    </label>
    <div class="relative">
      <input
        :id="id"
        :type="type"
        :placeholder="placeholder"
        :value="modelValue"
        @input="$emit('update:modelValue', ($event.target as HTMLInputElement).value)"
        :required="required"
        class="bg-zinc-900/60 border border-zinc-700/60 text-white placeholder:text-zinc-500 focus:border-zinc-400 focus:ring-1 focus:ring-zinc-400 h-11 rounded-lg font-light tracking-wide text-sm transition-all duration-200 pl-3 relative w-full"
      />
      <!-- Input field texture -->
      <div class="absolute inset-0 bg-gradient-to-r from-zinc-800/5 to-transparent rounded-lg pointer-events-none" />
    </div>
    <p v-if="error" class="text-red-400 text-xs mt-0.5">{{ error }}</p>
  </div>
</template>

<script setup lang="ts">
defineProps({
  id: {
    type: String,
    required: true
  },
  type: {
    type: String,
    default: 'text'
  },
  label: {
    type: String,
    required: true
  },
  placeholder: {
    type: String,
    default: ''
  },
  modelValue: {
    type: [String, Number],
    default: ''
  },
  required: {
    type: Boolean,
    default: false
  },
  error: {
    type: String,
    default: ''
  }
});

defineEmits(['update:modelValue']);
</script>

<style scoped>
.auth-input-wrapper {
  margin-bottom: 1rem;
}

input:focus {
  outline: none;
}
</style>
