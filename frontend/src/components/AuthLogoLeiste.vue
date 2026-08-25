<template>
  <div v-if="logos.length > 0" class="flex items-center justify-center gap-x-6 h-10 mx-auto mb-4">
    <img v-for="logo in logos" :key="logo.id" :src="logo.asset.url" alt="Logo" class="h-10" />
  </div>
  <div v-else class="flex items-center justify-center gap-x-6 h-10 mx-auto mb-4">
    <img src="../assets/logos/HSRM_Unterzeile_farbig_RGB.png" alt="Logo" class="h-10" />
    <img src="../assets/logos/Pimoo-Logo-Primaer.png" alt="Logo" class="h-10" />
    <img src="../assets/logos/oberursel-logo.webp" alt="Logo" class="h-11" />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { apiClient } from '@/services/axios'

const logos = ref([])

onMounted(async () => {
  try {
    const res = await apiClient.get('/branding/logo-listen/login')
    logos.value = res.data
  } catch {
    logos.value = []
  }
})
</script>
