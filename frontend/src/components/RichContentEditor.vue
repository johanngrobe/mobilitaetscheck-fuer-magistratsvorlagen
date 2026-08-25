<template>
  <Editor
    :modelValue="modelValue"
    @update:modelValue="(v) => emit('update:modelValue', v)"
    :editorStyle="editorStyle"
    @load="onLoad"
  />
</template>

<script setup>
import Editor from 'primevue/editor'
import { apiClient } from '@/services/axios'
import { useToast } from 'primevue/usetoast'

defineProps({
  modelValue: {
    type: String,
    default: ''
  },
  editorStyle: {
    type: String,
    default: 'min-height: 320px'
  }
})

const emit = defineEmits(['update:modelValue'])

const toast = useToast()

const onLoad = (event) => {
  const quill = event.instance
  quill.getModule('toolbar').addHandler('image', () => selectAndUploadImage(quill))
}

const selectAndUploadImage = (quill) => {
  const input = document.createElement('input')
  input.setAttribute('type', 'file')
  input.setAttribute('accept', 'image/*')
  input.onchange = async () => {
    const file = input.files?.[0]
    if (!file) return

    const formData = new FormData()
    formData.append('file', file)

    try {
      const res = await apiClient.post('/branding/assets', formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      })
      const range = quill.getSelection(true)
      quill.insertEmbed(range.index, 'image', res.data.url, 'user')
      quill.setSelection(range.index + 1)
    } catch {
      toast.add({
        severity: 'error',
        summary: 'Fehler',
        detail: 'Bild konnte nicht hochgeladen werden.',
        life: 3000
      })
    }
  }
  input.click()
}
</script>
