<template>
  <div class="my-5">
    <!-- <FloatLabel variant="on">
      <InputText id="searchQuery" v-model="searchQuery" class="w-full" />
      <label for="searchQuery">Nach Klimacheck suchen</label>
    </FloatLabel> -->
    <!-- Display list of submissions -->
    <BaseSpinner v-if="isLoading" class="m-10" />
    <div v-else-if="eingaben.length === 0">
      <p class="font-lg font-bold m-5">Keine Klimachecks gefunden.</p>
    </div>
    <div v-else>
      <div v-for="eingabe in filteredEingaben" :key="eingabe.id">
        <KlimacheckListeItem
          :item="eingabe"
          @update-item="onUpdate"
          @publish-item="onPublish"
          @copy-item="onCopy"
          @delete-item="onDelete"
          @export-item="onExport"
          @reload-item="refetchEingabe"
        />
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { copyItem, deleteItem, exportItem, fetchItems, updateItem } from '@/composables/crud'
import KlimacheckListeItem from '@/components/KlimacheckListeItem.vue'
import InputText from 'primevue/inputtext'
import FloatLabel from 'primevue/floatlabel'
import BaseSpinner from '@/components/BaseSpinner.vue'

const eingaben = ref([])
const isLoading = ref(false)
const searchQuery = ref('')
const route = useRoute()

onMounted(async () => {
  await fetchEingaben()
})

const fetchEingaben = async () => {
  isLoading.value = true
  eingaben.value = await fetchItems(`klimacheck/eingabe/magistratsvorlage/${route.params.id}`)
  isLoading.value = false
}

const refetchEingabe = async (id) => {
  const index = eingaben.value.findIndex((eingabe) => eingabe.id === id)
  if (index !== -1) {
    eingaben.value[index] = await fetchItems(`klimacheck/eingabe/${id}`)
  }
}

// Computed property to filter submissions by multiple fields
const filteredEingaben = computed(() => {
  return eingaben.value.filter((eingabe) => {
    const query = searchQuery.value.toLowerCase()
    isLoading.value = true
    let results =
      (typeof eingabe.name === 'string' && eingabe.name.toLowerCase().includes(query)) ||
      (typeof eingabe.autor === 'string' && eingabe.autor.toLowerCase().includes(query)) ||
      (typeof eingabe.erstelltAm === 'string' && eingabe.erstelltAm.includes(query)) // Date format remains the same, no need to lowercase
    isLoading.value = false
    return results
  })
})

const onUpdate = async ({ modelId, values }) => {
  const response = await updateItem({
    model: 'klimacheck/eingabe',
    modelId,
    values,
    detail: {
      success: 'Klimacheck erfolgreich aktualisiert',
      error: 'Fehler beim Aktualisieren des Klimachecks'
    }
  })
  const index = eingaben.value.findIndex((eingabe) => eingabe.id === modelId)
  eingaben.value[index] = response
}

const onPublish = async ({ modelId, values }) => {
  const response = await updateItem({
    model: 'klimacheck/eingabe',
    modelId,
    values,
    detail: {
      success: values.veroeffentlicht
        ? 'Klimacheck veröffentlicht'
        : 'Veröffentlichung zurückgezogen',
      error: 'Fehler beim Veröffentlichen des Klimachecks'
    }
  })
  const index = eingaben.value.findIndex((eingabe) => eingabe.id === modelId)
  eingaben.value[index] = response
}

const onCopy = async (modelId) => {
  const response = await copyItem({
    model: 'klimacheck',
    modelId,
    detail: {
      success: 'Klimacheck erfolgreich kopiert',
      error: 'Fehler beim Kopieren des Klimachecks'
    }
  })
  eingaben.value.unshift(response)
}

const onDelete = async (modelId) => {
  await deleteItem({
    model: 'klimacheck/eingabe',
    modelId,
    detail: {
      success: 'Klimacheck erfolgreich gelöscht',
      error: 'Fehler beim Löschen des Klimachecks'
    }
  })
  const index = eingaben.value.findIndex((eingabe) => eingabe.id === modelId)
  eingaben.value.splice(index, 1)
}

const onExport = async (modelId) => {
  await exportItem({
    model: 'klimacheck',
    modelId,
    detail: {
      success: 'Klimacheck erfolgreich exportiert',
      error: 'Fehler beim Exportieren des Klimachecks'
    }
  })
}
</script>

<style scoped>
/* Add your styling here */
</style>
