<template>
  <div class="min-h-screen flex flex-col">
    <div class="max-w-6xl mx-auto p-1 w-full flex-1">
      <TheNavigationsmenuTopbar class="w-full mb-2" />
      <Toast position="bottom-right" />
      <ConfirmDialog />
      <RouterView />
    </div>
    <TheFooter />
  </div>
</template>

<script setup>
import { RouterView } from 'vue-router'
import { useTitle } from '@vueuse/core'
import ConfirmDialog from 'primevue/confirmdialog'
import Toast from 'primevue/toast'
import TheNavigationsmenuTopbar from './components/TheNavigationsmenuTopbar.vue'
import TheFooter from './components/TheFooter.vue'

useTitle('pimoo Mobilitätscheck')
</script>

<style>
.route-enter-from {
  opacity: 0;
  transform: translateY(-30px);
}
.route-leave-to {
  opacity: 0;
  transform: translateY(30px);
}

.route-enter-active {
  transition: all 0.3s ease-out;
}

.route-leave-active {
  transition: all 0.3s ease-in;
}

.route-enter-to,
.route-leave-from {
  opacity: 1;
  transform: translateY(0);
}
</style>
