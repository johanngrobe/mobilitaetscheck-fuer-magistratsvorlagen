<template>
  <div class="field">
    <div class="flex items-start gap-2">
      <Checkbox
        id="nutzungsbedingungenAkzeptiert"
        v-model="checked"
        :binary="true"
        :invalid="!!errorMessage"
      />
      <label for="nutzungsbedingungenAkzeptiert" class="text-sm">
        Ich habe die
        <RouterLink
          :to="{ name: 'nutzungsbedingungen' }"
          target="_blank"
          class="text-blue-600 hover:underline"
          >Nutzungsbedingungen</RouterLink
        >
        gelesen und stimme zu.
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
