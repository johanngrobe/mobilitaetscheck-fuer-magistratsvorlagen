<template>
  <div class="max-w-6xl">
    <div class="grid grid-cols-2 w-full items-center">
      <BaseHeading>Neuer Mobilitätscheck</BaseHeading>
      <div class="flex w-full justify-end">
        <ButtonZuruecksetzen @click="refreshPage()">zurücksetzen</ButtonZuruecksetzen>
      </div>
    </div>
    <div v-if="isLoading">
      <BaseSpinner />
    </div>
    <div v-else>
      <MobilitaetscheckFormularEingabeZielOber :item="eingabeZielOber" />
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { fetchItem } from '@/composables/crud'
import ButtonZuruecksetzen from '@/components/ButtonZuruecksetzen.vue'
import { useRoute, useRouter } from 'vue-router'
import MobilitaetscheckFormularEingabeZielOber from '@/components/MobilitaetscheckFormularEingabeZielOber.vue'
import BaseSpinner from '@/components/BaseSpinner.vue'

const route = useRoute()
const router = useRouter()

const eingabeZielOber = ref({})
const isLoading = ref(false)

const fetchEingabeZielOber = async () => {
  isLoading.value = true
  const checkId = route.params.checkId
  if (checkId) {
    eingabeZielOber.value = await fetchItem(`/mobilitaetscheck/eingabe/${checkId}`)
  }
  isLoading.value = false
}

onMounted(async () => {
  await fetchEingabeZielOber()
})

const refreshPage = () => {
  router.go() // Reloads the current route
}
</script>

<style></style>
