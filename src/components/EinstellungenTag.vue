<template>
  <div>
    <!-- Display list of submissions -->

    <BaseModal v-model="isModalOpen" @close="toggleModal">
      <template #header>
        <h2>Tag hinzufügen</h2>
      </template>
      <EinstellungenTagFormular :editMode="false" @add-item="onSubmit" />
    </BaseModal>
    <div class="flex gap-4 items-center mb-5">
      <BaseSubheading>Tags</BaseSubheading>
      <Button
        v-tooltip="'Neuen Tag hinzufügen'"
        icon="pi pi-plus"
        rounded
        aria-label="Neuen Tag hinzufügen"
        @click="toggleModal"
      />
    </div>
    <FloatLabel variant="on">
      <InputText id="searchQuery" v-model="searchQuery" class="w-full" />
      <label for="searchQuery">Nach Tag suchen</label>
    </FloatLabel>
    <BaseSpinner v-if="isLoading" class="m-10" />
    <div v-else-if="tags.length === 0">
      <p class="font-lg font-bold m-5">Keine Tags vorhanden.</p>
    </div>
    <div v-else>
      <div v-for="tag in filteredTags" :key="tag.id">
        <EinstellungenTagItem
          :item="tag"
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
import { fetchItems, deleteItem, createItem, updateItem } from '@/composables/crud'
import InputText from 'primevue/inputtext'
import FloatLabel from 'primevue/floatlabel'
import EinstellungenTagFormular from '@/components/EinstellungenTagFormular.vue'
import EinstellungenTagItem from '@/components/EinstellungenTagItem.vue'
import BaseSpinner from '@/components/BaseSpinner.vue'
import Button from 'primevue/button'

const isLoading = ref(false)
const isModalOpen = ref(false)
const tags = ref([])
const searchQuery = ref('')

onMounted(async () => {
  await fetchTags()
})

const toggleModal = () => {
  isModalOpen.value = !isModalOpen.value
}

const fetchTags = async () => {
  isLoading.value = true
  tags.value = await fetchItems('/einstellungen/tag')
  isLoading.value = false
}

// Computed property to filter submissions by multiple fields
const filteredTags = computed(() => {
  return tags.value.filter((tag) => {
    const query = searchQuery.value.toLowerCase()
    isLoading.value = true
    let results = tag.name.toLowerCase().includes(query)

    isLoading.value = false
    return results
  })
})

const onPublish = async ({ modelId, values }) => {
  const response = await updateItem({
    model: 'einstellungen/tag',
    modelId,
    values,
    detail: {
      success: values.gemeindespezifisch ? 'Tag veröffentlicht' : 'Veröffentlichung zurückgezogen',
      error: 'Fehler beim Veröffentlichen des Tags'
    }
  })
  const index = tags.value.findIndex((eingabe) => eingabe.id === modelId)
  tags.value[index].gemeindespezifisch = response.gemeindespezifisch
}

const onDelete = async (modelId) => {
  await deleteItem({
    model: 'einstellungen/tag',
    modelId,
    detail: {
      success: 'Tag erfolgreich gelöscht',
      error: 'Fehler beim Löschen des Tags'
    }
  })
  const ix = tags.value.findIndex((tag) => tag.id === modelId)
  if (ix !== -1) {
    tags.value.splice(ix, 1)
  }
}

const onUpdate = async ({ modelId, values }) => {
  const response = await updateItem({
    model: 'einstellungen/tag',
    modelId,
    values,
    detail: {
      success: 'Tag erfolgreich aktualisiert',
      error: 'Fehler beim Aktualisieren des Tags'
    }
  })
  const ix = tags.value.findIndex((tag) => tag.id === modelId)
  if (ix !== -1) {
    tags.value[ix] = response
  }
}

const onSubmit = async (values) => {
  const response = await createItem({
    model: 'einstellungen/tag',
    values,
    detail: {
      success: 'Tag erfolgreich hinzugefügt',
      error: 'Fehler beim Hinzufügen des Tags'
    }
  })
  tags.value.unshift(response)
  toggleModal()
}
</script>

<style scoped>
/* Add your styling here */
</style>
