<template>
  <div class="auth-background">
    <!-- Background elements -->
    <div class="noise-texture"></div>
    <div class="grid-texture"></div>
    <div class="gradient-overlay"></div>
    
    <!-- Three.js canvas for particle background -->
    <canvas ref="threeCanvas" class="three-canvas"></canvas>
    
    <!-- Main container for content -->
    <div class="content-container">
      <slot></slot>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onBeforeUnmount } from 'vue';
import * as THREE from 'three';

// Three.js setup
const threeCanvas = ref<HTMLCanvasElement | null>(null);
let scene: THREE.Scene | null = null;
let camera: THREE.PerspectiveCamera | null = null;
let renderer: THREE.WebGLRenderer | null = null;
let particles: THREE.Points | null = null;
let animationFrameId: number | null = null;

// Initialize Three.js scene
const initThree = () => {
  if (!threeCanvas.value) return;
  
  // Scene setup
  scene = new THREE.Scene();
  
  // Camera setup
  const { clientWidth: width, clientHeight: height } = threeCanvas.value;
  camera = new THREE.PerspectiveCamera(75, width / height, 0.1, 1000);
  camera.position.z = 30;
  
  // Renderer setup - optimize for performance
  renderer = new THREE.WebGLRenderer({ 
    canvas: threeCanvas.value,
    alpha: true,
    antialias: false, // Disable antialiasing for better performance
    powerPreference: 'high-performance'
  });
  renderer.setSize(width, height);
  renderer.setPixelRatio(Math.min(window.devicePixelRatio, 1.5)); // Limit pixel ratio for performance
  
  // Create particles - reduce count for better performance
  const particlesGeometry = new THREE.BufferGeometry();
  const particlesCount = 500; // Reduced from 1000
  
  const posArray = new Float32Array(particlesCount * 3);
  for (let i = 0; i < particlesCount * 3; i++) {
    posArray[i] = (Math.random() - 0.5) * 40; // Slightly reduced spread
  }
  
  particlesGeometry.setAttribute('position', new THREE.BufferAttribute(posArray, 3));
  
  const particlesMaterial = new THREE.PointsMaterial({
    size: 0.12, // Slightly larger to compensate for fewer particles
    color: 0xffffff,
    transparent: true,
    opacity: 0.5,
    sizeAttenuation: true
  });
  
  particles = new THREE.Points(particlesGeometry, particlesMaterial);
  scene.add(particles);
  
  // Start animation
  animate();
  
  // Handle resize
  window.addEventListener('resize', handleResize);
};

// Animation loop with throttling for better performance
let lastFrameTime = 0;
const frameInterval = 1000 / 30; // Target 30fps instead of 60fps for better performance

const animate = (currentTime = 0) => {
  if (!scene || !camera || !renderer || !particles) return;
  
  animationFrameId = requestAnimationFrame(animate);
  
  // Throttle rendering to improve performance
  const deltaTime = currentTime - lastFrameTime;
  if (deltaTime < frameInterval) return;
  
  // Adjust for any skipped frames
  lastFrameTime = currentTime - (deltaTime % frameInterval);
  
  // Slower rotation for smoother appearance
  particles.rotation.x += 0.0003;
  particles.rotation.y += 0.0002;
  
  renderer.render(scene, camera);
};

// Handle window resize
const handleResize = () => {
  if (!camera || !renderer || !threeCanvas.value) return;
  
  const { clientWidth: width, clientHeight: height } = threeCanvas.value;
  
  camera.aspect = width / height;
  camera.updateProjectionMatrix();
  
  renderer.setSize(width, height);
  renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
};

// Lifecycle hooks
onMounted(() => {
  initThree();
});

onBeforeUnmount(() => {
  if (animationFrameId !== null) {
    cancelAnimationFrame(animationFrameId);
  }
  
  window.removeEventListener('resize', handleResize);
  
  // Clean up Three.js resources
  if (particles) {
    if (particles.geometry) particles.geometry.dispose();
    if (particles.material) {
      if (Array.isArray(particles.material)) {
        particles.material.forEach(m => m.dispose());
      } else {
        particles.material.dispose();
      }
    }
  }
  
  if (renderer) renderer.dispose();
  
  scene = null;
  camera = null;
  renderer = null;
  particles = null;
});
</script>

<style scoped>
.auth-background {
  position: relative;
  width: 100%;
  min-height: 100vh;
  background: linear-gradient(to bottom right, #0a0a0a, #111827);
  overflow: hidden;
}

.noise-texture {
  position: absolute;
  inset: 0;
  background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 200 200' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noiseFilter'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.5' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noiseFilter)'/%3E%3C/svg%3E");
  opacity: 0.2;
  pointer-events: none;
}

.grid-texture {
  position: absolute;
  inset: 0;
  background-image: linear-gradient(to right, rgba(255, 255, 255, 0.07) 1px, transparent 1px),
                    linear-gradient(to bottom, rgba(255, 255, 255, 0.07) 1px, transparent 1px);
  background-size: 20px 20px;
  pointer-events: none;
}

.gradient-overlay {
  position: absolute;
  inset: 0;
  background: radial-gradient(circle at center, transparent 0%, rgba(0, 0, 0, 0.7) 100%);
  pointer-events: none;
}

.three-canvas {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
  z-index: 0;
}

.content-container {
  position: relative;
  width: 100%;
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1;
  padding: 2rem;
}
</style>
