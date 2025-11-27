<template>
  <div>
    <BaseModal v-model="isModalOpen" @close="toggleModal">
      <template #header>
        <h2>Leitziel hinzufügen</h2>
      </template>
      <EinstellungenMobilitaetscheckFormularZielOber
        :editMode="false"
        :naechsteNr="naechsteNr"
        @add-item="onSubmit"
      />
    </BaseModal>
    <div class="flex gap-4 items-center mb-5">
      <BaseSubheading>Leitziele</BaseSubheading>
      <Button
        v-tooltip="'Neues Leitziel hinzufügen'"
        icon="pi pi-plus"
        rounded
        aria-label="Neues Leitzziel hinzufügen"
        @click="toggleModal"
      />
    </div>
    <BaseSpinner v-if="isLoading" class="m-10" />
    <div v-else-if="zielOberListe.length === 0">
      <p class="font-lg font-bold m-5">Keine Leitziele vorhanden.</p>
    </div>
    <div v-else>
      <Draggable v-model="zielOberListe" item-key="id" @end="onDragEnd" animation="200">
        <template #item="{ element }">
          <EinstellungenMobilitaetscheckZielOberItem
            :item="element"
            @delete-ziel-ober="onDeleteZielOber"
            @update-ziel-ober="onUpdateZielOber"
          />
        </template>
      </Draggable>
    </div>
  </div>
</template>

<script setup>
import { computed, ref, onMounted } from 'vue'
import {
  createItem,
  fetchItems,
  updateItem,
  updateItemSilent,
  deleteItem
} from '@/composables/crud'
import Button from 'primevue/button'
import Draggable from 'vuedraggable'
import BaseSpinner from '@/components/BaseSpinner.vue'
import EinstellungenMobilitaetscheckFormularZielOber from './EinstellungenMobilitaetscheckFormularZielOber.vue'
import EinstellungenMobilitaetscheckZielOberItem from './EinstellungenMobilitaetscheckZielOberItem.vue'

const isLoading = ref(false)
const isModalOpen = ref(false)
const zielOberListe = ref([])

onMounted(async () => {
  await fetchZielOberListe()
})

const toggleModal = () => {
  isModalOpen.value = !isModalOpen.value
}

const fetchZielOberListe = async () => {
  isLoading.value = true
  zielOberListe.value = await fetchItems('/einstellungen/mobilitaetscheck/ziel/ober')
  isLoading.value = false
}

const onDeleteZielOber = async (id) => {
  await deleteItem({
    model: 'einstellungen/mobilitaetscheck/ziel/ober',
    modelId: id,
    detail: {
      success: 'Leitziel erfolgreich gelöscht',
      error: 'Fehler beim Löschen des Leitziels'
    }
  })
  const ix = zielOberListe.value.findIndex((ziel) => ziel.id === id)
  if (ix !== -1) {
    zielOberListe.value.splice(ix, 1)
  }
}

const naechsteNr = computed(() => {
  return zielOberListe.value.length + 1
})

const onUpdateZielOber = async ({ modelId, values }) => {
  const response = await updateItem({
    model: 'einstellungen/mobilitaetscheck/ziel/ober',
    modelId,
    values,
    detail: {
      success: 'Leitziel erfolgreich aktualisiert',
      error: 'Fehler beim Aktualisieren des Leitziels'
    }
  })
  const ix = zielOberListe.value.findIndex((zielOber) => zielOber.id === response.id)
  if (ix !== -1) {
    zielOberListe.value.splice(ix, 1, response)
  }
}

const onSubmit = async (values) => {
  const response = await createItem({
    model: 'einstellungen/mobilitaetscheck/ziel/ober',
    values: values,
    detail: {
      success: 'Leitziel erfolgreich hinzugefügt',
      error: 'Fehler beim Hinzufügen des Leitziels'
    }
  })
  zielOberListe.value.push(response)
  toggleModal()
}

const onDragEnd = () => {
  zielOberListe.value.forEach((item, index) => {
    item.nr = index + 1
  })
  // Optionally, you can update the order in the backend if needed
  zielOberListe.value.forEach(async (item) => {
    await updateItemSilent({
      model: 'einstellungen/mobilitaetscheck/ziel/ober',
      modelId: item.id,
      values: { nr: item.nr }
    })
  })
}
</script>

<style scoped>
/* Add your styling here */
</style>
