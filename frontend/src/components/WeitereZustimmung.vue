<template>
  <div class="field">
    <div class="flex items-start gap-2">
      <Checkbox
        id="weitereZustimmungAkzeptiert"
        v-model="checked"
        :binary="true"
        :invalid="!!errorMessage"
      />
      <!-- TODO: Platzhaltertext, finaler Zustimmungstext folgt noch -->
      <label for="weitereZustimmungAkzeptiert" class="text-sm">
        Ich stimme [Platzhaltertext] zu.
      </label>
    </div>
    <small v-if="errorMessage" class="p-error block">{{ errorMessage }}</small>
  </div>
</template>

<script setup>
import Checkbox from 'primevue/checkbox'

defineProps({
  errorMessage: {
    type: String,
    default: ''
  }
})

const checked = defineModel({ type: Boolean, default: false })
</script>

<style scoped>
.p-error {
  @apply text-red-600;
}
</style>
