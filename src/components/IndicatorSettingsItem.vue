<template>
  <BaseModal v-model="editMode" @close="toggleEditMode">
    <template #header>
      <h2>Indikator hinzufügen</h2>
    </template>
    <IndicatorForm :editMode="true" :item="props.item" :tags="tags" @update-item="onUpdate" />
  </BaseModal>
  <BaseCard>
    <div class="grid grid-cols-12 gap-x-2">
      <div class="col-span-10 grid grid-cols-1 gap-2">
        <h3>
          <div v-if="props.item.sourceUrl">
            <a
              v-tooltip.top="'Quelle öffnen'"
              :href="props.item.sourceUrl"
              target="_blank"
              class="w-fit flex items-center gap-2 text-blue-800 hover:underline"
            >
              <span>{{ props.item.label }}</span>
            </a>
          </div>
          <div v-else class="flex items-center gap-2">
            <span v-tooltip.top="'Keine URL hinterlegt'">{{ props.item.label }}</span>
          </div>
        </h3>

        <div class="flex items-center gap-2">
          <span class="font-semibold">Tags:</span>
          <div v-if="props.item.tags.length > 0" class="flex items-center gap-2">
            <div v-for="tag in props.item.tags" :key="tag.id">
              <BaseBadge>{{ tag.label }}</BaseBadge>
            </div>
          </div>
          <div v-else>
            <BaseBadge color="red">Keine Tags vergeben</BaseBadge>
          </div>
        </div>
      </div>
      <div class="col-span-2 flex items-center justify-end gap-1">
        <ButtonBearbeiten @click="toggleEditMode" />
        <ButtonLoeschen @delete-confirmed="onDelete" />
      </div>
    </div>
  </BaseCard>
</template>

<script setup>
import { ref } from 'vue'
import IndicatorForm from '@/components/EinstellungenIndikatorFormular.vue'
import ButtonLoeschen from '@/components/ButtonLoeschen.vue'
import ButtonBearbeiten from '@/components/ButtonBearbeiten.vue'
import BaseBadge from '@/components/BaseBadge.vue'

const editMode = ref(false)

const toggleEditMode = () => {
  editMode.value = !editMode.value
}

const props = defineProps({
  item: Object,
  tags: Array
})

const emit = defineEmits(['delete-item', 'update-item'])

const onUpdate = (values) => {
  emit('update-item', values)
  toggleEditMode()
}

const onDelete = () => {
  emit('delete-item', props.item.id)
}
</script>

<style></style>
