<template>
  <div ref="sidebarContainer">
    <!-- Button to toggle sidebar -->
    <button
      @click="toggleSidebar"
      aria-controls="logo-sidebar"
      type="button"
      class="inline-flex items-center p-2 mt-2 ms-3 text-sm text-gray-500 rounded-lg sm:hidden hover:bg-gray-100 focus:outline-none focus:ring-2 focus:ring-gray-200 dark:text-gray-400 dark:hover:bg-gray-700 dark:focus:ring-gray-600"
    >
      <span class="sr-only">Open sidebar</span>
      <svg
        class="w-6 h-6"
        aria-hidden="true"
        fill="currentColor"
        viewBox="0 0 20 20"
        xmlns="http://www.w3.org/2000/svg"
      >
        <path
          clip-rule="evenodd"
          fill-rule="evenodd"
          d="M2 4.75A.75.75 0 012.75 4h14.5a.75.75 0 010 1.5H2.75A.75.75 0 012 4.75zm0 10.5a.75.75 0 01.75-.75h7.5a.75.75 0 010 1.5h-7.5a.75.75 0 01-.75-.75zM2 10a.75.75 0 01.75-.75h14.5a.75.75 0 010 1.5H2.75A.75.75 0 012 10z"
        ></path>
      </svg>
    </button>

    <!-- Sidebar -->
    <aside
      :class="{ '-translate-x-full': !isSidebarOpen, 'translate-x-0': isSidebarOpen }"
      id="logo-sidebar"
      class="fixed top-0 left-0 z-40 w-64 h-screen transition-transform bg-gray-50 dark:bg-gray-800 sm:translate-x-0"
      aria-label="Sidebar"
    >
      <div class="h-full px-3 py-4 overflow-y-auto">
        <RouterLink to="/" class="flex items-center ps-2.5 mb-5">
          <img src="../assets/pimoo_3logos.png" class="h-6 me-3 sm:h-7" alt="pimoo Logos" />
          <!-- <span class="self-center text-xl font-semibold whitespace-nowrap dark:text-white">pimoo</span> -->
        </RouterLink>
        <ul class="space-y-2 font-medium">
          <li v-for="item in filteredMenuItems" :key="item.name">
            <RouterLink
              :to="item.link"
              class="flex items-center p-2 text-gray-900 rounded-lg dark:text-white hover:bg-gray-100 dark:hover:bg-gray-700 group"
              active-class="bg-gray-200 dark:bg-gray-700"
            >
              <img
                v-if="item.icon"
                :src="getIconPath(item.icon)"
                class="w-5 h-5 text-gray-500 transition duration-75 dark:text-gray-400 group-hover:text-gray-900 dark:group-hover:text-white"
                aria-hidden="true"
                alt=""
              />
              <span class="ms-3">{{ item.name }}</span>
            </RouterLink>
          </li>
        </ul>
        <transition>
          <div v-if="authStore.isLoggedIn">
            <div class="border-t-2 border-gray-200 dark:border-gray-700 my-2"></div>
            <ul class="space-y-2 font-medium">
              <li v-for="item in filteredAuthMenuItems" :key="item.name">
                <RouterLink
                  :to="item.link"
                  class="flex items-center p-2 text-gray-900 rounded-lg dark:text-white hover:bg-gray-100 dark:hover:bg-gray-700 group"
                  active-class="bg-gray-200 dark:bg-gray-700"
                >
                  <img
                    v-if="item.icon"
                    :src="getIconPath(item.icon)"
                    class="w-5 h-5 text-gray-500 transition duration-75 dark:text-gray-400 group-hover:text-gray-900 dark:group-hover:text-white"
                    aria-hidden="true"
                    alt=""
                  />
                  <span class="ms-3">{{ item.name }}</span>
                </RouterLink>
              </li>
              <div class="border-t-2 border-gray-200 dark:border-gray-700 my-2"></div>
              <li key="logout">
                <div
                  @click="handleLogout"
                  class="flex items-center p-2 text-gray-900 rounded-lg dark:text-white hover:bg-gray-100 dark:hover:bg-gray-700 group"
                >
                  <img
                    v-if="itemLogout.icon"
                    :src="getIconPath(itemLogout.icon)"
                    class="w-5 h-5 text-gray-500 transition duration-75 dark:text-gray-400 group-hover:text-gray-900 dark:group-hover:text-white"
                    aria-hidden="true"
                    alt=""
                  />
                  <span class="ms-3">{{ itemLogout.name }}</span>
                </div>
              </li>
            </ul>
          </div>
        </transition>
      </div>
    </aside>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRouter, RouterLink } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { onClickOutside } from '@vueuse/core'

const router = useRouter()
const authStore = useAuthStore()

const isSidebarOpen = ref(false)
const sidebarContainer = ref(null)

const toggleSidebar = () => {
  isSidebarOpen.value = !isSidebarOpen.value
}

// Simulate authentication status
// const isLoggedIn = ref(true)

// Define menu items
const menuItems = ref([
  {
    name: 'Startseite',
    link: '/',
    icon: 'MaterialSymbolsHouse.svg',
    onlyWhenLoggedOut: false
  },
  {
    name: 'Über das Tool',
    link: '/ueber-das-tool',
    icon: 'MaterialSymbolsBookmarkSharp.svg',
    onlyWhenLoggedOut: false
  },
  {
    name: 'Anmelden',
    link: '/auth/anmelden',
    icon: 'MaterialSymbolsLogin.svg',
    onlyWhenLoggedOut: true
  },
  {
    name: 'Registrieren',
    link: '/auth/registrieren',
    icon: 'MaterialSymbolsAdd.svg',
    onlyWhenLoggedOut: true
  }
])

const authMenuItems = ref([
  {
    name: 'Meine Datenbank',
    link: '/datenbank/persoenlich',
    icon: 'MaterialSymbolsHistory.svg',
    requiresAuth: true,
    requiresUserRolleId: [2]
  },
  {
    name: 'Magistratsvorlagen',
    link: '/magistratsvorlage',
    icon: 'MaterialSymbolsFileCopy.svg',
    requiresAuth: true,
    requiresUserRolleId: [1, 2]
  },
  {
    name: 'Einstellungen',
    link: '/einstellungen/leitziel',
    icon: 'MaterialSymbolsSettings.svg',
    requiresAuth: true,
    requiresUserRolleId: [1]
  }
])

const itemLogout = {
  name: 'Abmelden',
  icon: 'MaterialSymbolsLogout.svg'
}

const filteredMenuItems = computed(() => {
  return menuItems.value.filter((item) => {
    if (authStore.isLoggedIn) {
      return !item.onlyWhenLoggedOut
    } else {
      return item.onlyWhenLoggedOut || !item.onlyWhenLoggedOut
    }
  })
})

const filteredAuthMenuItems = computed(() => {
  return authMenuItems.value.filter((item) => {
    if (authStore.isLoggedIn) {
      return item.requiresAuth && item.requiresUserRolleId.includes(authStore.userRolleId)
    } else {
      return !item.requiresAuth
    }
  })
})

const getIconPath = (icon) => {
  return new URL(`/src/assets/icons/${icon}`, import.meta.url).href
}

onClickOutside(sidebarContainer, () => {
  isSidebarOpen.value = false
})

const handleLogout = () => {
  authStore.logout()
  router.replace({ name: 'startseite' })
}
</script>

<style scoped>
.v-enter-active,
.v-leave-active {
  transition: opacity 0.5s ease;
}

.v-enter-from,
.v-leave-to {
  opacity: 0;
}
</style>
