<template>
  <span
    class="flex item-center justify-center px-2 py-1 rounded-2xl"
    :class="bgColorPresets[props.color]"
  >
    <slot></slot>
  </span>
</template>

<script setup>
const props = defineProps({
  color: {
    type: String,
    default: 'blue'
  }
})

const bgColorPresets = {
  gray: 'bg-gray-400',
  red: 'bg-red-600 text-white',
  yellow: 'bg-yellow-200',
  green: 'bg-green-200',
  blue: 'bg-blue-600 text-white',
  indigo: 'bg-indigo-200',
  purple: 'bg-purple-200 text-white',
  pink: 'bg-pink-200'
}
</script>

<style scoped></style>
