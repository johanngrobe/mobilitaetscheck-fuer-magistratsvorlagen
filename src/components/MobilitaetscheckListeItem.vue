<template>
  <div>
    <BaseModal v-model="editMode">
      <template #header>
        <h2>{{ props.item.name || 'Kein Name' }} bearbeiten</h2>
      </template>
      <MobilitaetscheckFormularEingabeZielOber
        :editMode="editMode"
        :item="props.item"
        @close-modal="toggleEditMode"
        @reload-item="emit('reload-item', props.item.id)"
      />
    </BaseModal>
    <BaseCard>
      <div class="col-span-10 grid grid-cols-1 gap-x-4 gap-y-1">
        <h3 class="font-bold text-lg">{{ props.item.name || 'Kein Name' }}</h3>
        <div class="grid grid-cols-2 gap-4">
          <div class="flex items-center gap-2">
            <span class="font-semibold">Erstellt von</span>
            <span>{{ props.item.autor?.vorname }} {{ props.item.autor?.nachname }}</span>
          </div>
          <div class="flex items-center gap-2">
            <span class="font-semibold">Erstellt am</span>
            <span>{{ new Date(props.item.erstelltAm).toLocaleDateString('de-DE') }}</span>
          </div>
        </div>
      </div>
      <div class="col-span-2 grid grid-cols-1 items-center gap-y-1">
        <div v-if="userRolleZugang" class="grid grid-cols-5 items-center gap-1">
          <div class="col-span-4 flex gap-2">
            <ToggleButton
              v-model="veroeffentlicht"
              onLabel="veröffentlicht"
              offLabel="verwaltungsintern"
              onIcon="pi pi-lock-open"
              offIcon="pi pi-lock"
              @change="onPublish"
              size="small"
              style="width: 10rem"
            />
            <Button
              icon="pi pi-pen-to-square"
              v-if="userRolleZugang"
              @click="toggleEditMode"
              label="bearbeiten"
              size="small"
            />
            <ButtonBearbeiten v-if="userRolleZugang(['politik'])" @click="onCopy" color="green"
              >In meine Datenbank kopieren</ButtonBearbeiten
            >
            <Button icon="pi pi-download" @click="onExport" label="PDF-Export" size="small" />
          </div>
          <div class="flex justify-end">
            <ButtonLoeschen v-if="userRolleZugang" @delete-confirmed="onDelete" />
          </div>
        </div>
      </div>
    </BaseCard>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'

import ToggleButton from 'primevue/togglebutton'

import MobilitaetscheckFormularEingabeZielOber from '@/components/MobilitaetscheckFormularEingabeZielOber.vue'
import ButtonBearbeiten from '@/components/ButtonBearbeiten.vue'
import Button from 'primevue/button'
import ButtonLoeschen from '@/components/ButtonLoeschen.vue'

const veroeffentlicht = ref()
const editMode = ref(false)
const authStore = useAuthStore()

const props = defineProps({
  item: Object
})

onMounted(() => {
  veroeffentlicht.value = props.item.veroeffentlicht
})

const toggleEditMode = () => {
  editMode.value = !editMode.value
}

const userRolleZugang = (fuerUserRollen = ['verwaltung']) => {
  return fuerUserRollen.includes(authStore.userRolle)
}

const emit = defineEmits([
  'update-item',
  'delete-item',
  'copy-item',
  'publish-item',
  'export-item',
  'reload-item'
])

const onPublish = () => {
  emit('publish-item', {
    modelId: props.item.id,
    values: { veroeffentlicht: veroeffentlicht.value }
  })
}

// const onUpdate = (values) => {
//   emit('update-item', { modelId: props.item.id, values })
// }

const onExport = () => {
  emit('export-item', props.item.id)
}

const onDelete = () => {
  emit('delete-item', props.item.id)
}

const onCopy = () => {
  emit('copy-item', props.item.id)
}
</script>

<style></style>
