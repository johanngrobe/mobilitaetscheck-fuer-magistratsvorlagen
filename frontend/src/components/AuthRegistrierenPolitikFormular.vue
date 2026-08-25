<template>
  <BaseSpinner v-if="isLoading" />
  <form v-else @submit.prevent="onSubmit" class="grid grid-cols-1 gap-y-4">
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
        <label for="gemeinde">Kommune</label>
      </FloatLabel>
      <small v-if="errors.gemeindeId" id="gemeindeId-help" class="p-error block">{{
        errors.gemeindeId
      }}</small>
    </div>

    <div class="field">
      <FloatLabel variant="on">
        <Select
          id="gruppeId"
          v-model="gruppeId"
          :options="gruppenOptionen"
          optionLabel="name"
          optionValue="id"
          class="w-full"
          :disabled="!gemeindeId"
          showClear
        />
        <label for="gruppeId">Fraktion / Partei (optional)</label>
      </FloatLabel>
    </div>

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

    <DatenschutzZustimmung v-model="datenschutzAkzeptiert" :error-message="errors.datenschutzAkzeptiert" />

    <Button label="Registrieren" type="submit" class="w-full" />
  </form>
</template>

<script setup>
import { ref, watch, onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useRouter } from 'vue-router'
import { useForm } from 'vee-validate'
import { schema } from '@/utils/schemas/authRegistrieren'
import Button from 'primevue/button'
import InputText from 'primevue/inputtext'
import FloatLabel from 'primevue/floatlabel'
import Password from 'primevue/password'
import Divider from 'primevue/divider'
import Select from 'primevue/select'
import DatenschutzZustimmung from '@/components/DatenschutzZustimmung.vue'
import { apiClient } from '@/services/axios'
import { useToast } from 'primevue/usetoast'

const isLoading = ref(false)
const gemeindeOptions = ref([])
const gruppenOptionen = ref([])
const gruppeId = ref(null)
const politikRolleId = ref(null)

const toast = useToast()
const router = useRouter()
const { register } = useAuthStore()

const { defineField, handleSubmit, errors } = useForm({ validationSchema: schema })

const [vorname] = defineField('vorname')
const [nachname] = defineField('nachname')
const [gemeindeId] = defineField('gemeindeId')
const [email] = defineField('email')
const [password] = defineField('password')
const [confirmPassword] = defineField('confirmPassword')
const [datenschutzAkzeptiert] = defineField('datenschutzAkzeptiert')

onMounted(async () => {
  try {
    const [gemeindeRes, rollenRes] = await Promise.all([
      apiClient.get('/option/gemeinde'),
      apiClient.get('/option/user-rolle')
    ])
    gemeindeOptions.value = gemeindeRes.data
    politikRolleId.value = rollenRes.data.find((r) => r.name === 'Politik')?.id ?? null
  } catch {
    gemeindeOptions.value = []
  }
})

watch(gemeindeId, async (newId) => {
  gruppeId.value = null
  gruppenOptionen.value = []
  if (!newId || !politikRolleId.value) return
  try {
    const res = await apiClient.get('/public/gruppen', {
      params: { gemeinde_id: newId, rolle_id: politikRolleId.value }
    })
    gruppenOptionen.value = res.data
  } catch {
    gruppenOptionen.value = []
  }
})

const onSubmit = handleSubmit(async (values) => {
  try {
    isLoading.value = true
    // eslint-disable-next-line no-unused-vars
    const { datenschutzAkzeptiert, ...registerValues } = values
    await register({ ...registerValues, rolle_id: 2, gruppeId: gruppeId.value ?? undefined })
    router.replace({
      name: 'account-bestaetigen',
      query: { verify: 'check-mail', email: values.email }
    })
  } catch (error) {
    console.log(error)
    toast.add({
      severity: 'error',
      summary: 'Fehler',
      detail: 'Registrierung fehlgeschlagen',
      life: 3000
    })
  } finally {
    isLoading.value = false
  }
})
</script>

<style scoped>
.p-error {
  @apply text-red-600;
}
</style>
