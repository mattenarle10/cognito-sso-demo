<template>
  <div class="orders-page min-h-screen bg-black text-white overflow-hidden">
    <!-- Header -->
    <header class="fixed top-0 left-0 right-0 z-50 px-8 py-6">
      <nav class="flex items-center justify-between max-w-7xl mx-auto">
        <div class="flex items-center">
          <button @click="router.push('/')" class="back-button">
            <svg class="back-icon" viewBox="0 0 24 24" fill="none">
              <path d="M19 12H5" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              <path d="M12 19L5 12L12 5" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
            BACK
          </button>
        </div>
        <div class="text-2xl font-light tracking-[0.2em]"></div>
        <div class="flex items-center">
          <UserDropdown :userName="getUserDisplayName()" />
        </div>
      </nav>
    </header>
    
    <!-- Animated Background -->
    <div class="fixed inset-0 bg-gradient">
      <!-- Animated dots -->
      <div v-for="i in 8" :key="i" class="animated-dot" :style="getRandomDotStyle(i)"></div>
    </div>
    
    <!-- Main Content -->
    <main class="relative z-10 flex items-center justify-center min-h-screen px-8 pt-24 pb-12">
      <div class="orders-wrapper w-full">
        <div class="title-section">
        </div>
        
        <!-- Create Order Section -->
        <div class="create-order-card">
          <h2 class="section-title">Products</h2>
          
          <div class="menu-grid">
            <div 
              v-for="item in menuItems" 
              :key="item.id"
              @click="selectItem(item)"
              :class="['menu-item', { 'selected': selectedItem?.id === item.id }]"
            >
              <div class="item-info">
                <h3>{{ item.name }}</h3>
                <p class="item-description">{{ item.description }}</p>
                <div class="item-price">₱{{ item.price }}</div>
              </div>
            </div>
          </div>
          
          <div v-if="selectedItem" class="order-controls">
            <div class="quantity-control">
              <button @click="decrementQuantity" class="qty-button">
                <svg viewBox="0 0 24 24" fill="none">
                  <path d="M5 12H19" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
                </svg>
              </button>
              <span class="quantity">{{ quantity }}</span>
              <button @click="incrementQuantity" class="qty-button">
                <svg viewBox="0 0 24 24" fill="none">
                  <path d="M12 5V19" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
                  <path d="M5 12H19" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
                </svg>
              </button>
            </div>
            
            <button 
              @click="createOrder" 
              :disabled="creatingOrder"
              class="create-order-button"
            >
              {{ creatingOrder ? 'ORDERING...' : `ORDER NOW — ₱${totalPrice}` }}
            </button>
          </div>
        </div>
        
        <!-- Orders History -->
        <div class="orders-history-card">
          <h2 class="section-title">Order History</h2>
          
          <div v-if="loading" class="loading-state">
            <div class="spinner"></div>
            <p class="loading-text">Loading your orders...</p>
          </div>
          
          <div v-else-if="error" class="error-state">
            <svg class="error-icon" viewBox="0 0 24 24" fill="none">
              <circle cx="12" cy="12" r="10" stroke="currentColor" stroke-width="2"/>
              <path d="M15 9L9 15" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
              <path d="M9 9L15 15" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
            </svg>
            <p>{{ error }}</p>
            <button @click="fetchOrders" class="retry-button">RETRY</button>
          </div>
          
          <div v-else-if="orders.length === 0" class="empty-state">
            <svg class="empty-icon" viewBox="0 0 100 100" fill="none">
              <!-- Coffee cup SVG -->
              <path d="M20 35H15C12.2386 35 10 37.2386 10 40V50C10 52.7614 12.2386 55 15 55H20" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
              <path d="M20 25H70V70C70 75.5228 65.5228 80 60 80H30C24.4772 80 20 75.5228 20 70V25Z" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
              <path d="M25 25V20C25 17.2386 27.2386 15 30 15H60C62.7614 15 65 20V25" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
              <!-- Steam lines -->
              <path d="M35 10C35 8 36 6 36 4" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" opacity="0.6"/>
              <path d="M45 10C45 8 46 6 46 4" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" opacity="0.6"/>
              <path d="M55 10C55 8 56 6 56 4" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" opacity="0.6"/>
            </svg>
            <p class="empty-text">No orders yet.<br/>Time for your first brew.</p>
          </div>
          
          <div v-else class="orders-list">
            <div v-for="order in orders" :key="order.order_id" class="order-item">
              <div class="order-header">
                <div class="order-info">
                  <h3>{{ order.item_name || 'Order' }}</h3>
                  <p class="order-date">{{ formatDate(order.created_at) }}</p>
                </div>
                <div class="order-details">
                  <span class="order-quantity">{{ order.quantity }}×</span>
                  <span class="order-price">₱{{ formatPrice(order.total_price || order.total) }}</span>
                  <span :class="'status-badge status-' + (order.status || 'pending').toLowerCase()">
                    {{ (order.status || 'pending').toUpperCase() }}
                  </span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/authStore'
import UserDropdown from '../components/UserDropdown.vue'
import axios from 'axios'

interface MenuItem {
  id: number
  name: string
  description: string
  price: number
}

interface Order {
  order_id: string
  user_id: string
  item_name?: string
  quantity?: number
  total_price?: number
  total?: number
  status: string
  created_at: string
}

const router = useRouter()
const authStore = useAuthStore()
const orders = ref<Order[]>([])
const loading = ref(false)
const error = ref('')
const creatingOrder = ref(false)
const selectedItem = ref<MenuItem | null>(null)
const quantity = ref(1)

// Filipino coffee menu items
const menuItems = ref<MenuItem[]>([
  {
    id: 1,
    name: 'Ca Phe Sua Da',
    description: 'vietnamese iced coffee with sweetened condensed milk',
    price: 85
  },
  {
    id: 2,
    name: 'Kapeng Barako',
    description: 'strong native filipino coffee',
    price: 75
  },
  {
    id: 3,
    name: 'Salabat Latte',
    description: 'ginger tea latte with steamed milk',
    price: 95
  },
  {
    id: 4,
    name: 'Tsokolate Eh',
    description: 'thick filipino hot chocolate',
    price: 120
  },
  {
    id: 5,
    name: 'Kape Con Leche',
    description: 'coffee with milk, filipino style',
    price: 80
  },
  {
    id: 6,
    name: 'Ube Frappuccino',
    description: 'purple yam blended coffee drink',
    price: 140
  }
])

// Computed total price
const totalPrice = computed(() => {
  if (!selectedItem.value) return 0
  return selectedItem.value.price * quantity.value
})

// Function to get user display name
function getUserDisplayName(): string {
  return authStore.user?.name || 'User'
}

// Menu item selection
function selectItem(item: MenuItem) {
  selectedItem.value = item
  quantity.value = 1
}

// Quantity controls
function incrementQuantity() {
  quantity.value++
}

function decrementQuantity() {
  if (quantity.value > 1) {
    quantity.value--
  }
}

// Create new order
async function createOrder() {
  if (!selectedItem.value) return
  
  creatingOrder.value = true
  error.value = ''
  
  try {
    const idToken = authStore.tokens?.id_token
    if (!idToken) {
      throw new Error('Not authenticated')
    }
    
    const orderData = {
      item_name: selectedItem.value.name,
      quantity: quantity.value,
      price_per_item: selectedItem.value.price
    }
    
    const response = await axios.post(`${import.meta.env.VITE_CLIENT_API_URL}/orders`, orderData, {
      headers: {
        Authorization: `Bearer ${idToken}`,
        'Content-Type': 'application/json'
      }
    })
    
    if (response.data.success) {
      // Reset form
      selectedItem.value = null
      quantity.value = 1
      // Refresh orders list
      await fetchOrders()
    }
    
  } catch (err: any) {
    console.error('Failed to create order:', err)
    error.value = err.response?.data?.message || 'Failed to create order. Please try again.'
  } finally {
    creatingOrder.value = false
  }
}

// Fetch orders from the client backend API
async function fetchOrders() {
  loading.value = true
  error.value = ''
  
  try {
    // Get ID token from auth store
    const idToken = authStore.tokens?.id_token
    
    if (!idToken) {
      throw new Error('Not authenticated')
    }
    
    // Call the client backend API with the ID token
    const response = await axios.get(`${import.meta.env.VITE_CLIENT_API_URL}/orders`, {
      headers: {
        Authorization: `Bearer ${idToken}`
      }
    })
    
    // Update orders state
    orders.value = response.data.data.orders || []
    
  } catch (err: any) {
    console.error('Failed to fetch orders:', err)
    error.value = err.response?.data?.message || 'Failed to fetch orders. Please try again.'
  } finally {
    loading.value = false
  }
}

// Format date for display
function formatDate(dateString: string) {
  return new Date(dateString).toLocaleDateString()
}

// Format price for display
function formatPrice(price: number | undefined) {
  return (price || 0).toFixed(2)
}

// Generate random dot styles for background animation
function getRandomDotStyle(index: number) {
  const positions = [
    { top: '25%', left: '15%', size: '12px', delay: '0s', duration: '8s' },
    { top: '65%', left: '80%', size: '8px', delay: '0.5s', duration: '10s' },
    { top: '35%', right: '20%', size: '15px', delay: '1s', duration: '9s' },
    { top: '75%', left: '30%', size: '10px', delay: '1.5s', duration: '7s' },
    { top: '15%', right: '15%', size: '14px', delay: '2s', duration: '11s' },
    { top: '45%', left: '10%', size: '9px', delay: '2.5s', duration: '9s' },
    { top: '85%', right: '25%', size: '11px', delay: '3s', duration: '10s' },
    { top: '55%', left: '70%', size: '13px', delay: '3.5s', duration: '8s' },
  ]
  
  const pos = positions[index % positions.length]
  return {
    ...pos,
    width: pos.size,
    height: pos.size,
    animationDelay: pos.delay,
    animationDuration: pos.duration,
    opacity: (Math.random() * 0.3 + 0.1).toString()
  }
}

// Fetch orders on component mount
onMounted(() => {
  fetchOrders()
})
</script>

<style scoped>
/* Base styles */
.orders-page {
  min-height: 100vh;
  background-color: #000;
  color: #fff;
  overflow: hidden;
  font-family: system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
}

/* Header styles */
header {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 50;
  padding: 1.5rem 2rem;
}

nav {
  display: flex;
  align-items: center;
  justify-content: space-between;
  max-width: 80rem;
  margin: 0 auto;
}

.text-2xl {
  font-size: 1.5rem;
  font-weight: 300;
  letter-spacing: 0.2em;
}

.back-button {
  background-color: transparent;
  border: 1px solid rgba(255, 255, 255, 0.2);
  color: #fff;
  padding: 0.5rem 1rem;
  font-size: 0.875rem;
  font-weight: 300;
  letter-spacing: 0.05em;
  cursor: pointer;
  transition: all 0.3s;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.back-button:hover {
  background-color: rgba(255, 255, 255, 0.1);
}

.back-icon {
  width: 1rem;
  height: 1rem;
}

/* Background styles */
.bg-gradient {
  background: linear-gradient(135deg, #000000 0%, #1a1a1a 100%);
}

.animated-dot {
  position: absolute;
  background-color: rgba(255, 255, 255, 0.15);
  border-radius: 50%;
  animation: float 10s infinite ease-in-out;
}

@keyframes float {
  0%, 100% { transform: translateY(0) rotate(0deg); }
  25% { transform: translateY(-20px) rotate(90deg); }
  50% { transform: translateY(0) rotate(180deg); }
  75% { transform: translateY(20px) rotate(270deg); }
}

/* Main content styles */
main {
  position: relative;
  z-index: 10;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  justify-content: center;
  padding: 8rem 2rem 4rem;
}

.orders-wrapper {
  width: 100%;
  max-width: 70rem;
  margin: 0 auto;
  display: flex;
  flex-direction: column;
  gap: 4rem;
}

/* Title section */
.title-section {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 2rem;
}

.main-title {
  font-size: 4rem;
  font-weight: 100;
  letter-spacing: -0.02em;
  line-height: 1;
  text-align: center;
}

.divider {
  width: 1px;
  height: 5rem;
  background-color: rgba(255, 255, 255, 0.2);
}

/* Card styles */
.create-order-card, .orders-history-card {
  background-color: rgba(15, 15, 15, 0.6);
  border-radius: 0;
  overflow: hidden;
  box-shadow: 0 25px 50px rgba(0, 0, 0, 0.4);
  backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.06);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.section-title {
  font-size: 1.5rem;
  font-weight: 300;
  margin-bottom: 2rem;
  padding: 3rem 3rem 0;
  letter-spacing: 0.05em;
  color: rgba(255, 255, 255, 0.9);
}

/* Menu grid */
.menu-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
  gap: 1.5rem;
  padding: 0 3rem;
  margin-bottom: 3rem;
}

.menu-item {
  background-color: rgba(255, 255, 255, 0.03);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 0;
  padding: 2rem;
  cursor: pointer;
  transition: all 0.4s ease;
}

.menu-item:hover {
  background-color: rgba(255, 255, 255, 0.06);
  transform: translateY(-4px);
  border-color: rgba(255, 255, 255, 0.15);
}

.menu-item.selected {
  background-color: rgba(255, 255, 255, 0.1);
  border-color: rgba(255, 255, 255, 0.2);
}

.item-info h3 {
  font-size: 1.25rem;
  font-weight: 400;
  margin-bottom: 0.75rem;
  letter-spacing: -0.01em;
}

.item-description {
  font-size: 0.9rem;
  color: rgba(255, 255, 255, 0.6);
  margin-bottom: 1.5rem;
  line-height: 1.5;
  font-weight: 300;
}

.item-price {
  font-size: 1.5rem;
  font-weight: 300;
  color: #fff;
  letter-spacing: -0.01em;
}

/* Order controls */
.order-controls {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 3rem 3rem;
  gap: 3rem;
}

.quantity-control {
  display: flex;
  align-items: center;
  gap: 1.5rem;
  background-color: rgba(255, 255, 255, 0.03);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 0;
  padding: 1rem 1.5rem;
}

.qty-button {
  background-color: transparent;
  border: 1px solid rgba(255, 255, 255, 0.15);
  color: #fff;
  width: 2.5rem;
  height: 2.5rem;
  border-radius: 0;
  cursor: pointer;
  transition: all 0.3s;
  display: flex;
  align-items: center;
  justify-content: center;
}

.qty-button:hover {
  background-color: rgba(255, 255, 255, 0.1);
  border-color: rgba(255, 255, 255, 0.3);
}

.qty-button svg {
  width: 1rem;
  height: 1rem;
}

.quantity {
  font-size: 1.25rem;
  font-weight: 300;
  min-width: 3rem;
  text-align: center;
  letter-spacing: -0.01em;
}

.create-order-button {
  background-color: #fff;
  color: #000;
  border: none;
  padding: 1.25rem 3rem;
  font-size: 1rem;
  font-weight: 300;
  letter-spacing: 0.05em;
  border-radius: 0;
  cursor: pointer;
  transition: all 0.3s ease;
  min-width: 250px;
}

.create-order-button:hover:not(:disabled) {
  background-color: rgba(255, 255, 255, 0.9);
  transform: scale(1.02);
}

.create-order-button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

/* Loading and error states */
.loading-state, .error-state, .empty-state {
  text-align: center;
  padding: 4rem 3rem;
}

.loading-text {
  font-weight: 300;
  color: rgba(255, 255, 255, 0.7);
}

.spinner {
  width: 2rem;
  height: 2rem;
  border: 2px solid rgba(255, 255, 255, 0.1);
  border-top: 2px solid rgba(255, 255, 255, 0.6);
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin: 0 auto 1.5rem;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.empty-icon, .error-icon {
  width: 4rem;
  height: 4rem;
  margin: 0 auto 1.5rem;
  color: rgba(255, 255, 255, 0.4);
}

.empty-text {
  font-weight: 300;
  color: rgba(255, 255, 255, 0.7);
  line-height: 1.5;
}

.retry-button {
  background-color: rgba(255, 255, 255, 0.06);
  border: 1px solid rgba(255, 255, 255, 0.15);
  color: #fff;
  padding: 0.75rem 2rem;
  border-radius: 0;
  cursor: pointer;
  transition: all 0.3s;
  margin-top: 1.5rem;
  font-weight: 300;
  letter-spacing: 0.05em;
}

.retry-button:hover {
  background-color: rgba(255, 255, 255, 0.1);
}

/* Orders list */
.orders-list {
  padding: 0 3rem 3rem;
}

.order-item {
  background-color: rgba(255, 255, 255, 0.03);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 0;
  padding: 2rem;
  margin-bottom: 1.5rem;
  transition: all 0.3s ease;
}

.order-item:hover {
  background-color: rgba(255, 255, 255, 0.06);
}

.order-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.order-info h3 {
  font-size: 1.25rem;
  font-weight: 400;
  margin-bottom: 0.5rem;
  letter-spacing: -0.01em;
}

.order-date {
  font-size: 0.875rem;
  color: rgba(255, 255, 255, 0.5);
  margin: 0;
  font-weight: 300;
}

.order-details {
  display: flex;
  align-items: center;
  gap: 1.5rem;
}

.order-quantity {
  font-size: 0.9rem;
  color: rgba(255, 255, 255, 0.7);
  font-weight: 300;
}

.order-price {
  font-size: 1.25rem;
  font-weight: 300;
  color: #fff;
  letter-spacing: -0.01em;
}

.status-badge {
  display: inline-block;
  padding: 0.5rem 1rem;
  border-radius: 0;
  font-size: 0.75rem;
  font-weight: 400;
  letter-spacing: 0.05em;
  border: 1px solid;
}

.status-pending {
  background-color: rgba(255, 193, 7, 0.1);
  color: #ffc107;
  border-color: rgba(255, 193, 7, 0.3);
}

.status-preparing {
  background-color: rgba(13, 202, 240, 0.1);
  color: #0dcaf0;
  border-color: rgba(13, 202, 240, 0.3);
}

.status-completed {
  background-color: rgba(25, 135, 84, 0.1);
  color: #198754;
  border-color: rgba(25, 135, 84, 0.3);
}

.status-cancelled {
  background-color: rgba(220, 53, 69, 0.1);
  color: #dc3545;
  border-color: rgba(220, 53, 69, 0.3);
}

/* Media queries */
@media (min-width: 768px) {
  .main-title {
    font-size: 6rem;
  }
}

@media (max-width: 768px) {
  .main-title {
    font-size: 3rem;
  }
  
  .menu-grid {
    grid-template-columns: 1fr;
    padding: 0 1.5rem;
  }
  
  .order-controls {
    flex-direction: column;
    gap: 2rem;
    padding: 0 1.5rem 2rem;
  }
  
  .create-order-button {
    width: 100%;
  }
  
  .order-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 1rem;
  }
  
  .order-details {
    width: 100%;
    justify-content: space-between;
  }
  
  .section-title {
    padding: 2rem 1.5rem 0;
  }
  
  .orders-list {
    padding: 0 1.5rem 2rem;
  }
}
</style>
