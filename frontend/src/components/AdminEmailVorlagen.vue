<template>
  <BaseCard>
    <div class="flex items-center justify-between mb-4">
      <h5 class="text-lg font-semibold">E-Mail-Vorlagen</h5>
    </div>
    <p class="text-sm text-gray-500 mb-4">
      Passen Sie Betreff und Inhalt der automatisch versendeten E-Mails an. Platzhalter in
      geschweiften Klammern (siehe Liste je Vorlage) werden beim Versand durch die tatsächlichen
      Werte ersetzt und müssen erhalten bleiben.
    </p>

    <BaseSpinner v-if="isLoading" />
    <Accordion v-else v-model:value="activeKey">
      <AccordionPanel v-for="vorlage in vorlagen" :key="vorlage.key" :value="vorlage.key">
        <AccordionHeader>{{ labels[vorlage.key] || vorlage.key }}</AccordionHeader>
        <AccordionContent>
          <div class="field mb-4">
            <FloatLabel variant="on">
              <InputText
                :id="`betreff-${vorlage.key}`"
                v-model="vorlage.betreffEdit"
                class="w-full"
              />
              <label :for="`betreff-${vorlage.key}`">Betreff</label>
            </FloatLabel>
          </div>

          <p class="text-xs text-gray-500 mb-2">
            Verfügbare Platzhalter:
            <code v-for="p in vorlage.platzhalter" :key="p" class="mr-2">{{ placeholderLabel(p) }}</code>
          </p>

          <RichContentEditor v-model="vorlage.inhaltEdit" editorStyle="min-height: 280px" />

          <div class="flex justify-end gap-2 mt-4">
            <Button
              label="Auf Standard zurücksetzen"
              text
              severity="secondary"
              :loading="vorlage.isResetting"
              @click="confirmReset(vorlage)"
            />
            <Button label="Speichern" @click="submitVorlage(vorlage)" :loading="vorlage.isSaving" />
          </div>
        </AccordionContent>
      </AccordionPanel>
    </Accordion>
  </BaseCard>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import RichContentEditor from '@/components/RichContentEditor.vue'
import Button from 'primevue/button'
import InputText from 'primevue/inputtext'
import FloatLabel from 'primevue/floatlabel'
import Accordion from 'primevue/accordion'
import AccordionPanel from 'primevue/accordionpanel'
import AccordionHeader from 'primevue/accordionheader'
import AccordionContent from 'primevue/accordioncontent'
import { apiClient } from '@/services/axios'
import { useToast } from 'primevue/usetoast'
import { useConfirm } from 'primevue/useconfirm'

const labels = {
  'account-bestaetigen': 'Account bestätigen',
  einladung: 'Einladung zur Registrierung',
  'passwort-zuruecksetzen': 'Passwort zurücksetzen'
}

const isLoading = ref(false)
const vorlagen = ref([])
const activeKey = ref(null)
const toast = useToast()
const confirm = useConfirm()

const fetchVorlagen = async () => {
  isLoading.value = true
  try {
    const res = await apiClient.get('/admin/email-vorlage')
    vorlagen.value = res.data.map((v) => ({
      ...v,
      betreffEdit: v.betreff || v.standardBetreff,
      inhaltEdit: v.inhalt || v.standardInhalt,
      isSaving: false,
      isResetting: false
    }))
    activeKey.value = vorlagen.value[0]?.key ?? null
  } catch {
    vorlagen.value = []
  } finally {
    isLoading.value = false
  }
}

onMounted(fetchVorlagen)

const submitVorlage = async (vorlage) => {
  vorlage.isSaving = true
  try {
    const res = await apiClient.patch(`/admin/email-vorlage/${vorlage.key}`, {
      betreff: vorlage.betreffEdit,
      inhalt: vorlage.inhaltEdit
    })
    vorlage.betreff = res.data.betreff
    vorlage.inhalt = res.data.inhalt
    toast.add({ severity: 'success', summary: 'Gespeichert', life: 3000 })
  } catch {
    toast.add({
      severity: 'error',
      summary: 'Fehler',
      detail: 'Vorlage konnte nicht gespeichert werden.',
      life: 3000
    })
  } finally {
    vorlage.isSaving = false
  }
}

const confirmReset = (vorlage) => {
  confirm.require({
    message: `Die Vorlage "${labels[vorlage.key] || vorlage.key}" wird auf den Standard-Betreff und -Inhalt zurückgesetzt.`,
    header: 'Auf Standard zurücksetzen',
    icon: 'pi pi-exclamation-triangle',
    rejectProps: { label: 'Abbrechen', severity: 'secondary', outlined: true },
    acceptProps: { label: 'Zurücksetzen', severity: 'danger' },
    accept: async () => {
      vorlage.isResetting = true
      try {
        const res = await apiClient.post(`/admin/email-vorlage/${vorlage.key}/reset`)
        vorlage.betreff = res.data.betreff
        vorlage.inhalt = res.data.inhalt
        vorlage.betreffEdit = res.data.betreff || res.data.standardBetreff
        vorlage.inhaltEdit = res.data.inhalt || res.data.standardInhalt
        toast.add({ severity: 'success', summary: 'Zurückgesetzt', life: 3000 })
      } catch {
        toast.add({
          severity: 'error',
          summary: 'Fehler',
          detail: 'Vorlage konnte nicht zurückgesetzt werden.',
          life: 3000
        })
      } finally {
        vorlage.isResetting = false
      }
    }
  })
}

const placeholderLabel = (name) => `{{ ${name} }}`
</script>

<style scoped>
code {
  @apply bg-gray-100 rounded px-1 py-0.5 text-xs;
}
</style>
