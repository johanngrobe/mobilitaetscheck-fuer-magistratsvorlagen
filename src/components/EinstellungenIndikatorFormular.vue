<template>
  <form @submit.prevent="onSubmit">
    <div class="grid grid-cols-1 gap-2">
      <div class="grid grid-cols-1 gap-3">
        <div class="w-full">
          <FloatLabel variant="on" class="w-full">
            <InputText id="name" v-model="name" class="w-full" :invalid="!!errors.name" />
            <label for="name">Indikator-Bezeichnung</label>
          </FloatLabel>
          <small v-if="errors.name" id="name-help" class="p-error block">{{ errors.name }}</small>
        </div>
        <div class="w-full">
          <FloatLabel variant="on" class="w-full">
            <InputText
              id="quelleUrl"
              v-model.trim="quelleUrl"
              class="w-full"
              :invalid="!!errors.quelleUrl"
            />
            <label for="quelleUrl">Quellen-URL</label>
          </FloatLabel>
          <small v-if="errors.quelleUrl" id="quelleUrl-help" class="p-error block">{{
            errors.quelleUrl
          }}</small>
        </div>
        <FloatLabel variant="on">
          <MultiSelect
            id="tags"
            v-model="tagIds"
            :options="props.tags"
            optionLabel="name"
            optionValue="id"
            display="chip"
            class="w-full"
          />
          <label for="tags">Tags auswählen</label>
        </FloatLabel>
      </div>
      <div class="flex justify-end items-center">
        <ButtonSpeichern type="submit" />
      </div>
    </div>
  </form>
</template>

<script setup>
import { onMounted } from 'vue'
import { useForm } from 'vee-validate'
import { schema } from '@/utils/schemas/indikator.js'
import FloatLabel from 'primevue/floatlabel'
import InputText from 'primevue/inputtext'
import MultiSelect from 'primevue/multiselect'
import ButtonSpeichern from '@/components/ButtonSpeichern.vue'

const props = defineProps({
  editMode: {
    type: Boolean,
    required: true
  },
  item: {
    type: Object,
    default: null
  },
  tags: Array
})

const { defineField, handleSubmit, errors, setValues } = useForm({
  validationSchema: schema
})

const [name] = defineField('name')
const [quelleUrl] = defineField('quelleUrl')
const [tagIds] = defineField('tagIds')

onMounted(() => {
  if (props.editMode) {
    setValues({
      name: props.item.name,
      tagIds: props.item.tagIds,
      quelleUrl: props.item.quelleUrl
    })
  }
})

const emit = defineEmits(['add-item', 'update-item'])

const onSubmit = handleSubmit(async (values) => {
  if (props.editMode) {
    emit('update-item', { modelId: props.item.id, values })
  } else {
    emit('add-item', values)
  }
})
</script>

<style scoped>
.p-invalid {
  @apply border-red-600 text-red-600;
}

.p-error {
  @apply text-red-600;
}
</style>
