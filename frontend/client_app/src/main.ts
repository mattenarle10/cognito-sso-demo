import './style.css'
import './assets/toast.css'

import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router'

// Import Toast Notification
import Toast, { type PluginOptions, POSITION } from 'vue-toastification'
import 'vue-toastification/dist/index.css'

// Toast configuration
const toastOptions: PluginOptions = {
  position: POSITION.TOP_RIGHT, 
  timeout: 3000,
  closeOnClick: true,
  pauseOnFocusLoss: true,
  pauseOnHover: true,
  draggable: true,
  draggablePercent: 0.6,
  showCloseButtonOnHover: true,
  hideProgressBar: false,
  closeButton: 'button',
  icon: true,
  rtl: false,
  // Custom CSS classes for styling
  toastClassName: 'custom-toast',
  bodyClassName: 'custom-toast-body',
  containerClassName: 'custom-toast-container',
  transition: 'Vue-Toastification__fade',
  maxToasts: 5,
  newestOnTop: true,
  filterBeforeCreate: (toast, toasts) => {
    if (toasts.filter(t => t.content === toast.content).length !== 0) {
      // Returning false discards the toast
      return false
    }
    // You can modify the toast here
    return toast
  }
}

// Create app instance
const app = createApp(App)

// Use Pinia for state management
app.use(createPinia())

// Use router
app.use(router)

// Use Toast
app.use(Toast, toastOptions)

// Mount app
app.mount('#app')
