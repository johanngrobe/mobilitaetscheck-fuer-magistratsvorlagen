<template>
  <component
    :is="href ? 'a' : 'span'"
    :href="href || undefined"
    :target="href ? '_blank' : undefined"
    :rel="href ? 'noopener noreferrer' : undefined"
  >
    <slot />
  </component>
</template>

<script setup>
defineProps({
  href: {
    type: String,
    default: null
  }
})
</script>
