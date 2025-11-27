<template>
  <div class="my-5">
    <!-- <FloatLabel variant="on">
      <InputText id="searchQuery" v-model="searchQuery" class="w-full" />
      <label for="searchQuery">Nach Mobilitätscheck suchen</label>
    </FloatLabel> -->
    <BaseSpinner v-if="isLoading" class="m-10" />
    <div v-else-if="filteredEingaben.length === 0">
      <p class="font-lg font-bold m-5">Keine Mobilitätschecks gefunden.</p>
    </div>
    <div v-else>
      <div v-for="eingabe in filteredEingaben" :key="eingabe.id">
        <MobilitaetscheckListeItem
          :item="eingabe"
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
import MobilitaetscheckListeItem from '@/components/MobilitaetscheckListeItem.vue'
import InputText from 'primevue/inputtext'
import FloatLabel from 'primevue/floatlabel'
import BaseSpinner from '@/components/BaseSpinner.vue'

const route = useRoute()
const isLoading = ref(false)
const eingaben = ref([])
const searchQuery = ref('')

const fetchEingaben = async () => {
  isLoading.value = true
  eingaben.value = await fetchItems(`mobilitaetscheck/eingabe/magistratsvorlage/${route.params.id}`)
  isLoading.value = false
}

const refetchEingabe = async (id) => {
  const index = eingaben.value.findIndex((eingabe) => eingabe.id === id)
  if (index !== -1) {
    eingaben.value[index] = await fetchItems(`mobilitaetscheck/eingabe/${id}`)
  }
}

onMounted(async () => {
  await fetchEingaben()
})

// Computed property to filter submissions by multiple fields
const filteredEingaben = computed(() => {
  return eingaben.value.filter((eingabe) => {
    const query = searchQuery.value.toLowerCase()
    isLoading.value = true
    let results =
      eingabe.name.toLowerCase().includes(query) ||
      eingabe.autor.toLowerCase().includes(query) ||
      eingabe.erstelltAm.includes(query) // Date format remains the same, no need to lowercase
    isLoading.value = false
    return results
  })
})

const onPublish = async ({ modelId, values }) => {
  const response = await updateItem({
    model: 'mobilitaetscheck/eingabe',
    modelId,
    values,
    detail: {
      success: values.veroeffentlicht
        ? 'Mobilitätscheck veröffentlicht'
        : 'Veröffentlichung zurückgezogen',
      error: 'Fehler beim Veröffentlichen des Mobilitätschecks'
    }
  })
  const index = eingaben.value.findIndex((eingabe) => eingabe.id === modelId)
  eingaben.value[index].veroeffentlicht = response.veroeffentlicht
}

const onCopy = async (modelId) => {
  const response = await copyItem({
    model: 'mobilitaetscheck/eingabe',
    modelId,
    detail: {
      success: 'Mobilitätscheck erfolgreich kopiert',
      error: 'Fehler beim Kopieren des Mobilitätschecks'
    }
  })
  eingaben.value.unshift(response)
}

const onDelete = async (modelId) => {
  await deleteItem({
    model: 'mobilitaetscheck/eingabe',
    modelId,
    detail: {
      success: 'Mobilitätscheck erfolgreich gelöscht',
      error: 'Fehler beim Löschen des Mobilitätschecks'
    }
  })
  const index = eingaben.value.findIndex((eingabe) => eingabe.id === modelId)
  eingaben.value.splice(index, 1)
}

const onExport = async (modelId) => {
  await exportItem({
    model: 'mobilitaetscheck',
    modelId,
    detail: {
      success: 'Mobilitätscheck erfolgreich exportiert',
      error: 'Fehler beim Exportieren des Mobilitätschecks'
    }
  })
}
</script>

<style scoped>
/* Add your styling here */
</style>
