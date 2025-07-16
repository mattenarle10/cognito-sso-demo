<template>
  <button
    :type="type"
    :disabled="disabled || loading"
    :class="[
      'btn-primary',
      { 'opacity-50 cursor-not-allowed': disabled || loading }
    ]"
    @click="$emit('click')"
  >
    <span v-if="loading" style="margin-right: 0.5rem;">⏳</span>
    <slot />
  </button>
</template>

<script setup lang="ts">
interface Props {
  type?: 'button' | 'submit' | 'reset'
  variant?: 'primary' | 'secondary'
  disabled?: boolean
  loading?: boolean
}

withDefaults(defineProps<Props>(), {
  type: 'button',
  variant: 'primary',
  disabled: false,
  loading: false
})

defineEmits<{
  click: []
}>()
</script> 