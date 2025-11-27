<template>
  <div>
    <div class="flex items-center gap-5">
      <BaseSubheading>Klimachecks</BaseSubheading>
      <RouterLink :to="`${route.fullPath}/neu`">
        <Button
          v-tooltip="'Klimacheck hinzufügen'"
          icon="pi pi-plus"
          rounded
          aria-label="Klimacheck hinzufügen"
        />
      </RouterLink>
    </div>
    <KlimacheckListe />
  </div>
</template>

<script setup>
import { useRoute } from 'vue-router'
import KlimacheckListe from '@/components/KlimacheckListe.vue'
import Button from 'primevue/button'

const route = useRoute()
</script>

<style></style>
