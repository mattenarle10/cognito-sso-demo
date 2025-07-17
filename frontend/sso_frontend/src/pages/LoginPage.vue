<template>
  <div class="min-h-screen bg-gradient-to-br from-neutral-950 via-black to-zinc-950 relative overflow-hidden">
    <!-- Enhanced 3D background textures -->
    <div class="absolute inset-0 bg-[radial-gradient(ellipse_80%_80%_at_50%_-20%,rgba(120,119,198,0.05),transparent)]" />
    <div class="absolute inset-0 bg-[radial-gradient(ellipse_80%_80%_at_80%_80%,rgba(120,119,198,0.04),transparent)]" />
    <div class="absolute inset-0 bg-[linear-gradient(to_right,#80808015_1px,transparent_1px),linear-gradient(to_bottom,#80808015_1px,transparent_1px)] bg-[size:24px_24px]" />

    <!-- Enhanced noise texture overlay -->
    <div
      class="absolute inset-0 opacity-[0.025]"
      style="
        background-image: url('data:image/svg+xml,%3Csvg viewBox=\'0 0 256 256\' xmlns=\'http://www.w3.org/2000/svg\'%3E%3Cfilter id=\'noiseFilter\'%3E%3CfeTurbulence type=\'fractalNoise\' baseFrequency=\'0.9\' numOctaves=\'4\' stitchTiles=\'stitch\'/%3E%3C/filter%3E%3Crect width=\'100%25\' height=\'100%25\' filter=\'url(%23noiseFilter)\'/%3E%3C/svg%3E');
      "
    />
    
    <!-- 3D Canvas background -->
    <div ref="threeContainer" class="absolute inset-0 z-0 opacity-40"></div>

    <!-- Main container - centered layout -->
    <div class="min-h-screen flex items-center justify-center p-8">
      <div class="w-full max-w-md relative">
        <!-- Form container with enhanced textures -->
        <div class="relative transform-gpu transition-all duration-500 hover:scale-[1.01]" :style="cardStyle">
          <!-- Enhanced 3D glow effects -->
          <div class="absolute -inset-3 bg-gradient-to-r from-zinc-800/30 to-neutral-800/30 rounded-3xl blur-xl" />
          <div class="absolute -inset-1 bg-gradient-to-br from-zinc-700/20 to-zinc-900/20 rounded-3xl blur-lg" />
          <div class="absolute -inset-0 bg-gradient-to-tr from-zinc-800/5 via-zinc-600/5 to-zinc-900/5 rounded-3xl" />

          <div ref="cardContainer" class="relative bg-gradient-to-b from-zinc-900/95 to-black/98 backdrop-blur-xl border border-zinc-800/60 rounded-2xl p-8 lg:p-10 overflow-hidden">
            <!-- Card texture overlays -->
            <div class="absolute inset-0 bg-gradient-to-br from-zinc-800/5 via-transparent to-zinc-900/10 rounded-2xl" />
            <div class="absolute inset-0 bg-[radial-gradient(circle_at_30%_20%,rgba(255,255,255,0.01)_0%,transparent_50%)]" />
            <div class="absolute inset-0 bg-[radial-gradient(circle_at_70%_80%,rgba(255,255,255,0.008)_0%,transparent_50%)]" />

            <!-- Subtle grain texture on card -->
            <div
              class="absolute inset-0 opacity-[0.03] rounded-2xl"
              style="
                background-image: url('data:image/svg+xml,%3Csvg viewBox=\'0 0 200 200\' xmlns=\'http://www.w3.org/2000/svg\'%3E%3Cfilter id=\'cardNoise\'%3E%3CfeTurbulence type=\'fractalNoise\' baseFrequency=\'0.65\' numOctaves=\'3\' seed=\'1\' stitchTiles=\'stitch\'/%3E%3C/filter%3E%3Crect width=\'100%25\' height=\'100%25\' filter=\'url(%23cardNoise)\'/%3E%3C/svg%3E');
              "
            />

            <!-- Subtle border highlight -->
            <div class="absolute inset-0 rounded-2xl bg-gradient-to-r from-transparent via-zinc-600/20 to-transparent p-[1px]">
              <div class="w-full h-full bg-transparent rounded-2xl" />
            </div>

            <div class="relative z-10">
              <!-- Enhanced header section -->
              <div class="mb-12 relative">
                <div class="absolute -top-10 -right-10 w-40 h-40 bg-gradient-to-br from-blue-500/5 to-purple-500/5 rounded-full blur-3xl"></div>
                <h1 class="text-4xl lg:text-5xl font-medium tracking-tight text-white mb-4 bg-gradient-to-r from-white via-zinc-100 to-zinc-300 bg-clip-text text-transparent relative">
                  <span class="relative inline-block transform transition-all duration-500 hover:scale-105">Sign In</span>
                </h1>
                <p class="text-zinc-400 font-light tracking-wide" v-if="appName">Welcome back to {{ appName }}</p>
                <p class="text-zinc-400 font-light tracking-wide" v-else>Welcome back to continue your journey</p>
              </div>

              <!-- Form with enhanced styling -->
              <form @submit.prevent="handleLogin" class="space-y-8">
                <div class="space-y-3 relative">
                  <label
                    for="email"
                    class="text-zinc-300 font-medium tracking-wide text-sm block flex items-center gap-2"
                  >
                    <MailIcon :size="14" class="text-zinc-500" />
                    Email Address
                  </label>
                  <div class="relative">
                    <input
                      id="email"
                      type="email"
                      placeholder="your@email.com"
                      v-model="formData.email"
                      required
                      class="bg-zinc-900/60 border border-zinc-700/60 text-white placeholder:text-zinc-500 focus:border-zinc-400 focus:ring-1 focus:ring-zinc-400 h-14 rounded-xl font-light tracking-wide text-base transition-all duration-200 pl-4 relative w-full"
                    />
                    <!-- Input field texture -->
                    <div class="absolute inset-0 bg-gradient-to-r from-zinc-800/5 to-transparent rounded-xl pointer-events-none" />
                  </div>
                  <p v-if="errors.email" class="text-red-400 text-sm mt-1">{{ errors.email }}</p>
                </div>

                <div class="space-y-3 relative">
                  <label
                    for="password"
                    class="text-zinc-300 font-medium tracking-wide text-sm block flex items-center gap-2"
                  >
                    <LockIcon :size="14" class="text-zinc-500" />
                    Password
                  </label>
                  <div class="relative">
                    <input
                      id="password"
                      type="password"
                      placeholder="Enter your password"
                      v-model="formData.password"
                      required
                      class="bg-zinc-900/60 border border-zinc-700/60 text-white placeholder:text-zinc-500 focus:border-zinc-400 focus:ring-1 focus:ring-zinc-400 h-14 rounded-xl font-light tracking-wide text-base transition-all duration-200 pl-4 relative w-full"
                    />
                    <!-- Input field texture -->
                    <div class="absolute inset-0 bg-gradient-to-r from-zinc-800/5 to-transparent rounded-xl pointer-events-none" />
                  </div>
                  <p v-if="errors.password" class="text-red-400 text-sm mt-1">{{ errors.password }}</p>
                </div>

                <button
                  type="submit"
                  :disabled="!isFormValid || loading"
                  class="w-full bg-gradient-to-r from-zinc-700 to-zinc-800 hover:from-zinc-600 hover:to-zinc-700 text-white font-medium tracking-wide py-4 h-14 rounded-xl transition-all duration-300 shadow-lg hover:shadow-xl border border-zinc-600/30 group relative overflow-hidden disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  <!-- Button texture -->
                  <div class="absolute inset-0 bg-gradient-to-r from-zinc-600/10 via-transparent to-zinc-800/10" />
                  <span class="group-hover:tracking-wider transition-all duration-200 flex items-center justify-center gap-2 relative z-10">
                    <span v-if="loading" class="inline-block animate-spin mr-2">⏳</span>
                    Sign In
                    <ArrowRightIcon :size="16" class="group-hover:translate-x-1 transition-transform duration-200" />
                  </span>
                </button>
              </form>

              <!-- Error Display -->
              <div v-if="error" class="mt-6 p-4 bg-red-900/20 border border-red-800/30 rounded-xl text-red-400 text-sm">
                {{ error }}
              </div>

              <!-- Footer with better styling -->
              <div class="mt-10 pt-8 border-t border-zinc-800/50 relative">
                <!-- Border texture -->
                <div class="absolute top-0 left-0 right-0 h-[1px] bg-gradient-to-r from-transparent via-zinc-700/30 to-transparent" />
                <p class="text-center text-zinc-400 font-light">
                  Don't have an account?
                  <router-link
                    :to="registerLink"
                    class="text-zinc-200 hover:text-white font-medium underline underline-offset-4 decoration-zinc-600 hover:decoration-zinc-400 transition-all duration-200 inline-flex items-center gap-1"
                  >
                    Create your account
                    <ArrowRightIcon :size="12" class="opacity-60" />
                  </router-link>
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onBeforeUnmount } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useMouseInElement } from '@vueuse/core'
import type { LoginCredentials } from '../types/auth'
import { cognitoService } from '../services/cognitoService'
import { useApi } from '../composables/useApi'
import { Mail as MailIcon, Lock as LockIcon, ArrowRight as ArrowRightIcon } from 'lucide-vue-next'
import * as THREE from 'three'

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

// 3D effect refs
const threeContainer = ref<HTMLElement | null>(null)
const cardContainer = ref<HTMLElement | null>(null)
const { elementX, elementY, isOutside } = useMouseInElement(cardContainer)

// 3D tilt effect for card
const cardStyle = computed(() => {
  if (isOutside.value) return {}
  
  const maxTilt = 2
  const tiltX = maxTilt * ((elementY.value / 300) - 0.5) * 2
  const tiltY = maxTilt * ((elementX.value / 300) - 0.5) * -2
  
  return {
    transform: `perspective(1000px) rotateX(${tiltX}deg) rotateY(${tiltY}deg)`,
    boxShadow: `
      ${-tiltY * 5}px ${tiltX * 5}px 20px rgba(0,0,0,0.2),
      0 10px 20px rgba(0,0,0,0.1)
    `
  }
})

// Three.js scene setup
let scene: THREE.Scene
let camera: THREE.PerspectiveCamera
let renderer: THREE.WebGLRenderer
let particles: THREE.Points
let animationFrameId: number

const initThreeScene = () => {
  if (!threeContainer.value) return
  
  // Setup scene
  scene = new THREE.Scene()
  camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000)
  renderer = new THREE.WebGLRenderer({ alpha: true })
  renderer.setSize(window.innerWidth, window.innerHeight)
  threeContainer.value.appendChild(renderer.domElement)
  
  // Create particles
  const particlesGeometry = new THREE.BufferGeometry()
  const particlesCount = 500
  const posArray = new Float32Array(particlesCount * 3)
  
  for (let i = 0; i < particlesCount * 3; i++) {
    posArray[i] = (Math.random() - 0.5) * 5
  }
  
  particlesGeometry.setAttribute('position', new THREE.BufferAttribute(posArray, 3))
  
  const particlesMaterial = new THREE.PointsMaterial({
    size: 0.005,
    color: 0xffffff,
    transparent: true,
    opacity: 0.8,
  })
  
  particles = new THREE.Points(particlesGeometry, particlesMaterial)
  scene.add(particles)
  
  camera.position.z = 2
  
  // Animation function
  const animate = () => {
    animationFrameId = requestAnimationFrame(animate)
    particles.rotation.y += 0.0005
    particles.rotation.x += 0.0002
    renderer.render(scene, camera)
  }
  
  animate()
  
  // Handle resize
  const handleResize = () => {
    camera.aspect = window.innerWidth / window.innerHeight
    camera.updateProjectionMatrix()
    renderer.setSize(window.innerWidth, window.innerHeight)
  }
  
  window.addEventListener('resize', handleResize)
}

// URL parameters from client app redirect
onMounted(() => {
  appName.value = route.query.application_name as string || ''
  channelId.value = route.query.channel_id as string || ''
  
  // todo: validate app/channel with backend
  console.log('App:', appName.value, 'Channel:', channelId.value)
  
  // Initialize Three.js scene
  initThreeScene()
})

onBeforeUnmount(() => {
  // Clean up Three.js resources
  if (animationFrameId) {
    cancelAnimationFrame(animationFrameId)
  }
  
  if (renderer) {
    renderer.dispose()
  }
  
  window.removeEventListener('resize', () => {})
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

<style>
/* All styles are now handled with Tailwind classes */
</style> 