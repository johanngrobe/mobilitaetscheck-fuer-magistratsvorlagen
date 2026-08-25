<template>
  <BaseSpinner v-if="isLoadingInvite" />
  <div v-else-if="inviteError" class="text-center py-4">
    <div class="flex justify-center mb-4">
      <div class="w-14 h-14 rounded-full bg-red-100 flex items-center justify-center">
        <i class="pi pi-times-circle text-red-500" style="font-size: 1.75rem" />
      </div>
    </div>
    <p class="font-semibold text-gray-800 mb-1">Einladung ungültig</p>
    <p class="text-sm text-gray-500">{{ inviteError }}</p>
  </div>
  <form v-else @submit.prevent="onSubmit" class="grid grid-cols-1 gap-y-4">
    <div class="bg-gray-50 rounded-lg p-3 grid grid-cols-1 gap-y-1 text-sm">
      <div class="flex gap-2">
        <span class="text-gray-500 w-24 shrink-0">E-Mail</span>
        <span class="font-medium break-all">{{ inviteData.email }}</span>
      </div>
      <div class="flex gap-2">
        <span class="text-gray-500 w-24 shrink-0">Kommune</span>
        <span class="font-medium">{{ inviteData.gemeindeName }}</span>
      </div>
      <div class="flex gap-2">
        <span class="text-gray-500 w-24 shrink-0">Rolle</span>
        <span class="font-medium">{{ inviteData.rolleName }}</span>
      </div>
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

    <div v-if="gruppenOptionen.length > 0" class="field">
      <FloatLabel variant="on">
        <Select
          id="gruppeId"
          v-model="gruppeId"
          :options="gruppenOptionen"
          optionLabel="name"
          optionValue="id"
          class="w-full"
          showClear
        />
        <label for="gruppeId">{{ gruppeLabel }}</label>
      </FloatLabel>
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

    <Button label="Registrieren" type="submit" class="w-full" :loading="isSubmitting" />
  </form>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useRouter, useRoute } from 'vue-router'
import { useForm } from 'vee-validate'
import { schema } from '@/utils/schemas/authRegistrierenEinladung'
import Button from 'primevue/button'
import InputText from 'primevue/inputtext'
import FloatLabel from 'primevue/floatlabel'
import Password from 'primevue/password'
import Divider from 'primevue/divider'
import Select from 'primevue/select'
import DatenschutzZustimmung from '@/components/DatenschutzZustimmung.vue'
import { apiClient } from '@/services/axios'
import { useToast } from 'primevue/usetoast'

const isLoadingInvite = ref(true)
const isSubmitting = ref(false)
const inviteError = ref(null)
const inviteData = ref({})
const gruppenOptionen = ref([])
const gruppeId = ref(null)

const gruppeLabel = computed(() =>
  inviteData.value.rolleName === 'Politik' ? 'Fraktion / Partei (optional)' : 'Gruppe (optional)'
)

const toast = useToast()
const route = useRoute()
const router = useRouter()
const { register } = useAuthStore()

const token = route.query.token

const { defineField, handleSubmit, errors } = useForm({ validationSchema: schema })

const [vorname] = defineField('vorname')
const [nachname] = defineField('nachname')
const [password] = defineField('password')
const [confirmPassword] = defineField('confirmPassword')
const [datenschutzAkzeptiert] = defineField('datenschutzAkzeptiert')

onMounted(async () => {
  if (!token) {
    inviteError.value = 'Kein Einladungstoken gefunden.'
    isLoadingInvite.value = false
    return
  }
  try {
    const response = await apiClient.get(`/public/einladung/${token}`)
    inviteData.value = response.data
    const gruppenRes = await apiClient.get('/public/gruppen', {
      params: { gemeinde_id: response.data.gemeindeId, rolle_id: response.data.rolleId }
    })
    gruppenOptionen.value = gruppenRes.data
  } catch {
    inviteError.value = 'Der Einladungslink ist ungültig oder abgelaufen.'
  } finally {
    isLoadingInvite.value = false
  }
})

const onSubmit = handleSubmit(async (values) => {
  isSubmitting.value = true
  try {
    await register({
      vorname: values.vorname,
      nachname: values.nachname,
      email: inviteData.value.email,
      password: values.password,
      gemeindeId: inviteData.value.gemeindeId,
      rolleId: inviteData.value.rolleId,
      gruppeId: gruppeId.value ?? undefined,
      einladungs_token: token
    })
    router.replace({
      name: 'account-bestaetigen',
      query: { verify: 'check-mail', email: inviteData.value.email }
    })
  } catch {
    toast.add({
      severity: 'error',
      summary: 'Fehler',
      detail: 'Registrierung fehlgeschlagen',
      life: 3000
    })
  } finally {
    isSubmitting.value = false
  }
})
</script>

<style scoped>
.p-error {
  @apply text-red-600;
}
</style>
