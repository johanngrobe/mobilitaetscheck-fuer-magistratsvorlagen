<template>
  <Button icon="pi pi-plus" v-tooltip.top="props.tooltip" size="small" :label="label" />
</template>

<script setup>
import { computed } from 'vue'
import Button from 'primevue/button'

const props = defineProps({
  tooltip: {
    type: String,
    default: 'Hinzufügen'
  },
  label: {
    type: Boolean,
    default: false
  }
})

const label = computed(() => {
  return props.label ? 'Hinzufügen' : ''
})
</script>

<style></style>
