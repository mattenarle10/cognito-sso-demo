<template>
  <div 
    ref="cardContainer"
    class="auth-card-container"
    :class="{ 'auth-card-wide': wide }"
    :style="cardTransformStyle"
    @mousemove="handleMouseMove"
    @mouseleave="handleMouseLeave"
  >
    <!-- Card glow effects -->
    <div class="card-glow-effect"></div>
    <div class="card-inner-glow"></div>
    
    <!-- Main card content -->
    <div class="auth-card">
      <slot></slot>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue';
import { useMouseInElement } from '@vueuse/core';

// Props
defineProps({
  wide: {
    type: Boolean,
    default: false
  }
});

// Card container ref
const cardContainer = ref<HTMLElement | null>(null);

// Mouse tracking for tilt effect - simple implementation for performance
const { elementX, elementY, isOutside, elementHeight, elementWidth } = useMouseInElement(cardContainer, {
  handleOutside: true
});

// Add debouncing for performance
let lastMoveTime = 0;
const moveThreshold = 16; // ms (approximately 60fps)

// Calculate tilt effect based on mouse position - reduced intensity
const tiltX = computed(() => {
  if (isOutside.value) return 0;
  const center = elementWidth.value / 2;
  return ((elementX.value - center) / center) * 3; // -3 to 3 degrees (reduced from 5)
});

const tiltY = computed(() => {
  if (isOutside.value) return 0;
  const center = elementHeight.value / 2;
  return ((elementY.value - center) / center) * -3; // -3 to 3 degrees (reduced from 5)
});

// Generate CSS transform style with will-change optimization
const cardTransformStyle = computed(() => {
  return {
    transform: `perspective(1000px) rotateX(${tiltY.value}deg) rotateY(${tiltX.value}deg)`,
    transition: isOutside.value ? 'all 0.5s ease' : 'transform 0.05s linear',
    willChange: isOutside.value ? 'auto' : 'transform' // Only use will-change when actively moving
  };
});

// Event handlers with debouncing for better performance
const handleMouseMove = (e: MouseEvent) => {
  const now = performance.now();
  if (now - lastMoveTime < moveThreshold) return;
  lastMoveTime = now;
  // The actual tracking is handled by useMouseInElement
};

const handleMouseLeave = () => {
  // Reset will happen automatically via isOutside
  lastMoveTime = 0;
};
</script>

<style scoped>
.auth-card-container {
  position: relative;
  width: 100%;
  max-width: 450px;
  padding: 2px;
  border-radius: 1.5rem;
  background: linear-gradient(145deg, rgba(30, 30, 30, 0.5), rgba(15, 15, 15, 0.8));
  box-shadow: 
    0 10px 30px rgba(0, 0, 0, 0.6),
    0 0 0 1px rgba(50, 50, 50, 0.3) inset;
  backdrop-filter: blur(10px);
  transform-style: preserve-3d;
  will-change: transform;
  z-index: 10;
}

.auth-card-wide {
  max-width: 580px;
}

.auth-card {
  position: relative;
  background: rgba(15, 15, 15, 0.85);
  border-radius: 1.4rem;
  padding: 2rem;
  overflow: hidden;
  z-index: 2;
}

.card-glow-effect {
  position: absolute;
  inset: -2px;
  background: linear-gradient(145deg, rgba(40, 40, 40, 0.5), rgba(10, 10, 10, 0.2));
  border-radius: 1.5rem;
  opacity: 0.7;
  z-index: 1;
  pointer-events: none;
}

.card-inner-glow {
  position: absolute;
  inset: 0;
  border-radius: 1.5rem;
  background: radial-gradient(circle at 50% 30%, rgba(30, 30, 40, 0.4), transparent 70%);
  z-index: 1;
  pointer-events: none;
}

@media (max-width: 640px) {
  .auth-card {
    padding: 1.5rem;
  }
}
</style>
