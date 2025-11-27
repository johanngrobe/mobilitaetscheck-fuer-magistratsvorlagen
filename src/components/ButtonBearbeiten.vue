<template>
  <Button
    icon="pi pi-pen-to-square"
    v-tooltip.top="'bearbeiten'"
    :label="label"
    size="small"
    :disabled="props.disabled"
  />
</template>

<script setup>
import { computed } from 'vue'
import Button from 'primevue/button'

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
  return props.noLabel ? '' : 'bearbeiten'
})
</script>

<style></style>
