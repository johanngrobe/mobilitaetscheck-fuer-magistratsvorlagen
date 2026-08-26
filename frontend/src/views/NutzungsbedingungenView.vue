<template>
  <div>
    <BaseHeading>Nutzungsbedingungen</BaseHeading>

    <BaseSpinner v-if="isLoading" />
    <div v-else-if="modus === 'url' && url">
      <p>
        Die Nutzungsbedingungen finden Sie unter folgendem Link:
        <a class="text-blue-600 hover:underline" :href="url" target="_blank" rel="noopener noreferrer">{{
          url
        }}</a>
      </p>
    </div>
    <div v-else-if="inhalt" v-html="inhalt" />
    <p v-else class="text-gray-400">Keine Nutzungsbedingungen hinterlegt.</p>
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
    modus.value = res.data.nutzungsbedingungenModus || 'inhalt'
    inhalt.value = res.data.nutzungsbedingungenInhalt || ''
    url.value = res.data.nutzungsbedingungenUrl || ''
  } catch {
    modus.value = 'inhalt'
    inhalt.value = ''
    url.value = ''
  } finally {
    isLoading.value = false
  }
})
</script>
