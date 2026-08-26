<template>
  <div class="flex items-start justify-center pt-12 px-4">
    <div class="w-full max-w-md">
      <BaseAlert
        v-show="sessionExpired"
        type="warning"
        title="Sitzung abgelaufen"
        message="Ihre Sitzung ist abgelaufen. Bitte melden Sie sich erneut an."
        class="mb-4"
      />

      <BaseCard class="p-2">
        <div class="text-center mb-8">
          <AuthLogoLeiste />
          <h1 class="text-xl font-bold text-gray-800 my-0 ">Mobilitätscheck</h1>
          <p class="text-sm text-gray-500">für Magistratsvorlagen</p>
        </div>

        <h2 class="text-lg font-semibold text-gray-700 mb-5">Anmelden</h2>

        <BaseAlert
          v-show="loginFailed"
          type="warning"
          title="Anmeldung fehlgeschlagen"
          message="E-Mail oder Passwort falsch. Bitte überprüfen Sie Ihre Angaben."
          class="mb-4"
        />

        <BaseSpinner v-if="isLoading" />
        <form v-else @submit.prevent="onSubmit" class="grid grid-cols-1 gap-y-4">
          <div class="field">
            <FloatLabel variant="on">
              <InputText id="email" v-model="email" class="w-full" autocomplete="email" />
              <label for="email">E-Mail</label>
            </FloatLabel>
          </div>
          <div class="field">
            <FloatLabel variant="on">
              <Password
                id="password"
                class="w-full"
                inputClass="w-full"
                v-model="password"
                toggleMask
                :feedback="false"
                autocomplete="current-password"
              />
              <label for="password">Passwort</label>
            </FloatLabel>
          </div>
          <Button label="Anmelden" type="submit" class="w-full mt-1" :loading="isLoading" />
        </form>

        <div class="border-t border-gray-100 mt-6 pt-4 grid grid-cols-1 gap-y-2 text-sm">
          <RouterLink class="text-blue-600 hover:underline" :to="{ name: 'passwort-vergessen' }">
            Passwort vergessen?
          </RouterLink>
          <RouterLink class="text-blue-600 hover:underline" :to="{ name: 'registrieren' }">
            Noch kein Konto? Hier registrieren
          </RouterLink>
        </div>
      </BaseCard>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useRoute } from 'vue-router'
import { useForm } from 'vee-validate'
import InputText from 'primevue/inputtext'
import FloatLabel from 'primevue/floatlabel'
import Password from 'primevue/password'
import Button from 'primevue/button'
import AuthLogoLeiste from '@/components/AuthLogoLeiste.vue'

const isLoading = ref(false)

const { defineField, handleSubmit } = useForm()

const [email] = defineField('email')
const [password] = defineField('password')

const route = useRoute()

const sessionExpired = computed(() => route.query.redirect === 'sessionExpired')

const { login } = useAuthStore()
const loginFailed = ref(false)

const onSubmit = handleSubmit(async (values) => {
  try {
    isLoading.value = true
    await login(values)
    loginFailed.value = false
  } catch {
    loginFailed.value = true
  } finally {
    isLoading.value = false
  }
})
</script>

<style scoped>
.p-error {
  @apply text-red-600 text-sm;
}
</style>
