<template>
  <BaseModal v-model="editMode">
    <template #header>
      <h2>Tag bearbeiten</h2>
    </template>
    <EinstellungenTagFormular :editMode="true" :item="props.item" @update-item="onUpdate" />
  </BaseModal>
  <BaseCard class="hover:bg-gray-200">
    <div>
      <div class="grid grid-cols-12 gap-2">
        <div class="col-span-9 grid grid-cols-1 gap-2">
          <h3>{{ props.item.name }}</h3>
        </div>
        <div class="col-span-3 flex items-center justify-end gap-1">
          <ToggleSwitch
            v-model="gemeindespezifisch"
            v-tooltip="'Status gemeindespezifisch'"
            @change="onPublish"
            :disabled="andereGemeinde"
          />
          <ButtonBearbeiten @click="toggleEditMode" noLabel :disabled="andereGemeinde" />
          <ButtonLoeschen @delete-confirmed="onDelete" noLabel :disabled="andereGemeinde" />
        </div>
      </div>
    </div>
  </BaseCard>
</template>

<script setup>
import { computed, ref, onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'
import ToggleSwitch from 'primevue/toggleswitch'
import EinstellungenTagFormular from '@/components/EinstellungenTagFormular.vue'
import ButtonLoeschen from '@/components/ButtonLoeschen.vue'
import ButtonBearbeiten from '@/components/ButtonBearbeiten.vue'

const props = defineProps({
  item: Object
})

const authStore = useAuthStore()
const editMode = ref(false)
const gemeindespezifisch = ref()

const toggleEditMode = () => {
  editMode.value = !editMode.value
}

const andereGemeinde = computed(() => {
  return props.item.gemeindeId !== authStore.gemeindeId
})

onMounted(() => {
  gemeindespezifisch.value = props.item.gemeindespezifisch
})

const emit = defineEmits(['delete-item', 'update-item', 'publish-item'])

const onPublish = () => {
  emit('publish-item', {
    modelId: props.item.id,
    values: { gemeindespezifisch: gemeindespezifisch.value }
  })
}

const onUpdate = (values) => {
  emit('update-item', values)
  toggleEditMode()
}

const onDelete = () => {
  emit('delete-item', props.item.id)
}
</script>

<style></style>
