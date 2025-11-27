<template>
  <BaseButton class="flex gap-2 px-2 py-1" :outline="true">
    <IconRefresh class="h-4 w-4" />
    <slot></slot>
  </BaseButton>
</template>

<script setup>
import IconRefresh from '@/assets/icons/MaterialSymbolsRefresh.svg?component'
</script>

<style></style>
