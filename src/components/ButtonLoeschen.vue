<template>
  <BaseModal v-model="isModalOpen">
    <template #header>
      <BaseSubheading>Möchtest du den Eintrag wirklich löschen?</BaseSubheading>
    </template>
    <slot></slot>
    <template #footer>
      <div class="flex items-center justify-end gap-4 w-full">
        <Button
          icon="pi pi-trash"
          class="p-button-danger"
          @click="handleDelete"
          label="löschen"
          size="small"
          severity="danger"
        />
        <Button
          icon="pi pi-times"
          class="p-button-secondary"
          @click="toggleModal"
          label="Abbrechen"
          size="small"
          severity="secondary"
        />
      </div>
    </template>
  </BaseModal>
  <Button
    icon="pi pi-trash"
    @click="toggleModal"
    size="small"
    severity="danger"
    :label="label"
    :disabled="props.disabled"
  />
</template>

<script setup>
import { computed, ref } from 'vue'
import Button from 'primevue/button'
import BaseModal from './BaseModal.vue'

const props = defineProps({
  noLabel: {
    type: Boolean,
    default: false
  },
  disabled: {
    type: Boolean,
    default: false
  }
})

const label = computed(() => {
  return props.noLabel ? '' : 'löschen'
})

const isModalOpen = ref(false)

const toggleModal = () => {
  isModalOpen.value = !isModalOpen.value
}

const emit = defineEmits(['delete-confirmed'])

const handleDelete = () => {
  emit('delete-confirmed')
  toggleModal()
}
</script>
