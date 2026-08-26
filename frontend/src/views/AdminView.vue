<template>
  <div>
    <div class="grid grid-cols-8 gap-x-2 grid-flow-col">
      <div class="container col-span-2 w-fit mt-10">
        <Menu :model="items" class="w-fit">
          <template #item="{ item, props }">
            <router-link v-if="item.route" v-slot="{ href, navigate }" :to="item.route" custom>
              <a :href="href" v-bind="props.action" @click="navigate">
                <span :class="item.icon" />
                <span class="ml-2">{{ item.label }}</span>
              </a>
            </router-link>
          </template>
        </Menu>
      </div>
      <div class="container col-span-6">
        <BaseHeading>Administration</BaseHeading>
        <Router-View />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import Menu from 'primevue/menu'

const items = ref([
  {
    label: 'Benutzerverwaltung',
    items: [
      { label: 'Kommunen', icon: 'pi pi-building', route: '/admin/kommunen' },
      { label: 'Benutzer', icon: 'pi pi-users', route: '/admin/benutzer' },
      { label: 'Einladungen', icon: 'pi pi-user-plus', route: '/admin/einladungen' }
    ]
  },
  {
    label: 'Inhalte',
    items: [
      { label: 'Startseite', icon: 'pi pi-home', route: '/admin/startseite' },
      { label: 'Über das Tool', icon: 'pi pi-info-circle', route: '/admin/ueber-das-tool' },
      { label: 'Impressum', icon: 'pi pi-file', route: '/admin/impressum' },
      { label: 'Datenschutz', icon: 'pi pi-shield', route: '/admin/datenschutz' },
      { label: 'Nutzungsbedingungen', icon: 'pi pi-file-edit', route: '/admin/nutzungsbedingungen' },
      { label: 'E-Mail-Vorlagen', icon: 'pi pi-envelope', route: '/admin/email-vorlagen' }
    ]
  },
  {
    label: 'Design',
    items: [{ label: 'Branding', icon: 'pi pi-palette', route: '/admin/branding' }]
  }
])
</script>
