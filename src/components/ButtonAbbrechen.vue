<template>
  <BaseButton v-tooltip.top="'Abbrechen'" class="flex gap-2 px-2 py-1" color="red"
    ><IconCancel class="h-4 w-4" />
    <span v-if="props.showLabel">{{ props.label }}</span>
  </BaseButton>
</template>

<script setup>
import IconCancel from '@/assets/icons/MaterialSymbolsCancel.svg?component'

const props = defineProps({
  showLabel: {
    type: Boolean,
    default: false
  },
  label: {
    type: String,
    default: 'Abbrechen'
  }
})
</script>

<style></style>
