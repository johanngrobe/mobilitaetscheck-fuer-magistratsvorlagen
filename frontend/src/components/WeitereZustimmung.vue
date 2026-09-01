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
        Mit meiner Registrierung bestätige ich meine Kenntnis darüber, dass auf der Plattform verschiedene politische Gruppen vertreten sind und es zum Austausch politischer Meinungen kommen kann. Die politische Meinung ist ein personenbezogenes Datum besonderer Kategorien. Hiermit willige ich ein, dass Daten von mir in diesem Zusammenhang von dem Betreiber dieser Plattform zum Zwecke der Plattform verarbeitet werden. Mir ist bekannt, dass ich meine Einwilligung jederzeit ohne Angabe von Gründen mit Wirkung für die Zukunft widerrufen kann, etwa per E-Mail an <a class="text-blue-600 hover:underline" href="mailto:widerruf@mobichecks-hessen.de">widerruf@mobichecks-hessen.de</a>. Weitere Informationen finden sich in den Datenschutzhinweisen.
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
