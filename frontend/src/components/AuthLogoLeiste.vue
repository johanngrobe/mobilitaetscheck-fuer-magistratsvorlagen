<template>
  <div v-if="brandingStore.loginLogos.length > 0" class="flex items-center justify-center gap-x-6 h-10 mx-auto mb-4">
    <img v-for="logo in brandingStore.loginLogos" :key="logo.id" :src="logo.asset.url" alt="Logo" class="h-10" />
  </div>
  <div v-else class="flex items-center justify-center gap-x-6 h-10 mx-auto mb-4">
    <img src="../assets/logos/HSRM_Unterzeile_farbig_RGB.png" alt="Logo" class="h-10" />
    <img src="../assets/logos/Pimoo-Logo-Primaer.png" alt="Logo" class="h-10" />
    <img src="../assets/logos/oberursel-logo.webp" alt="Logo" class="h-11" />
  </div>
</template>

<script setup>
import { useBrandingStore } from '@/stores/branding'

const brandingStore = useBrandingStore()
</script>
