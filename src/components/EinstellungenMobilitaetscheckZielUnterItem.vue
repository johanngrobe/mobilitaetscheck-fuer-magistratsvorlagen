<template>
  <div v-bind="$attrs">
    <BaseModal v-model="editMode">
      <template #header>
        <h2>Unterziel bearbeiten</h2>
      </template>
      <EinstellungenMobilitaetscheckFormularZielUnter
        :editMode="true"
        :item="props.item"
        :zielOberId="props.item.zielOber.id"
        :zielOber="props.item.zielOber"
        @update-item="onUpdate"
      />
    </BaseModal>
    <div class="grid grid-cols-12 gap-x-2 px-2 py-1 ms-3 hover:bg-gray-200 rounded-lg">
      <div class="col-span-10 flex items-center gap-2">
        <IconDrag class="w-4" />
        <span>{{ props.item.nr }}</span>
        <span>{{ props.item.name }}</span>
      </div>
      <div class="col-span-2 flex items-center justify-end gap-1">
        <ButtonBearbeiten @click="toggleEditMode" noLabel />
        <ButtonLoeschen @delete-confirmed="deleteZielUnter" noLabel />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import EinstellungenMobilitaetscheckFormularZielUnter from '@/components/EinstellungenMobilitaetscheckFormularZielUnter.vue'
import ButtonBearbeiten from '@/components/ButtonBearbeiten.vue'
import ButtonLoeschen from '@/components/ButtonLoeschen.vue'

import IconDrag from '@/assets/icons/MaterialSymbolsDragHandle.svg?component'

const editMode = ref(false)

const props = defineProps({
  item: Object
})

const toggleEditMode = () => {
  editMode.value = !editMode.value
}

const emit = defineEmits(['delete-ziel-unter', 'update-ziel-unter'])

const onUpdate = (values) => {
  emit('update-ziel-unter', values)
  toggleEditMode()
}

const deleteZielUnter = () => {
  emit('delete-ziel-unter', props.item.id)
}
</script>

<style></style>
