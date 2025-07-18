import './assets/main.css'
import './assets/toast.css'

import { createApp } from 'vue'
import App from './App.vue'
import router from './router'

// Import Toast Notification
import Toast, { POSITION, type PluginOptions } from 'vue-toastification'
import 'vue-toastification/dist/index.css'

// Toast configuration
const toastOptions: PluginOptions = {
  position: POSITION.TOP_RIGHT, // Centered at the top
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
  transition: 'Vue-Toastification__fade',
  maxToasts: 3,
  newestOnTop: true,
  filterBeforeCreate: (toast, toasts) => {
    if (toasts.filter(t => t.content === toast.content).length !== 0) {
      // Returning false discards the toast
      return false
    }
    // You can modify the toast here
    return toast
  },
  // Custom CSS classes for styling
  toastClassName: 'custom-toast',
  bodyClassName: 'custom-toast-body',
  containerClassName: 'custom-toast-container'
}

const app = createApp(App)

app.use(router)

// Use Toast
app.use(Toast, toastOptions)

app.mount('#app')
