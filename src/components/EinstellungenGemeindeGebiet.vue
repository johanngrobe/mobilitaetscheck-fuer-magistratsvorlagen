<template>
  <div>
    <!-- Display list of submissions -->
    <ConfirmDialog />
    <Dialog
      v-model:visible="visible"
      modal
      header="Neues Gebiet hinzufügen"
      :style="{ width: '50rem' }"
    >
      <EinstellungenGemeindeGebietFormular :editMode="false" @add-item="onSubmit" />
    </Dialog>
    <Dialog v-model:visible="editMode" modal header="Gebiet bearbeiten" :style="{ width: '50rem' }">
      <EinstellungenGemeindeGebietFormular
        :editMode="true"
        :item="itemToEdit"
        @update-item="onUpdate"
      />
    </Dialog>
    <div class="flex gap-4 items-center mb-5">
      <BaseSubheading>Gebiete</BaseSubheading>
      <Button
        v-tooltip="'Neues Gebiet hinzufügen'"
        icon="pi pi-plus"
        rounded
        aria-label="Neues Gebiet hinzufügen"
        @click="visible = true"
      />
    </div>
    <FloatLabel variant="on">
      <InputText id="searchQuery" v-model="searchQuery" class="w-full" />
      <label for="searchQuery">Nach Gebiet suchen</label>
    </FloatLabel>
    <BaseSpinner v-if="isLoading" class="m-10" />
    <div v-else-if="items.length === 0">
      <p class="font-lg font-bold m-5">Keine Gebiete vorhanden.</p>
    </div>
    <div v-else>
      <DataView :value="filteredItems">
        <template #list="slotProps">
          <div class="flex flex-col">
            <div v-for="(item, index) in slotProps.items" :key="index">
              <BaseCard>
                <div>
                  <div class="grid grid-cols-12 gap-2">
                    <div class="col-span-9 grid grid-cols-1 gap-2">
                      <h3>{{ item.name }}</h3>
                    </div>
                    <div class="col-span-3 flex items-center justify-end gap-1">
                      <Button
                        icon="pi pi-pen-to-square"
                        size="small"
                        @click="toggleEditMode(item)"
                      />
                      <Button
                        icon="pi pi-trash"
                        size="small"
                        @click="confirmDelete(item.id)"
                        severity="danger"
                      />
                    </div>
                  </div>
                </div>
              </BaseCard>
            </div>
          </div>
        </template>
      </DataView>
    </div>
  </div>
</template>

<script setup>
import { computed, ref, onMounted } from 'vue'
import { createItem, deleteItem, fetchItems, updateItem } from '@/composables/crud'
import { useConfirm } from 'primevue/useconfirm'
import Button from 'primevue/button'
import DataView from 'primevue/dataview'
import ConfirmDialog from 'primevue/confirmdialog'
import Dialog from 'primevue/dialog'
import InputText from 'primevue/inputtext'
import FloatLabel from 'primevue/floatlabel'
import BaseCard from '@/components/BaseCard.vue'
import BaseSpinner from '@/components/BaseSpinner.vue'
import EinstellungenGemeindeGebietFormular from './EinstellungenGemeindeGebietFormular.vue'

const isLoading = ref(false)
const visible = ref(false)
const items = ref([])
const itemToEdit = ref()
const editMode = ref(false)
const searchQuery = ref('')
const confirm = useConfirm()

const toggleEditMode = (item) => {
  itemToEdit.value = item
  editMode.value = true
}

onMounted(async () => {
  await fetchGebiete()
})

const fetchGebiete = async () => {
  isLoading.value = true
  items.value = await fetchItems('/einstellungen/gebiet')
  isLoading.value = false
}

// Computed property to filter submissions by multiple fields
const filteredItems = computed(() => {
  return items.value.filter((item) => {
    const query = searchQuery.value.toLowerCase()
    isLoading.value = true
    let results = item.name.toLowerCase().includes(query)

    isLoading.value = false
    return results
  })
})

const onUpdate = async ({ modelId, values }) => {
  const response = await updateItem({
    model: 'einstellungen/gebiet',
    modelId,
    values,
    detail: {
      success: 'Gebiet erfolgreich aktualisiert',
      error: 'Fehler beim Aktualisieren des Gebiets'
    }
  })
  const ix = items.value.findIndex((item) => item.id === modelId)
  if (ix !== -1) {
    items.value.splice(ix, 1, response)
  }
  editMode.value = false
}

const onSubmit = async (values) => {
  const response = await createItem({
    model: 'einstellungen/gebiet',
    values,
    detail: {
      success: 'Gebiet erfolgreich hinzugefügt',
      error: 'Fehler beim Hinzufügen des Gebiets'
    }
  })
  items.value.unshift(response)
  visible.value = false
}

const confirmDelete = (modelId) => {
  confirm.require({
    message: 'Möchten Sie diese Gebietszone löschen?',
    header: 'Löschen bestätigen',
    icon: 'pi pi-exclamation-triangle',
    rejectProps: {
      label: 'Abbrechen',
      severity: 'secondary',
      outlined: true
    },
    acceptProps: {
      label: 'löschen',
      severity: 'danger'
    },
    accept: async () => {
      await deleteItem({
        model: 'einstellungen/gebiet',
        modelId,
        detail: {
          success: 'Gebiet erfolgreich gelöscht',
          error: 'Fehler beim Löschen des Gebiets'
        }
      })
      const ix = items.value.findIndex((item) => item.id === modelId)
      if (ix !== -1) {
        items.value.splice(ix, 1)
      }
    }
  })
}
</script>

<style scoped>
/* Add your styling here */
</style>
