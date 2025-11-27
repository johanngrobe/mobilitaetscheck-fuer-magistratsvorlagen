<template>
  <div>
    <BaseHeading>Meine Datenbank</BaseHeading>

    <BaseTabs :tabs="tabs">
      <template #mobility-check>
        <MobilitySubmissionList :filter="setFilter()" />
      </template>

      <template #climate-check>
        <ClimateSubmissionList :filter="setFilter()" />
      </template>
    </BaseTabs>
  </div>
</template>

<script setup>
import { useAuthStore } from '@/stores/auth'
import BaseTabs from '@/components/BaseTabs.vue'
import MobilitySubmissionList from '@/components/MobilitaetscheckListe.vue'
import ClimateSubmissionList from '@/components/KlimacheckListe.vue'

const authStore = useAuthStore()

const setFilter = () => {
  let filter = {}

  switch (authStore.userRolle) {
    case 'administration':
      filter.userRolle = true
      break
    case 'politician':
      filter.userId = true
      break
  }
  return filter
}

const tabs = [
  { name: 'mobility-check', label: 'Mobilitätscheck', disabled: false },
  { name: 'climate-check', label: 'Klimacheck', disabled: false }
]
</script>

<style></style>
