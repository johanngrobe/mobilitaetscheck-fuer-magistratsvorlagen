<template>
  <div>
    <BaseModal v-model="isModalOpen" @close="toggleModal">
      <template #header>
        <h2>Textblock hinzufügen</h2>
      </template>
      <EinstellungenTextblockFormular :editMode="false" :tags="tags" @add-item="onSubmit" />
    </BaseModal>
    <div class="flex gap-4 items-center mb-5">
      <BaseSubheading>Textblöcke</BaseSubheading>
      <Button
        v-tooltip="'Neuen Textblock hinzufügen'"
        icon="pi pi-plus"
        rounded
        aria-label="Neuen Textblock hinzufügen"
        @click="toggleModal"
      />
    </div>
    <FloatLabel variant="on">
      <InputText id="searchQuery" v-model="searchQuery" class="w-full" />
      <label for="searchQuery">Nach Textblock suchen</label>
    </FloatLabel>
    <BaseSpinner v-if="isLoading" class="m-10" />
    <div v-else-if="textblocks.length === 0">
      <p class="font-lg font-bold m-5">Keine Textblöcke vorhanden.</p>
    </div>
    <div v-else>
      <div v-for="textblock in filteredTextblocks" :key="textblock.id">
        <EinstellungenTextblockItem
          :item="textblock"
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
import { fetchItems, deleteItem, createItem, updateItem } from '@/composables/crud'
import EinstellungenTextblockFormular from '@/components/EinstellungenTextblockFormular.vue'
import EinstellungenTextblockItem from '@/components/EinstellungenTextblockItem.vue'
import BaseSpinner from '@/components/BaseSpinner.vue'
import Button from 'primevue/button'
import InputText from 'primevue/inputtext'
import FloatLabel from 'primevue/floatlabel'

const isLoading = ref(false)
const isModalOpen = ref(false)
const textblocks = ref([])
const tags = ref([])

const searchQuery = ref('')

onMounted(async () => {
  await fetchTextblocks()
  await fetchTags()
})

const toggleModal = () => {
  isModalOpen.value = !isModalOpen.value
}

const fetchTextblocks = async () => {
  isLoading.value = true
  textblocks.value = await fetchItems('/einstellungen/textblock')
  isLoading.value = false
}

const fetchTags = async () => {
  tags.value = await fetchItems('/einstellungen/tag')
}

// Computed property to filter submissions by multiple fields
const filteredTextblocks = computed(() => {
  return textblocks.value.filter((textblock) => {
    const query = searchQuery.value.toLowerCase()
    isLoading.value = true
    let results = textblock.name.toLowerCase().includes(query)

    isLoading.value = false
    return results
  })
})

const onPublish = async ({ modelId, values }) => {
  const response = await updateItem({
    model: 'einstellungen/textblock',
    modelId,
    values,
    detail: {
      success: values.gemeindespezifisch
        ? 'Textblock veröffentlicht'
        : 'Veröffentlichung zurückgezogen',
      error: 'Fehler beim Veröffentlichen des Textblocks'
    }
  })
  const index = textblocks.value.findIndex((eingabe) => eingabe.id === modelId)
  textblocks.value[index].gemeindespezifisch = response.gemeindespezifisch
}

const onDelete = async (modelId) => {
  await deleteItem({
    model: 'einstellungen/textblock',
    modelId,
    detail: {
      success: 'Textblock erfolgreich gelöscht',
      error: 'Fehler beim Löschen des Textblocks'
    }
  })
  const ix = textblocks.value.findIndex((item) => item.id === modelId)
  if (ix !== -1) {
    textblocks.value.splice(ix, 1)
  }
}

const onUpdate = async ({ modelId, values }) => {
  const response = await updateItem({
    model: 'einstellungen/textblock',
    modelId,
    values,
    detail: {
      success: 'Textblock erfolgreich aktualisiert',
      error: 'Fehler beim Aktualisieren des Textblock'
    }
  })
  const ix = textblocks.value.findIndex((item) => item.id === response.id)
  if (ix !== -1) {
    textblocks.value.splice(ix, 1, response)
  }
}

const onSubmit = async (values) => {
  const response = await createItem({
    model: 'einstellungen/textblock',
    values,
    detail: {
      success: 'Textblock erfolgreich hinzugefügt',
      error: 'Fehler beim Hinzufügen des Textblock'
    }
  })
  textblocks.value.unshift(response)
  toggleModal()
}
</script>

<style scoped>
/* Add your styling here */
</style>
