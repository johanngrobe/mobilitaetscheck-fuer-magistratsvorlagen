<template>
  <Toolbar style="border-radius: 0.5rem; background-color: #193b4d" class="w-full">
    <template #start>
      <div class="flex items-center gap-2 text-white">
        <router-link
          :to="{ name: 'startseite' }"
          class="grid grid-cols-1 items-center justify-center justify-items-center menuItem-active-link"
        >
          <div class="font-bold text-lg flex items-center">Mobilitätscheck</div>
          <div class="font-bold text-xs">für Magistratsvorlagen</div>
        </router-link>
      </div>
    </template>
    <template #center>
      <div v-if="authStore.isLoggedIn">
        <router-link :to="{ name: 'magistratsvorlage-liste' }">
          <Button label="Magistratsvorlagen" />
        </router-link>
      </div>
    </template>

    <template #end>
      <div v-if="authStore.isLoggedIn" class="flex items-center gap-2">
        <router-link v-if="[1].includes(authStore.userRolleId)" :to="{ name: 'leitziel' }">
          <Button v-tooltip.left="'Einstellungen'" icon="pi pi-cog" />
        </router-link>

        <Avatar
          v-tooltip.right="'Profil und Abmelden'"
          :label="authStore.userInitialien"
          shape="circle"
          @click="toggle"
        />

        <Popover ref="op">
          <div class="flex flex-col gap-4 w-[8rem]">
            <router-link v-if="[1].includes(authStore.userRolleId)" :to="{ name: 'profil' }">
              <Button icon="pi pi-user" label="Profil" class="w-full" text plain />
            </router-link>
            <Button
              icon="pi pi-sign-out"
              label="Abmelden"
              class="w-full"
              @click="authStore.logout"
            />
          </div>
        </Popover>
      </div>
      <div v-else class="flex items-center gap-2">
        <router-link :to="{ name: 'anmelden' }">
          <Button label="Anmelden" icon="pi pi-sign-in" />
        </router-link>
      </div>
    </template>
  </Toolbar>
</template>

<script setup>
import { ref } from 'vue'
import { useAuthStore } from '@/stores/auth'
import Avatar from 'primevue/avatar'
import Button from 'primevue/button'
import Toolbar from 'primevue/toolbar'
import Popover from 'primevue/popover'

const authStore = useAuthStore()

const op = ref()

const toggle = (event) => {
  op.value.toggle(event)
}
</script>

<style scoped>
.router-link-exact-active.menuItem-active-link {
  @apply text-white;
}
.router-link-active,
.router-link-exact-active {
  @apply block py-2 px-3 text-white bg-blue-700 rounded md:bg-transparent md:text-blue-700 md:p-0 dark:text-white md:dark:text-blue-500;
}
</style>
