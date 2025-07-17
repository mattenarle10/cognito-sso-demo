<template>
  <div class="orders-container">
    <h1>My Orders</h1>
    
    <div v-if="loading" class="loading-state">
      <p>Loading your orders...</p>
    </div>
    
    <div v-else-if="error" class="error-state">
      <p>{{ error }}</p>
      <button @click="fetchOrders" class="retry-button">Retry</button>
    </div>
    
    <div v-else-if="orders.length === 0" class="empty-state">
      <p>You don't have any orders yet.</p>
    </div>
    
    <div v-else class="orders-list">
      <table class="orders-table">
        <thead>
          <tr>
            <th>Order ID</th>
            <th>Date</th>
            <th>Items</th>
            <th>Total</th>
            <th>Status</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="order in orders" :key="order.order_id">
            <td>{{ order.order_id }}</td>
            <td>{{ formatDate(order.created_at) }}</td>
            <td>
              <ul class="items-list">
                <li v-for="(item, index) in order.items" :key="index">
                  {{ item.quantity }}x {{ item.name }}
                </li>
              </ul>
            </td>
            <td>${{ formatPrice(order.total) }}</td>
            <td>
              <span :class="'status-badge status-' + order.status.toLowerCase()">
                {{ order.status }}
              </span>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useAuthStore } from '../stores/authStore'
import axios from 'axios'

interface OrderItem {
  name: string
  quantity: number
  price: number
}

interface Order {
  order_id: string
  user_id: string
  items: OrderItem[]
  total: number
  status: string
  created_at: string
}

const authStore = useAuthStore()
const orders = ref<Order[]>([])
const loading = ref(false)
const error = ref('')

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
function formatPrice(price: number) {
  return price.toFixed(2)
}

// Fetch orders on component mount
onMounted(() => {
  fetchOrders()
})
</script>

<style scoped>
.orders-container {
  padding: 20px 0;
}

.orders-container h1 {
  margin-bottom: 30px;
  color: #6b4226;
}

.loading-state,
.error-state,
.empty-state {
  text-align: center;
  padding: 40px;
  background-color: #f8f5f2;
  border-radius: 8px;
}

.retry-button {
  background-color: #6b4226;
  color: white;
  border: none;
  padding: 8px 15px;
  border-radius: 4px;
  cursor: pointer;
  margin-top: 15px;
}

.orders-table {
  width: 100%;
  border-collapse: collapse;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.orders-table th,
.orders-table td {
  padding: 15px;
  text-align: left;
  border-bottom: 1px solid #eee;
}

.orders-table th {
  background-color: #f8f5f2;
  color: #6b4226;
}

.orders-table tr:last-child td {
  border-bottom: none;
}

.items-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.status-badge {
  display: inline-block;
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 0.8rem;
  font-weight: bold;
}

.status-completed {
  background-color: #d1e7dd;
  color: #0f5132;
}

.status-processing {
  background-color: #cff4fc;
  color: #055160;
}

.status-pending {
  background-color: #fff3cd;
  color: #664d03;
}
</style>
