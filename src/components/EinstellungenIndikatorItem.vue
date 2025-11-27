<template>
  <BaseModal v-model="editMode" @close="toggleEditMode">
    <template #header>
      <h2>Indikator hinzufügen</h2>
    </template>
    <EinstellungenIndikatorFormular
      :editMode="true"
      :item="props.item"
      :tags="tags"
      @update-item="onUpdate"
    />
  </BaseModal>
  <BaseCard>
    <div class="grid grid-cols-12 gap-x-2">
      <div class="col-span-10 grid grid-cols-1 gap-2">
        <h3>
          <div v-if="props.item.quelleUrl">
            <a
              v-tooltip.top="'Quelle öffnen'"
              :href="props.item.quelleUrl"
              target="_blank"
              class="w-fit flex items-center gap-2 text-blue-800 hover:underline"
            >
              <span>{{ props.item.name }}</span>
            </a>
          </div>
          <div v-else class="flex items-center gap-2">
            <span v-tooltip.top="'Keine URL hinterlegt'">{{ props.item.name }}</span>
          </div>
        </h3>

        <div class="flex items-center gap-2">
          <div v-if="props.item.tags.length > 0" class="flex items-center gap-2">
            <div v-for="tag in props.item.tags" :key="tag.id">
              <Tag :value="tag.name" />
            </div>
          </div>
        </div>
      </div>
      <div class="col-span-2 flex items-center justify-end gap-1">
        <ToggleSwitch
          v-model="gemeindespezifisch"
          v-tooltip="'Status gemeindespezifisch'"
          @change="onPublish"
          :disabled="andereGemeinde"
        />
        <ButtonBearbeiten @click="toggleEditMode" :disabled="andereGemeinde" noLabel />
        <ButtonLoeschen @delete-confirmed="onDelete" :disabled="andereGemeinde" noLabel />
      </div>
    </div>
  </BaseCard>
</template>

<script setup>
import { computed, ref, onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'
import EinstellungenIndikatorFormular from '@/components/EinstellungenIndikatorFormular.vue'
import ButtonLoeschen from '@/components/ButtonLoeschen.vue'
import ButtonBearbeiten from '@/components/ButtonBearbeiten.vue'
import Tag from 'primevue/tag'
import ToggleSwitch from 'primevue/toggleswitch'

const authStore = useAuthStore()
const editMode = ref(false)
const gemeindespezifisch = ref()

const toggleEditMode = () => {
  editMode.value = !editMode.value
}

const props = defineProps({
  item: Object,
  tags: Array
})

onMounted(() => {
  gemeindespezifisch.value = props.item.gemeindespezifisch
})

const andereGemeinde = computed(() => {
  return props.item.gemeindeId !== authStore.gemeindeId
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
