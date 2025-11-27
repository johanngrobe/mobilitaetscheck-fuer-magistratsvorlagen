<template>
  <div class="mx-auto p-6">
    <div class="flex items-center gap-5">
      <BaseHeading>Magistratsvorlagen</BaseHeading>
      <RouterLink :to="{ name: 'magistratsvorlage-neu' }">
        <Button
          v-tooltip="'Neue Magistratsvorlage anlegen'"
          icon="pi pi-plus"
          rounded
          aria-label="Neue Magistratsvorlage anlegen"
        />
      </RouterLink>
    </div>
    <MagistrasvorlageListe />
  </div>
</template>

<script setup>
import MagistrasvorlageListe from '@/components/MagistrasvorlageListe.vue'
import Button from 'primevue/button'
</script>

<style></style>
