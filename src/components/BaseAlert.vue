<template>
  <div :class="alertClass" rolle="alert">
    <svg
      :class="iconClass"
      aria-hidden="true"
      xmlns="http://www.w3.org/2000/svg"
      fill="currentColor"
      viewBox="0 0 20 20"
    >
      <path
        d="M10 .5a9.5 9.5 0 1 0 9.5 9.5A9.51 9.51 0 0 0 10 .5ZM9.5 4a1.5 1.5 0 1 1 0 3 1.5 1.5 0 0 1 0-3ZM12 15H8a1 1 0 0 1 0-2h1v-3H8a1 1 0 0 1 0-2h2a1 1 0 0 1 1 1v4h1a1 1 0 0 1 0 2Z"
      />
    </svg>
    <span class="sr-only">{{ title }}</span>
    <div>
      <span class="font-medium">{{ title }}</span> {{ message }}
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

// Define the props for the component
const props = defineProps({
  type: {
    type: String,
    default: 'info', // default type
    validator: (value) => ['info', 'danger', 'success', 'warning', 'dark'].includes(value)
  },
  title: {
    type: String,
    default: 'Info alert!'
  },
  message: {
    type: String,
    required: true
  }
})

const alertClass = computed(() => {
  return `alert alert-${props.type} flex items-center`
})

const iconClass = computed(() => {
  return `flex-shrink-0 inline w-4 h-4 me-3`
})
</script>

<style scoped>
.alert {
  @apply p-4 mb-4 text-sm rounded-lg;
}

.alert-info {
  @apply text-blue-800 bg-blue-50 dark:bg-gray-800 dark:text-blue-400;
}

.alert-danger {
  @apply text-red-800 bg-red-50 dark:bg-gray-800 dark:text-red-400;
}

.alert-success {
  @apply text-green-800 bg-green-50 dark:bg-gray-800 dark:text-green-400;
}

.alert-warning {
  @apply text-yellow-800 bg-yellow-50 dark:bg-gray-800 dark:text-yellow-300;
}

.alert-dark {
  @apply text-gray-800 bg-gray-50 dark:bg-gray-800 dark:text-gray-300;
}
</style>
