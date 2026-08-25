<template>
  <div>
    <div class="flex items-center justify-between mb-3">
      <p class="text-sm text-gray-500">
        Beliebig viele Logos anzeigen. Ziehen Sie die Einträge, um die Reihenfolge zu ändern.
      </p>
      <Button label="Logo hinzufügen" icon="pi pi-plus" size="small" @click="pickerVisible = true" />
    </div>

    <BaseSpinner v-if="isLoading" />
    <div v-else-if="logos.length === 0" class="text-sm text-gray-400 text-center py-4">
      Noch keine Logos konfiguriert. Es werden die Standardgrafiken angezeigt.
    </div>
    <draggable
      v-else
      :list="logos"
      item-key="id"
      handle=".drag-handle"
      class="flex flex-col gap-2"
      @change="onReorder"
    >
      <template #item="{ element }">
        <div class="flex items-center gap-3 border border-gray-200 rounded-md p-3">
          <i class="pi pi-bars drag-handle cursor-move text-gray-400" />
          <img :src="element.asset.url" alt="Logo" class="h-10 max-w-24 object-contain bg-gray-50 rounded p-1" />
          <InputText
            v-if="verlinkbar"
            v-model="element.linkEdit"
            class="flex-1"
            placeholder="Link-Ziel (optional), https://…"
          />
          <div v-else class="flex-1" />
          <Button v-if="verlinkbar" label="Speichern" text size="small" @click="saveLink(element)" />
          <Button icon="pi pi-trash" severity="danger" text @click="remove(element)" />
        </div>
      </template>
    </draggable>

    <BrandingAssetPicker v-model:visible="pickerVisible" @select="add" />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import draggable from 'vuedraggable'
import Button from 'primevue/button'
import InputText from 'primevue/inputtext'
import { apiClient } from '@/services/axios'
import { useToast } from 'primevue/usetoast'
import BrandingAssetPicker from './BrandingAssetPicker.vue'

const props = defineProps({
  bereich: {
    type: String,
    required: true
  },
  verlinkbar: {
    type: Boolean,
    default: true
  }
})

const isLoading = ref(false)
const logos = ref([])
const pickerVisible = ref(false)
const toast = useToast()

const fetchLogos = async () => {
  isLoading.value = true
  try {
    const res = await apiClient.get(`/branding/logo-listen/${props.bereich}`)
    logos.value = res.data.map((l) => ({ ...l, linkEdit: l.link || '' }))
  } catch {
    logos.value = []
  } finally {
    isLoading.value = false
  }
}

onMounted(fetchLogos)

const add = async (asset) => {
  try {
    const res = await apiClient.post(`/branding/logo-listen/${props.bereich}`, { assetId: asset.id })
    logos.value.push({ ...res.data, linkEdit: res.data.link || '' })
    toast.add({ severity: 'success', summary: 'Logo hinzugefügt', life: 3000 })
    pickerVisible.value = false
  } catch {
    toast.add({
      severity: 'error',
      summary: 'Fehler',
      detail: 'Logo konnte nicht hinzugefügt werden.',
      life: 3000
    })
  }
}

const remove = async (logo) => {
  try {
    await apiClient.delete(`/branding/logo-listen/${props.bereich}/${logo.id}`)
    logos.value = logos.value.filter((l) => l.id !== logo.id)
    toast.add({ severity: 'success', summary: 'Logo entfernt', life: 3000 })
  } catch {
    toast.add({
      severity: 'error',
      summary: 'Fehler',
      detail: 'Logo konnte nicht entfernt werden.',
      life: 3000
    })
  }
}

const saveLink = async (logo) => {
  try {
    const res = await apiClient.patch(`/branding/logo-listen/${props.bereich}/${logo.id}`, {
      link: logo.linkEdit || null
    })
    logo.link = res.data.link
    logo.linkEdit = res.data.link || ''
    toast.add({ severity: 'success', summary: 'Link gespeichert', life: 3000 })
  } catch {
    toast.add({
      severity: 'error',
      summary: 'Fehler',
      detail: 'Link konnte nicht gespeichert werden.',
      life: 3000
    })
  }
}

const onReorder = async () => {
  try {
    const reihenfolge = logos.value.map((l, index) => ({ id: l.id, reihenfolge: index }))
    await apiClient.post(`/branding/logo-listen/${props.bereich}/reorder`, { reihenfolge })
  } catch {
    toast.add({
      severity: 'error',
      summary: 'Fehler',
      detail: 'Reihenfolge konnte nicht gespeichert werden.',
      life: 3000
    })
    await fetchLogos()
  }
}
</script>
