<template>
  <div>
    <BaseCard class="grid grid-cols-1 block mx-auto my-5 max-w-md gap-y-4">
      <h4 class="text-xl font-bold dark:text-white mb-5">Registrieren</h4>
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
              :invalid="!!errors.gemeindeId"
              aria-describedby="gemeindeId-help"
            />
            <label for="gemeinde">Gemeinde</label>
          </FloatLabel>
          <small v-if="errors.gemeindeId" id="gemeindeId-help" class="p-error block">{{
            errors.gemeindeId
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
              aria-describedby="rolle-help"
            />
            <label for="rolle">Benutzerrolle</label>
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
          <small v-if="errors.email" id="email-help" class="p-error block">{{
            errors.email
          }}</small>
        </div>

        <div class="field">
          <FloatLabel variant="on">
            <Password
              id="password"
              class="w-full"
              inputClass="w-full"
              v-model="password"
              promptLabel="Mindestanforderungen:"
              toggleMask
              :invalid="!!errors.password"
              aria-describedby="password-help"
            >
              <template #header>
                <h5 class="text-lg font-bold">Passwortstärke</h5>
              </template>
              <template #footer>
                <Divider />
                <ul class="pl-2 ml-2 my-0 leading-normal list-disc">
                  <li>Mindestens einen Kleinbuchstaben</li>
                  <li>Mindestens einen Großbuchstaben</li>
                  <li>Mindestens eine Ziffer</li>
                  <li>Mindestens ein Sonderzeichen</li>
                  <li>Mindestens 8 Zeichen</li>
                </ul>
              </template>
            </Password>
            <label for="password">Passwort</label>
          </FloatLabel>
          <small v-if="errors.password" id="password-help" class="p-error block">{{
            errors.password
          }}</small>
        </div>

        <div class="field">
          <FloatLabel variant="on">
            <Password
              id="confirmPassword"
              class="w-full"
              inputClass="w-full"
              v-model="confirmPassword"
              toggleMask
              :feedback="false"
              :invalid="!!errors.confirmPassword"
              aria-describedby="confirmPassword-help"
            />
            <label for="confirmPassword">Passwort wiederholen</label>
          </FloatLabel>
          <small v-if="errors.confirmPassword" id="confirmPassword-help" class="p-error block">{{
            errors.confirmPassword
          }}</small>
        </div>
        <Button label="Registrieren" type="submit" class="w-full" />
      </form>
    </BaseCard>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useRouter } from 'vue-router'
import { useForm } from 'vee-validate'
import { schema } from '@/utils/schemas/authRegistrieren'
import Button from 'primevue/button'
import InputText from 'primevue/inputtext'
import FloatLabel from 'primevue/floatlabel'
import Password from 'primevue/password'
import Select from 'primevue/select'
import { apiClient } from '@/services/axios'
import { useToast } from 'primevue/usetoast'

const isLoading = ref(false)
const gemeindeOptions = ref(null)
const userRolleOptions = ref(null)

const toast = useToast()

// Validation schema

// Form setup
const { defineField, handleSubmit, errors } = useForm({
  validationSchema: schema
})

const [vorname] = defineField('vorname')
const [nachname] = defineField('nachname')
const [rolleId] = defineField('rolleId')
const [gemeindeId] = defineField('gemeindeId')
const [email] = defineField('email')
const [password] = defineField('password')
const [confirmPassword] = defineField('confirmPassword')

const router = useRouter()
const { register } = useAuthStore()

const fetchMunicipalityOptions = async () => {
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
  fetchMunicipalityOptions()
  fetchUserRolleOptions()
})

const onSubmit = handleSubmit(async (values) => {
  try {
    isLoading.value = true
    await register(values)
    router.replace({ name: 'account-bestaetigen', query: { verify: 'check-mail' } })
  } catch (error) {
    console.log(error)
    toast.add({
      severity: 'error',
      summary: 'Fehler',
      detail: 'Registrierung fehlgeschlagen',
      life: 3000
    })
  }
  isLoading.value = false
})
</script>

<style scoped>
.p-button {
  text-decoration: none;
}

.p-invalid {
  @apply border-red-600;
}

.p-error {
  @apply text-red-600;
}
</style>
