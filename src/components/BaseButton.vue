<template>
  <component
    :is="tag"
    :to="isRouterLink ? to : undefined"
    :href="isLinkTag ? to : undefined"
    @click="handleClick"
    class="btn"
    :class="computedClass"
    :type="type"
  >
    <slot></slot>
  </component>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  tag: {
    type: String,
    default: 'button',
    validator: (value) => ['button', 'a', 'RouterLink'].includes(value)
  },
  to: {
    type: [String, Object],
    default: null
  },
  outline: {
    type: Boolean,
    default: false
  },
  type: {
    type: String,
    default: 'button'
  },
  color: {
    type: String,
    default: 'blue' // default color
  }
})

const emit = defineEmits(['click'])

// Determines if the component is a RouterLink or anchor tag
const isRouterLink = computed(() => props.tag === 'RouterLink')
const isLinkTag = computed(() => props.tag === 'a')

// Map for the outlined button styles
const outlineStyles = {
  blue: 'text-blue-700 border border-blue-700 hover:bg-blue-800 hover:text-white focus:ring-blue-300 dark:border-blue-500 dark:text-blue-500 dark:hover:bg-blue-500 dark:hover:text-white dark:focus:ring-blue-800',
  gray: 'text-gray-900 border border-gray-300 hover:bg-gray-100 hover:text-blue-700 focus:ring-gray-100 dark:focus:ring-gray-700 dark:bg-gray-800 dark:text-gray-400 dark:border-gray-600 dark:hover:bg-gray-700 dark:hover:text-white',
  green:
    'text-green-700 border border-green-700 hover:bg-green-800 hover:text-white focus:ring-green-300 dark:border-green-600 dark:text-green-600 dark:hover:bg-green-600 dark:hover:text-white dark:focus:ring-green-800',
  red: 'text-red-700 border border-red-700 hover:bg-red-800 hover:text-white focus:ring-red-300 dark:border-red-600 dark:text-red-600 dark:hover:bg-red-600 dark:hover:text-white dark:focus:ring-red-900',
  yellow:
    'text-yellow-400 border border-yellow-400 hover:bg-yellow-500 hover:text-white focus:ring-yellow-300 dark:border-yellow-600 dark:text-yellow-600 dark:hover:bg-yellow-600 dark:hover:text-white dark:focus:ring-yellow-900',
  purple:
    'text-purple-700 border border-purple-700 hover:bg-purple-800 hover:text-white focus:ring-purple-300 dark:border-purple-600 dark:text-purple-600 dark:hover:bg-purple-600 dark:hover:text-white dark:focus:ring-purple-900'
}

// Map for the solid button styles
const solidStyles = {
  blue: 'text-white bg-blue-700 hover:bg-blue-800 focus:ring-blue-300 dark:bg-blue-600 dark:hover:bg-blue-700 dark:focus:ring-blue-800',
  gray: 'text-white bg-gray-800 hover:bg-gray-900 focus:ring-gray-300 dark:bg-gray-800 dark:hover:bg-gray-700 dark:focus:ring-gray-700',
  green:
    'text-white bg-green-700 hover:bg-green-800 focus:ring-green-300 dark:bg-green-600 dark:hover:bg-green-700 dark:focus:ring-green-800',
  red: 'text-white bg-red-700 hover:bg-red-800 focus:ring-red-300 dark:bg-red-600 dark:hover:bg-red-700 dark:focus:ring-red-900',
  yellow:
    'text-white bg-yellow-400 hover:bg-yellow-500 focus:ring-yellow-300 dark:focus:ring-yellow-900',
  purple:
    'text-white bg-purple-700 hover:bg-purple-800 focus:ring-purple-300 dark:bg-purple-600 dark:hover:bg-purple-700 dark:focus:ring-purple-900'
}

// Compute the appropriate class based on the button's type (outline or solid)
const computedClass = computed(() => {
  return props.outline ? outlineStyles[props.color] : solidStyles[props.color]
})

// Handle click event and emit it
const handleClick = (event) => {
  emit('click', event)
}
</script>

<style scoped>
/* Base button class */
.btn {
  @apply inline-flex items-center justify-center cursor-pointer font-medium rounded-lg text-sm px-2 py-1 focus:outline-none;
}
</style>
