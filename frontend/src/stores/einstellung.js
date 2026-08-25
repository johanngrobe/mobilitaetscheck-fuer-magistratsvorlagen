import { ref } from 'vue'
import { defineStore } from 'pinia'
import { apiClient } from '@/services/axios'

export const useEinstellungStore = defineStore('einstellung', () => {
  const einstellung = ref({})
  const isLoaded = ref(false)

  async function fetchEinstellung() {
    try {
      const res = await apiClient.get('/public/plattform-einstellung')
      einstellung.value = res.data
    } catch {
      einstellung.value = {}
    } finally {
      isLoaded.value = true
    }
  }

  return { einstellung, isLoaded, fetchEinstellung }
})
