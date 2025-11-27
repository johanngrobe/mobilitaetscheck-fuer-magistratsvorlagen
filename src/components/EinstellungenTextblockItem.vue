<template>
  <div>
    <BaseModal v-model="editMode">
      <template #header>
        <h2>Textblock bearbeiten</h2>
      </template>
      <EinstellungenTextblockFormular
        :editMode="true"
        :item="props.item"
        :tags="props.tags"
        @update-item="onUpdate"
      />
    </BaseModal>
    <BaseCard class="hover:bg-gray-200">
      <div>
        <div class="grid grid-cols-12 gap-2">
          <div class="col-span-10 grid grid-cols-1 gap-2">
            <h3>{{ props.item.name }}</h3>
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
            <ButtonBearbeiten @click="toggleEditMode" noLabel :disabled="andereGemeinde" />
            <ButtonLoeschen @delete-confirmed="onDelete" noLabel :disabled="andereGemeinde" />
          </div>
        </div>
      </div>
    </BaseCard>
  </div>
</template>

<script setup>
import { computed, ref, onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'
import ToggleSwitch from 'primevue/toggleswitch'
import EinstellungenTextblockFormular from '@/components/EinstellungenTextblockFormular.vue'
import ButtonLoeschen from '@/components/ButtonLoeschen.vue'
import ButtonBearbeiten from '@/components/ButtonBearbeiten.vue'
import Tag from 'primevue/tag'

const props = defineProps({
  item: Object,
  tags: Array
})

const editMode = ref(false)
const gemeindespezifisch = ref()
const authStore = useAuthStore()

const toggleEditMode = () => {
  editMode.value = !editMode.value
}

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
