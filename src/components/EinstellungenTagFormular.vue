<template>
  <form @submit.prevent="onSubmit">
    <div class="grid grid-cols-1 gap-2 items-center">
      <div class="w-full">
        <FloatLabel variant="on" class="w-full">
          <InputText id="name" v-model="name" class="w-full" :invalid="!!errors.name" />
          <label for="name">Tag eingeben</label>
        </FloatLabel>
        <small v-if="errors.name" id="name-help" class="p-error block">{{ errors.name }}</small>
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
import { schema } from '@/utils/schemas/tag'
import FloatLabel from 'primevue/floatlabel'
import InputText from 'primevue/inputtext'
import ButtonSpeichern from '@/components/ButtonSpeichern.vue'

const props = defineProps({
  editMode: {
    type: Boolean,
    required: true
  },
  item: Object
})

const { defineField, handleSubmit, errors, setValues } = useForm({
  validationSchema: schema
})

const [name] = defineField('name')

onMounted(() => {
  if (props.editMode) {
    setValues({
      name: props.item.name
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
