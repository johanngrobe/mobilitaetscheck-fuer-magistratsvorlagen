<template>
  <div class="relative flex items-center">
    <!-- Icon -->
    <div class="cursor-pointer" @mouseenter="showInfo" @mouseleave="hideInfo">
      <img :src="getIconPath(props.icon)" class="w-5" />
    </div>

    <!-- Hover Information -->
    <div
      v-if="isHovered"
      class="absolute left-6 top-0 px-2 py-0.5 bg-gray-800 opacity-90 text-white rounded-md shadow-lg z-10 transition-opacity min-w-max"
    >
      <div class="font-bold text-sm">
        <slot name="title"></slot>
      </div>
      <div class="text-sm">
        <slot></slot>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

// Define props
const props = defineProps({
  icon: {
    type: String, // Icon name passed as a prop
    required: true
  }
})

const isHovered = ref(false)

const showInfo = () => {
  isHovered.value = true
}

const hideInfo = () => {
  isHovered.value = false
}

const getIconPath = (icon) => {
  return new URL(`/src/assets/icons/${icon}`, import.meta.url).href
}
</script>

<style scoped>
/* Additional styling if necessary */
</style>
