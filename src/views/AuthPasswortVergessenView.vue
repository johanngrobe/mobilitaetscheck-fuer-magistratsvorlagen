<template>
  <BaseCard class="block mx-auto my-7 max-w-md">
    <h4 class="text-xl font-bold dark:text-white mb-5">Passwort vergessen?</h4>
    <BaseSpinner v-if="isLoading" />
    <div v-else>
      <form v-if="!submit" @submit.prevent="onSubmit">
        <div class="field">
          <FloatLabel variant="on">
            <InputText
              id="email"
              v-model="email"
              class="w-full"
              :invalid="!!errors.email"
              aria-describedby="email-help"
            />
            <label for="email">E-Mail</label>
          </FloatLabel>
          <small v-if="errors.email" class="p-error">{{ errors.email }}</small>
        </div>
        <div class="flex justify-end mt-2">
          <Button label="Passwort zurücksetzen" type="submit" class="w-full" />
        </div>
      </form>
      <div v-else>
        <p>Prüfen SIe ihre E-Mails und klicken Sie den Link zum Zurücksetzen des Passworts.</p>
      </div>
    </div>
  </BaseCard>
</template>

<script setup>
import { ref } from 'vue'
import InputText from 'primevue/inputtext'
import { useAuthStore } from '@/stores/auth'
import * as yup from 'yup'
import { useForm } from 'vee-validate'
import { useToast } from 'primevue/usetoast'
import Button from 'primevue/button'
import FloatLabel from 'primevue/floatlabel'

const isLoading = ref(false)
const submit = ref(false)

const { forgotPassword } = useAuthStore()

const schema = yup.object({
  email: yup
    .string()
    .required('E-Mail ist erforderlich')
    .email('Ungültige E-Mail-Adresse')
    .label('E-Mail')
})

const { defineField, handleSubmit, errors } = useForm({
  validationSchema: schema
})

const [email] = defineField('email')

const toast = useToast()

const onSubmit = handleSubmit(async (values) => {
  try {
    isLoading.value = true
    await forgotPassword(values.email)
    isLoading.value = false
    submit.value = true
  } catch (error) {
    toast.add({ severity: 'error', summary: 'Fehler', detail: 'E-Mail nicht gefunden', life: 3000 })
  }
})
</script>

<style scoped>
.p-invalid {
  @apply border-red-600;
}

.p-error {
  @apply text-red-600;
}
</style>
