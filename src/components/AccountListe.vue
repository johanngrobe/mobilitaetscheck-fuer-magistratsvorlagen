<template>
  <div>
    <DataTable :value="accounts" removableSort tableStyle="min-width: 50rem">
      <Column field="vorname" header="Vorname" sortable></Column>
      <Column field="nachname" header="Nachname" sortable></Column>
      <Column field="email" header="E-Mail" sortable></Column>
      <Column field="rolleId" header="Rolle" sortable>
        <template #body="{ data }">
          <Select
            v-model="data.rolleId"
            :options="userRolleOptions"
            optionLabel="name"
            optionValue="id"
            class="w-full"
            @change="updateAccount(data.id, { rolleId: data.rolleId })"
          />
        </template>
      </Column>
      <Column field="isSuperuser" header="Admin" sortable>
        <template #body="{ data }">
          <Checkbox
            v-model="data.isSuperuser"
            @change="updateAccount(data.id, { isSuperuser: data.isSuperuser })"
            binary
          />
        </template>
      </Column>
      <Column field="erstelltAm" header="erstellt am" sortable>
        <template #body="{ data }">
          {{ new Date(data.erstelltAm).toLocaleDateString('de-DE') }}
        </template>
      </Column>
    </DataTable>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { fetchItems, updateItem } from '@/composables/crud'
import DataTable from 'primevue/datatable'
import Column from 'primevue/column'
import Select from 'primevue/select'
import Checkbox from 'primevue/checkbox'

const accounts = ref([])
const userRolleOptions = ref([])

onMounted(() => {
  fetchAccountListe()
  fetchUserRolleOptions()
})

const fetchAccountListe = async () => {
  accounts.value = await fetchItems('/users')
}

const fetchUserRolleOptions = async () => {
  userRolleOptions.value = await fetchItems('/option/user-rolle')
}

const updateAccount = async (id, values) => {
  await updateItem({
    model: 'users',
    modelId: id,
    values,
    detail: {
      success: 'Account erfolgreich aktualisiert',
      error: 'Fehler beim Aktualisieren des Accounts'
    }
  })
}
</script>

<style></style>
