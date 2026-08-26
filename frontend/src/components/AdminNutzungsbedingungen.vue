<template>
  <BaseCard>
    <div class="flex items-center justify-between mb-4">
      <h5 class="text-lg font-semibold">Nutzungsbedingungen</h5>
    </div>
    <p class="text-sm text-gray-500 mb-4">
      Diese Nutzungsbedingungen werden im Footer verlinkt und Nutzer:innen bei der Registrierung
      angezeigt. Sie müssen ihnen zustimmen, um ein Konto anlegen zu können.
    </p>

    <BaseSpinner v-if="isLoading" />
    <template v-else>
      <SelectButton
        v-model="modus"
        :options="modusOptionen"
        optionLabel="label"
        optionValue="value"
        class="mb-4"
      />

      <template v-if="modus === 'inhalt'">
        <RichContentEditor v-model="inhalt" />
      </template>
      <template v-else>
        <div class="field">
          <FloatLabel variant="on">
            <InputText id="nutzungsbedingungen-url" v-model="url" class="w-full" placeholder="https://…" />
            <label for="nutzungsbedingungen-url">URL der Nutzungsbedingungen</label>
          </FloatLabel>
          <small class="text-gray-500 block mt-1">
            Nutzer:innen werden bei der Registrierung zu dieser URL verlinkt, um die
            Nutzungsbedingungen zu lesen und müssen die Zustimmung dennoch aktiv bestätigen.
          </small>
        </div>
      </template>

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
import InputText from 'primevue/inputtext'
import FloatLabel from 'primevue/floatlabel'
import SelectButton from 'primevue/selectbutton'
import { apiClient } from '@/services/axios'
import { useToast } from 'primevue/usetoast'
import { useConfirm } from 'primevue/useconfirm'
import RichContentEditor from './RichContentEditor.vue'

const modusOptionen = [
  { label: 'HTML-Inhalt', value: 'inhalt' },
  { label: 'Externe URL', value: 'url' }
]

const isLoading = ref(false)
const isSaving = ref(false)
const modus = ref('inhalt')
const inhalt = ref('')
const url = ref('')

const toast = useToast()
const confirm = useConfirm()

const fetchEinstellung = async () => {
  isLoading.value = true
  try {
    const res = await apiClient.get('/admin/einstellung')
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
}

onMounted(fetchEinstellung)

const submit = async () => {
  isSaving.value = true
  try {
    await apiClient.patch('/admin/einstellung', {
      nutzungsbedingungenModus: modus.value,
      nutzungsbedingungenInhalt: inhalt.value,
      nutzungsbedingungenUrl: url.value
    })
    toast.add({ severity: 'success', summary: 'Gespeichert', life: 3000 })
  } catch {
    toast.add({
      severity: 'error',
      summary: 'Fehler',
      detail: 'Nutzungsbedingungen konnten nicht gespeichert werden.',
      life: 3000
    })
  } finally {
    isSaving.value = false
  }
}

const confirmReset = () => {
  confirm.require({
    message:
      'Die Nutzungsbedingungen werden gelöscht, ein hinterlegter externer Link entfernt und der Modus auf "HTML-Inhalt" zurückgesetzt.',
    header: 'Auf Standard zurücksetzen',
    icon: 'pi pi-exclamation-triangle',
    rejectProps: { label: 'Abbrechen', severity: 'secondary', outlined: true },
    acceptProps: { label: 'Zurücksetzen', severity: 'danger' },
    accept: async () => {
      modus.value = 'inhalt'
      inhalt.value = ''
      url.value = ''
      await submit()
    }
  })
}
</script>
