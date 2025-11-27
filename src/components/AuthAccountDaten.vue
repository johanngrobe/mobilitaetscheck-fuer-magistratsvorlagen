<template>
  <BaseCard>
    <!-- block my-5 mx-auto max-w-md -->
    <h4 class="text-xl font-bold dark:text-white mb-4">Benutzerangaben</h4>
    <BaseSpinner v-if="isLoading" />
    <form v-else @submit.prevent="onSubmit" class="grid grid-cols-1 gap-y-4">
      <div class="field">
        <FloatLabel variant="on">
          <InputText
            id="vorname"
            v-model="vorname"
            class="w-full"
            :invalid="!!errors.vorname"
            aria-describedby="vorname-help"
          />
          <label for="vorname">Vorname</label>
        </FloatLabel>
        <small v-if="errors.vorname" id="vorname-help" class="p-error block">{{
          errors.vorname
        }}</small>
      </div>
      <div class="field">
        <FloatLabel variant="on">
          <InputText
            id="nachname"
            v-model="nachname"
            class="w-full"
            :invalid="!!errors.nachname"
            aria-describedby="nachname-help"
          />
          <label for="nachname">Nachname</label>
        </FloatLabel>
        <small v-if="errors.nachname" id="nachname-help" class="p-error block">{{
          errors.nachname
        }}</small>
      </div>
      <div class="field">
        <FloatLabel variant="on">
          <Select
            id="gemeinde"
            v-model="gemeindeId"
            :options="gemeindeOptions"
            optionLabel="name"
            optionValue="id"
            class="w-full"
            :invalid="!!errors.gemeinde"
            aria-describedby="gemeinde-help"
            placeholder="Gemeinde auswählen"
            disabled
          />
          <label for="gemeinde">Gemeinde</label>
        </FloatLabel>
        <small v-if="errors.gemeinde" id="gemeinde-help" class="p-error block">{{
          errors.gemeinde
        }}</small>
      </div>
      <div class="field">
        <FloatLabel variant="on">
          <Select
            id="rolleId"
            v-model="rolleId"
            :options="userRolleOptions"
            optionLabel="name"
            optionValue="id"
            class="w-full"
            :invalid="!!errors.rolleId"
            aria-describedby="rolleId-help"
            placeholder="Benutzerrolle auswählen"
          />
          <label for="rolleId">Benutzerrolle</label>
        </FloatLabel>
        <small v-if="errors.rolleId" id="rolleId-help" class="p-error block">{{
          errors.rolleId
        }}</small>
      </div>
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
        <small v-if="errors.email" id="email-help" class="p-error block">{{ errors.email }}</small>
      </div>
      <div class="flex gap-4">
        <ButtonSave type="submit" class="w-full">speichern</ButtonSave>
      </div>
    </form>
  </BaseCard>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { schema } from '@/utils/schemas/accountDaten.js'
import { useForm } from 'vee-validate'
import { useToast } from 'primevue/usetoast'
import FloatLabel from 'primevue/floatlabel'
import InputText from 'primevue/inputtext'
import Select from 'primevue/select'
import { apiClient } from '@/services/axios'
import BaseSpinner from './BaseSpinner.vue'
import ButtonSave from './ButtonSpeichern.vue'

const gemeindeOptions = ref(null)
const userRolleOptions = ref(null)

const { defineField, handleSubmit, errors, setFieldValue } = useForm({
  validationSchema: schema
})

const [email] = defineField('email')
const [vorname] = defineField('vorname')
const [nachname] = defineField('nachname')
const [gemeindeId] = defineField('gemeindeId')
const [rolleId] = defineField('rolleId')

const authStore = useAuthStore()

const setUserValues = async () => {
  const user = await authStore.getUser()

  setFieldValue('email', user.email)
  setFieldValue('vorname', user.vorname)
  setFieldValue('nachname', user.nachname)
  setFieldValue('gemeindeId', user.gemeindeId)
  setFieldValue('rolleId', user.rolleId)
}

const fetchGemeindeOptions = async () => {
  try {
    const response = await apiClient.get('/option/gemeinde')
    gemeindeOptions.value = response.data
  } catch (error) {
    gemeindeOptions.value = []
  }
}

const fetchUserRolleOptions = async () => {
  try {
    const response = await apiClient.get('/option/user-rolle')
    userRolleOptions.value = response.data
  } catch (error) {
    userRolleOptions.value = []
  }
}
onMounted(() => {
  fetchGemeindeOptions()
  fetchUserRolleOptions()
  setUserValues()
})

const toast = useToast()

const onSubmit = handleSubmit(async (values) => {
  try {
    await authStore.updateUser(values)
    toast.add({
      severity: 'success',
      summary: 'Profil erfolgreich aktualisiert',
      life: 3000
    })
  } catch (error) {
    toast.add({
      severity: 'error',
      summary: 'Fehler beim Aktualisieren des Profils',
      life: 3000
    })
  }
})
</script>

<style></style>
