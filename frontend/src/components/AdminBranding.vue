<template>
  <BaseCard>
    <div class="flex items-center justify-between mb-4">
      <h5 class="text-lg font-semibold">Branding</h5>
      <Button
        label="Branding zurücksetzen"
        icon="pi pi-refresh"
        text
        severity="secondary"
        @click="confirmResetAll"
      />
    </div>
    <p class="text-sm text-gray-500 mb-4">
      Passen Sie Favicon und Logos der Anwendung an. Nicht gesetzte Bilder verwenden weiterhin die
      Standardgrafiken.
    </p>

    <BaseSpinner v-if="isLoading" />
    <template v-else>
      <template v-for="(bereich, index) in bereiche" :key="bereich">
        <Divider v-if="index > 0" />
        <h6 class="text-sm font-semibold text-gray-600 mb-3">{{ bereich }}</h6>

        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4 mb-2">
          <div
            v-for="slot in slotsByBereich[bereich]"
            :key="slot.slot"
            class="border border-gray-200 rounded-md p-4 flex flex-col items-center gap-3"
          >
            <div class="text-sm font-medium text-center">{{ slot.label }}</div>
            <div class="text-xs text-gray-500 text-center">{{ slot.beschreibung }}</div>

            <div
              class="w-full h-24 flex items-center justify-center bg-gray-50 rounded border border-dashed border-gray-300"
            >
              <img
                v-if="slot.asset"
                :src="slot.asset.url"
                :alt="slot.label"
                class="max-h-20 max-w-full object-contain"
              />
              <span v-else class="text-xs text-gray-400">Standardbild aktiv</span>
            </div>

            <div class="flex gap-2 w-full">
              <Button
                label="Bild auswählen"
                icon="pi pi-images"
                text
                class="flex-1"
                @click="openPicker(slot)"
              />
              <Button
                v-if="slot.asset"
                icon="pi pi-trash"
                severity="danger"
                text
                @click="unassign(slot)"
              />
            </div>

            <div v-if="slot.verlinkbar" class="field w-full">
              <FloatLabel variant="on">
                <InputText
                  :id="`link-${slot.slot}`"
                  v-model="slot.linkEdit"
                  class="w-full"
                  placeholder="https://…"
                />
                <label :for="`link-${slot.slot}`">Link-Ziel</label>
              </FloatLabel>
              <Button
                label="Link speichern"
                text
                size="small"
                class="mt-1 w-full"
                @click="saveLink(slot)"
              />
            </div>
          </div>
        </div>
      </template>

      <Divider />
      <h6 class="text-sm font-semibold text-gray-600 mb-3">Anmelde- und Registrierungsseite</h6>
      <AdminLogoListe :key="`login-${resetCounter}`" bereich="login" :verlinkbar="false" />

      <Divider />
      <h6 class="text-sm font-semibold text-gray-600 mb-3">Footer</h6>
      <AdminLogoListe :key="`footer-${resetCounter}`" bereich="footer" />
    </template>

    <BrandingAssetPicker v-model:visible="pickerVisible" @select="assign" />
  </BaseCard>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import Button from 'primevue/button'
import Divider from 'primevue/divider'
import InputText from 'primevue/inputtext'
import FloatLabel from 'primevue/floatlabel'
import { apiClient } from '@/services/axios'
import { useToast } from 'primevue/usetoast'
import { useConfirm } from 'primevue/useconfirm'
import { useBrandingStore } from '@/stores/branding'
import BrandingAssetPicker from './BrandingAssetPicker.vue'
import AdminLogoListe from './AdminLogoListe.vue'

const isLoading = ref(false)
const slotList = ref([])
const pickerVisible = ref(false)
const activeSlot = ref(null)
const resetCounter = ref(0)
const toast = useToast()
const confirm = useConfirm()
const brandingStore = useBrandingStore()

const bereiche = computed(() => [...new Set(slotList.value.map((s) => s.bereich))])
const slotsByBereich = computed(() =>
  Object.fromEntries(bereiche.value.map((b) => [b, slotList.value.filter((s) => s.bereich === b)]))
)

const fetchSlots = async () => {
  isLoading.value = true
  try {
    const res = await apiClient.get('/branding')
    slotList.value = res.data.map((s) => ({ ...s, linkEdit: s.link || '' }))
  } catch {
    slotList.value = []
  } finally {
    isLoading.value = false
  }
}

onMounted(fetchSlots)

const openPicker = (slot) => {
  activeSlot.value = slot
  pickerVisible.value = true
}

const applySlotUpdate = (updated) => {
  const idx = slotList.value.findIndex((s) => s.slot === updated.slot)
  if (idx !== -1) slotList.value[idx] = { ...updated, linkEdit: updated.link || '' }
}

const assign = async (asset) => {
  if (!activeSlot.value) return
  try {
    const res = await apiClient.patch(`/branding/${activeSlot.value.slot}/assign`, {
      assetId: asset.id
    })
    applySlotUpdate(res.data)
    toast.add({ severity: 'success', summary: 'Bild zugewiesen', life: 3000 })
    await brandingStore.fetchBranding()
    pickerVisible.value = false
  } catch {
    toast.add({
      severity: 'error',
      summary: 'Fehler',
      detail: 'Bild konnte nicht zugewiesen werden.',
      life: 3000
    })
  }
}

const unassign = async (slot) => {
  try {
    const res = await apiClient.patch(`/branding/${slot.slot}/assign`, { assetId: null })
    applySlotUpdate(res.data)
    toast.add({ severity: 'success', summary: 'Bild entfernt', life: 3000 })
    await brandingStore.fetchBranding()
  } catch {
    toast.add({
      severity: 'error',
      summary: 'Fehler',
      detail: 'Bild konnte nicht entfernt werden.',
      life: 3000
    })
  }
}

const saveLink = async (slot) => {
  try {
    const res = await apiClient.patch(`/branding/${slot.slot}/link`, {
      link: slot.linkEdit || null
    })
    applySlotUpdate(res.data)
    toast.add({ severity: 'success', summary: 'Link gespeichert', life: 3000 })
    await brandingStore.fetchBranding()
  } catch {
    toast.add({
      severity: 'error',
      summary: 'Fehler',
      detail: 'Link konnte nicht gespeichert werden.',
      life: 3000
    })
  }
}

const confirmResetAll = () => {
  confirm.require({
    message:
      'Favicon, Menüleisten-Logo sowie alle Login- und Footer-Logos werden entfernt und die Standardgrafiken wieder angezeigt. Bereits hochgeladene Bilder bleiben in der Bildbibliothek erhalten.',
    header: 'Branding zurücksetzen',
    icon: 'pi pi-exclamation-triangle',
    rejectProps: { label: 'Abbrechen', severity: 'secondary', outlined: true },
    acceptProps: { label: 'Zurücksetzen', severity: 'danger' },
    accept: async () => {
      try {
        await apiClient.post('/branding/reset')
        toast.add({ severity: 'success', summary: 'Branding zurückgesetzt', life: 3000 })
        await fetchSlots()
        resetCounter.value++
        await brandingStore.fetchBranding()
      } catch {
        toast.add({
          severity: 'error',
          summary: 'Fehler',
          detail: 'Branding konnte nicht zurückgesetzt werden.',
          life: 3000
        })
      }
    }
  })
}
</script>
