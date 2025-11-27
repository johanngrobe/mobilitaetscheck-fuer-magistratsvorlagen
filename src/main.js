import '@/assets/main.css'
import 'primeicons/primeicons.css'
import { createApp } from 'vue'
import { createPinia } from 'pinia'
import { localeDe } from './utils/translation'
import { definePreset } from '@primeuix/themes'
import App from './App.vue'
import router from './router'
import PrimeVue from 'primevue/config'
import Aura from '@primeuix/themes/aura'
import BaseAlert from './components/BaseAlert.vue'
import BaseCard from './components/BaseCard.vue'
import BaseButton from './components/BaseButton.vue'
import BaseModal from './components/BaseModal.vue'
import BaseSpinner from './components/BaseSpinner.vue'
import BaseHeading from './components/BaseHeading.vue'
import BaseSubheading from './components/BaseSubheading.vue'
import ToastService from 'primevue/toastservice'
import { setupToast } from '@/services/toast'
import ConfirmationService from 'primevue/confirmationservice'
import Tooltip from 'primevue/tooltip'

const MyPreset = definePreset(Aura, {
  semantic: {
    primary: {
      50: '#E9F2F9', // Optional, or choose a calculated value
      100: '#D1E5F4',
      200: '#A0CCE9',
      300: '#75B3D7',
      400: '#6297B6',
      500: '#507C96',
      600: '#3F6378',
      700: '#2E4A5B',
      800: '#1F333F',
      900: '#101D25',
      950: '#081218' // Optional dark shade
    },
    secondary: {
      50: '#FAFAFA',
      100: '#F4F4F5',
      200: '#E4E4E7',
      300: '#D4D4D8',
      400: '#A1A1AA',
      500: '#71717A',
      600: '#52525B',
      700: '#3F3F46',
      800: '#27272A',
      900: '#18181B',
      950: '#0B0B0E'
    },
    colorScheme: {
      light: {
        primary: {
          color: '{primary.600}',
          inverseColor: '#ffffff',
          hoverColor: '{primary.500}',
          activeColor: '{primary.600}'
        },
        highlight: {
          background: '{primary.500}',
          focusBackground: '{primary.600}',
          color: '#ffffff',
          focusColor: '#ffffff'
        }
      }
    }
  }
})

const app = createApp(App)

app.directive('tooltip', Tooltip)

app.component('BaseAlert', BaseAlert)
app.component('BaseCard', BaseCard)
app.component('BaseButton', BaseButton)
app.component('BaseModal', BaseModal)
app.component('BaseSpinner', BaseSpinner)
app.component('BaseHeading', BaseHeading)
app.component('BaseSubheading', BaseSubheading)

app.use(createPinia())
app.use(ToastService)
app.use(ConfirmationService)
setupToast(app, app.config.globalProperties.$toast)
app.use(router)
app.use(PrimeVue, {
  theme: {
    preset: MyPreset,
    options: {
      darkModeSelector: false || 'none'
    }
  },
  locale: localeDe
})

app.mount('#app')
