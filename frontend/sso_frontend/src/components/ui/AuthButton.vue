<template>
  <button
    :type="type"
    :disabled="disabled || loading"
    class="auth-button group relative overflow-hidden rounded-lg bg-zinc-900 border border-zinc-800 px-6 py-3 font-medium text-white shadow-md transition-all duration-200 hover:bg-zinc-800 hover:shadow-lg disabled:opacity-70"
  >
    <span class="flex items-center justify-center gap-2 relative z-10">
      <span v-if="loading" class="inline-block w-4 h-4 mr-2">
        <svg class="animate-spin" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
          <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
          <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
        </svg>
      </span>
      <slot></slot>
    </span>
  </button>
</template>

<script setup lang="ts">
defineProps({
  type: {
    type: String as () => 'button' | 'submit' | 'reset',
    default: 'button'
  },
  disabled: {
    type: Boolean,
    default: false
  },
  loading: {
    type: Boolean,
    default: false
  }
});
</script>

<style scoped>
.auth-button {
  will-change: transform;
  position: relative;
  overflow: hidden;
}

.auth-button:after {
  content: "";
  position: absolute;
  inset: 0;
  background: linear-gradient(to bottom, rgba(255, 255, 255, 0.03), transparent);
  opacity: 0;
  transition: opacity 0.2s ease;
}

.auth-button:hover:after {
  opacity: 1;
}

.auth-button:active {
  transform: translateY(1px);
}
</style>
