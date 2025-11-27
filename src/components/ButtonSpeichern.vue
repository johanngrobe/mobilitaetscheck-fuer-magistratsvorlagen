<template>
  <Button icon="pi pi-save" v-tooltip.top="'speichern'" :label="label" />
</template>

<script setup>
import { computed } from 'vue'
import Button from 'primevue/button'

const props = defineProps({
  noLabel: {
    type: Boolean,
    default: false
  }
})

const label = computed(() => {
  return props.noLabel ? '' : 'speichern'
})
</script>

<style></style>
