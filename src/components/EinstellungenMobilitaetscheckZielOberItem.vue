<template>
  <div v-bind="$attrs">
    <BaseModal v-model="editMode">
      <template #header>
        <h2>Leitziel bearbeiten</h2>
      </template>
      <EinstellungenMobilitaetscheckFormularZielOber
        :editMode="true"
        :item="props.item"
        @update-item="onUpdateZielOber"
      />
    </BaseModal>
    <BaseModal v-model="addMode">
      <template #header>
        <h2>Unterziel hinzufügen</h2>
      </template>
      <EinstellungenMobilitaetscheckFormularZielUnter
        :zielOberId="props.item.id"
        :zielOber="props.item"
        @add-item="onSubmit"
        :naechsteNr="naechsteNr"
      />
    </BaseModal>
    <BaseCard>
      <div class="grid grid-cols-12 gap-x-2 items-center hover:bg-gray-200 p-2 rounded-lg">
        <div class="col-span-10 flex items-center font-bold gap-2">
          <span>{{ props.item.nr }}</span>
          <span>{{ props.item.name }}</span>
        </div>

        <div class="col-span-2 flex gap-1 items-center justify-end">
          <ButtonHinzufuegen tooltip="Unterziel hinzufügen" @click="toggleAddMode" />
          <ButtonBearbeiten @click="toggleEditMode" noLabel />
          <ButtonLoeschen @delete-confirmed="onDeleteZielOber" noLabel />
        </div>
      </div>
      <Draggable v-model="zielUnterListe" item-key="id" @end="onDragEnd" animation="200">
        <template #item="{ element }">
          <EinstellungenMobilitaetscheckZielUnterItem
            :item="element"
            @update-ziel-unter="onUpdateZielUnter"
            @delete-ziel-unter="onDeleteZielUnter"
          />
        </template>
      </Draggable>

      <!-- <div v-for="zielUnter in zielUnterListe" :key="zielUnter.id">
      <EinstellungenMobilitaetscheckZielUnterItem
        :item="zielUnter"
        @update-ziel-unter="onUpdateZielUnter"
        @delete-ziel-unter="onDeleteZielUnter"
      />
    </div> -->
    </BaseCard>
  </div>
</template>

<script setup>
import { computed, ref, onMounted } from 'vue'
import {
  createItem,
  deleteItem,
  fetchItems,
  updateItem,
  updateItemSilent
} from '@/composables/crud'
import Draggable from 'vuedraggable'

import EinstellungenMobilitaetscheckFormularZielOber from '@/components/EinstellungenMobilitaetscheckFormularZielOber.vue'
import EinstellungenMobilitaetscheckFormularZielUnter from '@/components/EinstellungenMobilitaetscheckFormularZielUnter.vue'
import EinstellungenMobilitaetscheckZielUnterItem from '@/components/EinstellungenMobilitaetscheckZielUnterItem.vue'
import ButtonLoeschen from '@/components/ButtonLoeschen.vue'
import ButtonBearbeiten from '@/components/ButtonBearbeiten.vue'
import ButtonHinzufuegen from '@/components/ButtonHinzufuegen.vue'

const editMode = ref(false)
const addMode = ref(false)

const zielUnterListe = ref()

const naechsteNr = computed(() => {
  return zielUnterListe.value.length + 1
})

const fetchSubObjectives = async () => {
  zielUnterListe.value = await fetchItems(
    '/einstellungen/mobilitaetscheck/ziel/unter/nach-parametern',
    {
      zielOberId: props.item.id
    }
  )
}

onMounted(async () => {
  await fetchSubObjectives()
})

const props = defineProps({
  item: Object
})

const toggleEditMode = () => {
  editMode.value = !editMode.value
}

const toggleAddMode = () => {
  addMode.value = !addMode.value
}

const emit = defineEmits(['delete-ziel-ober', 'update-ziel-ober'])

const onUpdateZielOber = (values) => {
  emit('update-ziel-ober', values)
  toggleEditMode()
}

const onDeleteZielOber = () => {
  emit('delete-ziel-ober', props.item.id)
}

const onSubmit = async (values) => {
  const response = await createItem({
    model: 'einstellungen/mobilitaetscheck/ziel/unter',
    values,
    detail: {
      success: 'Unterziel erfolgreich hinzugefügt',
      error: 'Fehler beim Hinzufügen des Unterziels'
    }
  })
  zielUnterListe.value.push(response)
  toggleAddMode()
}

const onUpdateZielUnter = async ({ modelId, values }) => {
  const response = await updateItem({
    model: 'einstellungen/mobilitaetscheck/ziel/unter',
    modelId,
    values,
    detail: {
      success: 'Unterziel erfolgreich aktualisiert',
      error: 'Fehler beim Aktualisieren des Unterziels'
    }
  })
  const ix = zielUnterListe.value.findIndex((zielUnter) => zielUnter.id === response.id)
  if (ix !== -1) {
    zielUnterListe.value.splice(ix, 1, response)
  }
}

const onDeleteZielUnter = async (id) => {
  await deleteItem({
    model: 'einstellungen/mobilitaetscheck/ziel/unter',
    modelId: id,
    detail: {
      success: 'Unterziel erfolgreich gelöscht',
      error: 'Fehler beim Löschen des Unterziels'
    }
  })
  const ix = zielUnterListe.value.findIndex((zielUnter) => zielUnter.id === id)
  if (ix !== -1) {
    zielUnterListe.value.splice(ix, 1)
  }
}

function onDragEnd() {
  // here you can renumber or do something after reorder
  zielUnterListe.value.forEach((item, index) => {
    item.nr = index + 1
  })
  // Optionally, you can update the backend with the new order
  zielUnterListe.value.forEach(async (item) => {
    await updateItemSilent({
      model: 'einstellungen/mobilitaetscheck/ziel/unter',
      modelId: item.id,
      values: { nr: item.nr }
    })
  })
}
</script>

<style></style>
