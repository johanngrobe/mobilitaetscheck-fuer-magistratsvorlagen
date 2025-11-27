<template>
  <div>
    <BaseCard class="block mx-auto my-7 max-w-md">
      <h4 class="text-xl font-bold dark:text-white">Account bestätigen</h4>
      <div class="mt-4">
        <div v-if="route.query.verify === 'check-mail'">
          <p>Die Registrierung war erfolgreich.</p>
          <p class="font-semibold">
            Bitte überprüfen Sie ihre E-Mails und bestätigen Sie ihren Account.
          </p>
          <p>Dann können Sie das Webtool nutzen.</p>
        </div>
        <div v-if="route.query.verify === 'success'">
          <p class="font-semibold">Ihr Account wurde erfolgreich bestätigt.</p>
          <p>Sie können sich jetzt anmelden.</p>
          <div class="flex justify-end mt-5">
            <Button label="Anmelden" asChild><RouterLink :to="{ name: anmelden }" /></Button>
          </div>
        </div>
      </div>
    </BaseCard>
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { apiClient } from '@/services/axios'
import Button from 'primevue/button'

const route = useRoute()
const router = useRouter()

const verifyToken = async () => {
  const token = route.query.token || null
  if (token) {
    const response = await apiClient.post(`/auth/verify`, { token })
    if (response.status === 200) {
      router.replace({ name: 'account-bestaetigen', query: { verify: 'success' } })
    }
  }
  return false
}

onMounted(async () => {
  await verifyToken()
})
</script>
