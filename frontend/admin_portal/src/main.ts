import { createApp } from 'vue'
import App from './App.vue'
import Toast from 'vue-toastification'

// Import styles
import './style.css'
import 'vue-toastification/dist/index.css'

// Create app
const app = createApp(App)

// Use plugins
app.use(Toast, {
  position: 'top-right',
  timeout: 3000,
  closeOnClick: true,
  pauseOnFocusLoss: true,
  pauseOnHover: true,
  draggable: true,
  draggablePercent: 0.6,
  showCloseButtonOnHover: false,
  hideProgressBar: false,
  closeButton: 'button',
  icon: true,
  rtl: false
})

// Mount app
app.mount('#app')
