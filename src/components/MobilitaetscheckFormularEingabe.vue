<template>
  <div>
    <BaseSpinner v-if="isLoading" />
    <form v-else class="grid grid-cols-1 gap-y-4 my-7" @submit.prevent="onSubmit">
      <div class="form-group field">
        <FloatLabel variant="on">
          <InputText
            id="name"
            v-model="name"
            aria-describedby="name-help"
            :invalid="!!errors.name"
            class="w-full"
            inputClass="w-full"
          />
          <label for="name">Name des Mobilitätschecks</label>
        </FloatLabel>
        <small v-if="errors.name" id="name-help" class="p-error block">{{ errors.name }}</small>
      </div>
      <div class="flex justify-end w-full">
        <ButtonSpeichern type="submit">Mobilitätscheck anlegen</ButtonSpeichern>
      </div>
    </form>
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useForm } from 'vee-validate'
import { schema } from '@/utils/schemas/mobilitaetscheckEingabe'
import { toTypedSchema } from '@vee-validate/yup'
import { createItem } from '@/composables/crud'
import InputText from 'primevue/inputtext'
import FloatLabel from 'primevue/floatlabel'
import ButtonSpeichern from '@/components/ButtonSpeichern.vue'

const route = useRoute()
const router = useRouter()
const isLoading = ref(false)

const { defineField, handleSubmit, errors, setFieldValue } = useForm({
  validationSchema: toTypedSchema(schema)
})

const [name] = defineField('name')

setFieldValue('magistratsvorlageId', route.params.id)

onMounted(async () => {})

const onSubmit = handleSubmit(async (values) => {
  isLoading.value = true
  const response = await createItem({
    model: 'mobilitaetscheck/eingabe',
    values: values,
    detail: {
      success: 'Mobilitätscheck erfolgreich erstellt',
      error: 'Fehler beim Erstellen des Mobilitätschecks'
    }
  })

  router.replace({
    name: 'mobilitaetscheck-ziele-neu',
    params: { id: route.params.id, checkId: response.id }
  })
  isLoading.value = false
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
