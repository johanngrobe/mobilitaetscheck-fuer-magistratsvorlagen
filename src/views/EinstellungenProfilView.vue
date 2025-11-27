<template>
  <div>
    <BaseSubheading>Profil</BaseSubheading>

    <AuthAccountDaten />
    <AuthPasswortZuruecksetzen :changePassword="true" />
  </div>
</template>

<script setup>
import AuthAccountDaten from '@/components/AuthAccountDaten.vue'
import AuthPasswortZuruecksetzen from '@/components/AuthPasswortZuruecksetzen.vue'
</script>

<style></style>
