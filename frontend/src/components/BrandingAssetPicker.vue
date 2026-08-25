<template>
  <Dialog :visible="visible" @update:visible="(v) => emit('update:visible', v)" header="Bild auswählen" modal class="w-full max-w-2xl">
    <div class="flex flex-col gap-4">
      <FileUpload
        mode="basic"
        chooseLabel="Neues Bild hochladen"
        :auto="true"
        customUpload
        accept="image/*"
        :chooseButtonProps="{ class: 'w-full' }"
        @uploader="(e) => uploadAndSelect(e.files[0])"
      />

      <BaseSpinner v-if="isLoading" />
      <div v-else-if="assets.length === 0" class="text-sm text-gray-400 text-center py-4">
        Noch keine Bilder hochgeladen.
      </div>
      <div v-else class="grid grid-cols-3 sm:grid-cols-4 gap-3">
        <div
          v-for="asset in assets"
          :key="asset.id"
          class="relative border border-gray-200 rounded-md p-2 flex flex-col items-center gap-2 cursor-pointer hover:border-blue-400"
          @click="emit('select', asset)"
        >
          <img :src="asset.url" :alt="asset.originalDateiname" class="h-16 max-w-full object-contain" />
          <span class="text-[10px] text-gray-500 truncate w-full text-center">{{
            asset.originalDateiname
          }}</span>
          <Button
            v-if="!asset.inVerwendung"
            icon="pi pi-trash"
            severity="danger"
            text
            size="small"
            class="!absolute top-0 right-0"
            @click.stop="deleteAsset(asset)"
          />
        </div>
      </div>
    </div>
  </Dialog>
</template>

<script setup>
import { ref, watch } from 'vue'
import Button from 'primevue/button'
import Dialog from 'primevue/dialog'
import FileUpload from 'primevue/fileupload'
import { apiClient } from '@/services/axios'
import { useToast } from 'primevue/usetoast'

const props = defineProps({
  visible: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['update:visible', 'select'])

const isLoading = ref(false)
const assets = ref([])
const toast = useToast()

const fetchAssets = async () => {
  isLoading.value = true
  try {
    const res = await apiClient.get('/branding/assets')
    assets.value = res.data
  } catch {
    assets.value = []
  } finally {
    isLoading.value = false
  }
}

watch(
  () => props.visible,
  (visible) => {
    if (visible) fetchAssets()
  }
)

const uploadAndSelect = async (file) => {
  if (!file) return
  const formData = new FormData()
  formData.append('file', file)
  try {
    const res = await apiClient.post('/branding/assets', formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    })
    emit('select', res.data)
    await fetchAssets()
  } catch {
    toast.add({
      severity: 'error',
      summary: 'Fehler',
      detail: 'Bild konnte nicht hochgeladen werden.',
      life: 3000
    })
  }
}

const deleteAsset = async (asset) => {
  try {
    await apiClient.delete(`/branding/assets/${asset.id}`)
    toast.add({ severity: 'success', summary: 'Bild gelöscht', life: 3000 })
    await fetchAssets()
  } catch {
    toast.add({
      severity: 'error',
      summary: 'Fehler',
      detail: 'Bild konnte nicht gelöscht werden (wird evtl. noch verwendet).',
      life: 3000
    })
  }
}
</script>
