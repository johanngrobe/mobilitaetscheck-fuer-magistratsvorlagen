<template>
  <div>
    <!-- Display list of submissions -->

    <BaseModal v-model="isModalOpen" @close="toggleModal">
      <template #header>
        <h2>Indikator hinzufügen</h2>
      </template>
      <EinstellungenIndikatorFormular :editMode="false" :tags="tags" @add-item="onSubmit" />
    </BaseModal>
    <div class="flex gap-4 items-center mb-5">
      <BaseSubheading>Indikatoren</BaseSubheading>
      <Button
        v-tooltip="'Neuen Indiaktor hinzufügen'"
        icon="pi pi-plus"
        rounded
        aria-label="Neuen Indikator hinzufügen"
        @click="toggleModal"
      />
    </div>
    <FloatLabel variant="on">
      <InputText id="searchQuery" v-model="searchQuery" class="w-full" />
      <label for="searchQuery">Nach Indikator suchen</label>
    </FloatLabel>
    <BaseSpinner v-if="isLoading" class="m-10" />
    <div v-else-if="indikatoren.length === 0">
      <p class="font-lg font-bold m-5">Keine Indikatoren vorhanden.</p>
    </div>
    <div v-else>
      <div v-for="indikator in filteredIndikatoren" :key="indikator.id">
        <EinstellungenIndikatorItem
          :item="indikator"
          :tags="tags"
          @delete-item="onDelete"
          @update-item="onUpdate"
          @publish-item="onPublish"
        />
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, ref, onMounted } from 'vue'
import { createItem, deleteItem, fetchItems, updateItem } from '@/composables/crud'
import Button from 'primevue/button'
import InputText from 'primevue/inputtext'
import FloatLabel from 'primevue/floatlabel'
import BaseSpinner from '@/components/BaseSpinner.vue'
import EinstellungenIndikatorFormular from '@/components/EinstellungenIndikatorFormular.vue'
import EinstellungenIndikatorItem from '@/components/EinstellungenIndikatorItem.vue'

const isLoading = ref(false)
const isModalOpen = ref(false)
const indikatoren = ref([])
const tags = ref([])
const searchQuery = ref('')

onMounted(async () => {
  await fetchIndikatoren()
  await fetchTags()
})

const toggleModal = () => {
  isModalOpen.value = !isModalOpen.value
}

const fetchIndikatoren = async () => {
  isLoading.value = true
  indikatoren.value = await fetchItems('/einstellungen/indikator')
  isLoading.value = false
}

const fetchTags = async () => {
  tags.value = await fetchItems('/einstellungen/tag')
}

// Computed property to filter submissions by multiple fields
const filteredIndikatoren = computed(() => {
  return indikatoren.value.filter((indikator) => {
    const query = searchQuery.value.toLowerCase()
    isLoading.value = true
    let results = indikator.name.toLowerCase().includes(query)

    isLoading.value = false
    return results
  })
})

const onPublish = async ({ modelId, values }) => {
  const response = await updateItem({
    model: 'einstellungen/indikator',
    modelId,
    values,
    detail: {
      success: values.gemeindespezifisch
        ? 'Indiaktor veröffentlicht'
        : 'Veröffentlichung zurückgezogen',
      error: 'Fehler beim Veröffentlichen des Indikators'
    }
  })
  const index = indikatoren.value.findIndex((eingabe) => eingabe.id === modelId)
  indikatoren.value[index].gemeindespezifisch = response.gemeindespezifisch
}

const onDelete = async (modelId) => {
  await deleteItem({
    model: 'einstellungen/indikator',
    modelId,
    detail: {
      success: 'Indikator erfolgreich gelöscht',
      error: 'Fehler beim Löschen des Indikators'
    }
  })
  const ix = indikatoren.value.findIndex((indikator) => indikator.id === modelId)
  if (ix !== -1) {
    indikatoren.value.splice(ix, 1)
  }
}

const onUpdate = async ({ modelId, values }) => {
  const response = await updateItem({
    model: 'einstellungen/indikator',
    modelId,
    values,
    detail: {
      success: 'Indikator erfolgreich aktualisiert',
      error: 'Fehler beim Aktualisieren des Indikators'
    }
  })
  const ix = indikatoren.value.findIndex((indikator) => indikator.id === modelId)
  if (ix !== -1) {
    indikatoren.value.splice(ix, 1, response)
  }
}

const onSubmit = async (values) => {
  const response = await createItem({
    model: 'einstellungen/indikator',
    values,
    detail: {
      success: 'Indikator erfolgreich hinzugefügt',
      error: 'Fehler beim Hinzufügen des Indikators'
    }
  })
  indikatoren.value.unshift(response)
  toggleModal()
}
</script>

<style scoped>
/* Add your styling here */
</style>
