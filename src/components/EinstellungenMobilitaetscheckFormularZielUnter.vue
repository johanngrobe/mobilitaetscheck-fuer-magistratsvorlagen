<template>
  <form @submit.prevent="onSubmit">
    <div class="grid grid-cols-1 gap-2">
      <div class="flex gap-2 font-bold p-1">
        <span>Leitziel:</span>
        <span>{{ props.zielOber.nr }}</span
        ><span>{{ props.zielOber.name }}</span>
      </div>
      <div class="flex gap-2">
        <div>
          <FloatLabel variant="on">
            <InputNumber
              id="nr"
              v-model="nr"
              class="w-16"
              inputClass="w-16"
              locale="de-DE"
              :min="1"
              :step="1"
              :disabled="true"
              required="true"
            />
            <label for="nr">#</label>
          </FloatLabel>
          <small v-if="errors.nr" id="nr-help" class="p-error block">{{ errors.nr }}</small>
        </div>
        <div class="w-full">
          <FloatLabel variant="on" class="w-full">
            <InputText id="name" v-model="name" class="w-full" required="true" />
            <label for="name">Unterziel eingeben</label>
          </FloatLabel>
          <small v-if="errors.name" id="name-help" class="p-error block">{{ errors.name }}</small>
        </div>
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
import { schema } from '@/utils/schemas/ZielUnter'
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
  zielOberId: {
    type: Number,
    default: null
  },
  zielOber: {
    type: Object,
    default: null
  },
  naechsteNr: {
    type: Number,
    default: null
  }
})

const { defineField, handleSubmit, errors, setValues, setFieldValue } = useForm({
  validationSchema: schema
})

const [nr] = defineField('nr')
const [name] = defineField('name')

onMounted(() => {
  if (props.editMode) {
    setValues({
      zielOberId: props.zielOberId,
      nr: props.item.nr,
      name: props.item.name
    })
  } else {
    setFieldValue('zielOberId', props.zielOberId)
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
