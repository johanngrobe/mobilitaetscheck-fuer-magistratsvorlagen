<template>
  <div>
    <BaseHeading>Impressum</BaseHeading>

    <BaseSpinner v-if="isLoading" />
    <div v-else-if="modus === 'url' && url">
      <p>
        Das Impressum finden Sie unter folgendem Link:
        <a class="text-blue-600 hover:underline" :href="url" target="_blank" rel="noopener noreferrer">{{
          url
        }}</a>
      </p>
    </div>
    <div v-else-if="inhalt" v-html="inhalt" />
    <p v-else class="text-gray-400">Kein Impressum hinterlegt.</p>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { apiClient } from '@/services/axios'

const isLoading = ref(false)
const modus = ref('inhalt')
const inhalt = ref('')
const url = ref('')

onMounted(async () => {
  isLoading.value = true
  try {
    const res = await apiClient.get('/public/plattform-einstellung')
    modus.value = res.data.impressumModus || 'inhalt'
    inhalt.value = res.data.impressumInhalt || ''
    url.value = res.data.impressumUrl || ''
  } catch {
    modus.value = 'inhalt'
    inhalt.value = ''
    url.value = ''
  } finally {
    isLoading.value = false
  }
})
</script>
