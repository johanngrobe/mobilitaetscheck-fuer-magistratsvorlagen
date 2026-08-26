<template>
  <BaseCard>
    <div class="flex items-center justify-between mb-4">
      <h5 class="text-lg font-semibold">Startseite</h5>
    </div>
    <p class="text-sm text-gray-500 mb-4">
      Dieser Inhalt ersetzt den Hero-Bereich (Titel und Beschreibung) auf der Startseite. Die
      Kommunenauswahl und Liste der Magistratsvorlagen bleiben darunter unverändert bestehen. Leer
      lassen, um den Standardtext anzuzeigen.
    </p>

    <BaseSpinner v-if="isLoading" />
    <template v-else>
      <RichContentEditor v-model="inhalt" />
      <div class="flex justify-between mt-4">
        <Button
          label="Auf Standard zurücksetzen"
          text
          severity="secondary"
          @click="confirmReset"
        />
        <Button label="Speichern" @click="submit" :loading="isSaving" />
      </div>
    </template>
  </BaseCard>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import Button from 'primevue/button'
import { apiClient } from '@/services/axios'
import { useToast } from 'primevue/usetoast'
import { useConfirm } from 'primevue/useconfirm'
import RichContentEditor from './RichContentEditor.vue'
import { STARTSEITE_STANDARD_INHALT } from '@/utils/standardInhalte'

const isLoading = ref(false)
const isSaving = ref(false)
const inhalt = ref('')

const toast = useToast()
const confirm = useConfirm()

const fetchEinstellung = async () => {
  isLoading.value = true
  try {
    const res = await apiClient.get('/admin/einstellung')
    inhalt.value = res.data.startseiteInhalt || STARTSEITE_STANDARD_INHALT
  } catch {
    inhalt.value = STARTSEITE_STANDARD_INHALT
  } finally {
    isLoading.value = false
  }
}

onMounted(fetchEinstellung)

const submit = async () => {
  isSaving.value = true
  try {
    await apiClient.patch('/admin/einstellung', {
      startseiteInhalt: inhalt.value
    })
    toast.add({ severity: 'success', summary: 'Gespeichert', life: 3000 })
  } catch {
    toast.add({
      severity: 'error',
      summary: 'Fehler',
      detail: 'Inhalt konnte nicht gespeichert werden.',
      life: 3000
    })
  } finally {
    isSaving.value = false
  }
}

const confirmReset = () => {
  confirm.require({
    message: 'Der Startseiten-Inhalt wird gelöscht und der Standardtext wieder angezeigt.',
    header: 'Auf Standard zurücksetzen',
    icon: 'pi pi-exclamation-triangle',
    rejectProps: { label: 'Abbrechen', severity: 'secondary', outlined: true },
    acceptProps: { label: 'Zurücksetzen', severity: 'danger' },
    accept: async () => {
      inhalt.value = ''
      await submit()
    }
  })
}
</script>
