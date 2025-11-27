<template>
  <form @submit.prevent="onSubmit">
    <div class="grid grid-cols-1 gap-2">
      <div class="flex w-full">
        <div>
          <FloatLabel variant="on">
            <InputNumber
              id="zielOber"
              v-model="nr"
              class="w-16 me-2"
              inputClass="w-16"
              :invalid="!!errors.nr"
              :min="1"
              :step="1"
              disabled
            />
            <name for="zielOber">#</name>
          </FloatLabel>
          <small v-if="errors.nr" id="nr-help" class="p-error block">{{ errors.nr }}</small>
        </div>
        <div class="w-full">
          <FloatLabel variant="on" class="w-full">
            <InputText
              id="name"
              v-model="name"
              class="w-full"
              inputClass="w-full"
              :invalid="!!errors.name"
            />
            <name for="name">Leitziel eingeben</name>
          </FloatLabel>
          <small v-if="errors.name" id="name-help" class="p-error block">{{ errors.name }}</small>
        </div>
      </div>
      <div class="flex justify-end">
        <ButtonSpeichern type="submit" />
      </div>
    </div>
  </form>
</template>

<script setup>
import { onMounted } from 'vue'
import { useForm } from 'vee-validate'
import { schema } from '@/utils/schemas/ZielOber'
import FloatLabel from 'primevue/floatlabel'
import InputText from 'primevue/inputtext'
import InputNumber from 'primevue/inputnumber'
import ButtonSpeichern from '@/components/ButtonSpeichern.vue'

const props = defineProps({
  editMode: {
    type: Boolean,
    default: false
  },
  item: Object,
  naechsteNr: {
    type: Number,
    default: null
  }
})

const { defineField, handleSubmit, errors, setValues, setFieldValue } = useForm({
  validationSchema: schema
})

// Define form state
const [nr] = defineField('nr')
const [name] = defineField('name')

onMounted(() => {
  if (props.editMode) {
    setValues({
      nr: props.item.nr,
      name: props.item.name
    })
  } else {
    setFieldValue('nr', props.naechsteNr)
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
