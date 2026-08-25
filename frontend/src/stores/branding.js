import { ref } from 'vue'
import { defineStore } from 'pinia'
import { apiClient } from '@/services/axios'

export const useBrandingStore = defineStore('branding', () => {
  const slots = ref({})
  const isLoaded = ref(false)

  async function fetchBranding() {
    try {
      const res = await apiClient.get('/branding')
      slots.value = Object.fromEntries(res.data.map((s) => [s.slot, s]))
      applyFavicon()
    } catch {
      slots.value = {}
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

  return { slots, isLoaded, fetchBranding, url, link }
})
