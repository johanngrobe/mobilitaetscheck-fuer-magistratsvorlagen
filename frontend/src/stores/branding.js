import { ref } from 'vue'
import { defineStore } from 'pinia'
import { apiClient } from '@/services/axios'

export const useBrandingStore = defineStore('branding', () => {
  const slots = ref({})
  const footerLogos = ref([])
  const loginLogos = ref([])
  const isLoaded = ref(false)

  async function fetchBranding() {
    try {
      const [slotsRes, footerRes, loginRes] = await Promise.all([
        apiClient.get('/branding'),
        apiClient.get('/branding/logo-listen/footer'),
        apiClient.get('/branding/logo-listen/login')
      ])
      slots.value = Object.fromEntries(slotsRes.data.map((s) => [s.slot, s]))
      footerLogos.value = footerRes.data
      loginLogos.value = loginRes.data
      applyFavicon()
    } catch {
      slots.value = {}
      footerLogos.value = []
      loginLogos.value = []
    } finally {
      isLoaded.value = true
    }
  }

  function url(slot) {
    return slots.value[slot]?.asset?.url || null
  }

  function link(slot) {
    return slots.value[slot]?.link || null
  }

  function applyFavicon() {
    const faviconUrl = url('favicon')
    if (!faviconUrl) return
    let linkEl = document.querySelector("link[rel~='icon']")
    if (!linkEl) {
      linkEl = document.createElement('link')
      linkEl.rel = 'icon'
      document.head.appendChild(linkEl)
    }
    linkEl.href = faviconUrl
  }

  return { slots, footerLogos, loginLogos, isLoaded, fetchBranding, url, link }
})
