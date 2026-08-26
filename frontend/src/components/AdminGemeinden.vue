<template>
  <div>
    <BaseCard>
      <div class="flex items-center justify-between mb-4">
        <h5 class="text-lg font-semibold">Kommunen</h5>
        <Button icon="pi pi-plus" label="Neue Kommune" @click="openCreate" />
      </div>

      <InputText v-model="searchQuery" placeholder="Kommune suchen…" class="w-full mb-4" />

      <BaseSpinner v-if="isLoading" />
      <DataTable v-else :value="filteredGemeinden" class="w-full">
        <template #empty>
          <span class="text-gray-400 text-sm">Keine Kommune gefunden.</span>
        </template>
        <Column field="name" header="Name" />
        <Column field="verwaltungEmailDomain" header="E-Mail-Domain">
          <template #body="{ data }">
            <span class="text-gray-500 text-sm">{{
              data.verwaltungEmailDomain ? '@' + data.verwaltungEmailDomain : '–'
            }}</span>
          </template>
        </Column>
        <Column header="" style="width: 100px">
          <template #body="{ data }">
            <div class="flex gap-1">
              <Button
                icon="pi pi-pencil"
                text
                @click="openEdit(data)"
                :disabled="data.name === 'Systemadministration'"
              />
              <Button
                icon="pi pi-trash"
                severity="danger"
                text
                @click="deleteGemeinde(data.id)"
                :disabled="data.name === 'Systemadministration'"
              />
            </div>
          </template>
        </Column>
      </DataTable>
    </BaseCard>

    <!-- Create Dialog -->
    <Dialog
      v-model:visible="createVisible"
      header="Neue Kommune anlegen"
      :modal="true"
      class="w-full max-w-sm"
    >
      <form @submit.prevent="submitCreate" class="mt-2 flex flex-col gap-4">
        <div class="field">
          <FloatLabel variant="on">
            <InputText
              id="newName"
              v-model="createName"
              class="w-full"
              :invalid="!!createErrors.name"
            />
            <label for="newName">Name</label>
          </FloatLabel>
          <small v-if="createErrors.name" class="text-red-600 text-sm block mt-1">{{
            createErrors.name
          }}</small>
        </div>
        <div class="field">
          <label class="block text-sm text-gray-500 mb-1">E-Mail-Domain</label>
          <InputGroup>
            <InputGroupAddon>@</InputGroupAddon>
            <InputText
              id="newDomain"
              v-model="createDomain"
              :invalid="!!createErrors.verwaltungEmailDomain"
              placeholder="oberursel.de"
            />
          </InputGroup>
          <small
            v-if="createErrors.verwaltungEmailDomain"
            class="text-red-600 text-sm block mt-1"
            >{{ createErrors.verwaltungEmailDomain }}</small
          >
        </div>
      </form>
      <template #footer>
        <Button label="Abbrechen" text @click="createVisible = false" />
        <Button label="Anlegen" @click="submitCreate" :loading="isCreating" />
      </template>
    </Dialog>

    <!-- Edit Dialog -->
    <Dialog
      v-model:visible="editVisible"
      header="Kommune bearbeiten"
      :modal="true"
      class="w-full max-w-sm"
    >
      <form @submit.prevent="submitEdit" class="mt-2 flex flex-col gap-4">
        <div class="field">
          <FloatLabel variant="on">
            <InputText
              id="editName"
              v-model="editName"
              class="w-full"
              :invalid="!!editErrors.name"
            />
            <label for="editName">Name</label>
          </FloatLabel>
          <small v-if="editErrors.name" class="text-red-600 text-sm block mt-1">{{
            editErrors.name
          }}</small>
        </div>
        <div class="field">
          <label class="block text-sm text-gray-500 mb-1">E-Mail-Domain</label>
          <InputGroup>
            <InputGroupAddon>@</InputGroupAddon>
            <InputText
              id="editDomain"
              v-model="editDomain"
              :invalid="!!editErrors.verwaltungEmailDomain"
              placeholder="oberursel.de"
            />
          </InputGroup>
          <small v-if="editErrors.verwaltungEmailDomain" class="text-red-600 text-sm block mt-1">{{
            editErrors.verwaltungEmailDomain
          }}</small>
        </div>
      </form>
      <template #footer>
        <Button label="Abbrechen" text @click="editVisible = false" />
        <Button label="Speichern" @click="submitEdit" :loading="isSaving" />
      </template>
    </Dialog>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { onKeyStroke } from '@vueuse/core'
import { useForm } from 'vee-validate'
import * as yup from 'yup'
import Button from 'primevue/button'
import InputText from 'primevue/inputtext'
import FloatLabel from 'primevue/floatlabel'
import InputGroup from 'primevue/inputgroup'
import InputGroupAddon from 'primevue/inputgroupaddon'
import DataTable from 'primevue/datatable'
import Column from 'primevue/column'
import Dialog from 'primevue/dialog'
import { apiClient } from '@/services/axios'
import { useToast } from 'primevue/usetoast'

const gemeindeSchema = yup.object({
  name: yup.string().required('Name ist erforderlich.').label('Name'),
  verwaltungEmailDomain: yup
    .string()
    .nullable()
    .transform((value) => (value === '' ? null : value))
    .matches(/^[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/, {
      message: 'Ungültige Domain (z.B. oberursel.de).',
      excludeEmptyString: true
    })
    .label('E-Mail-Domain')
})

const gemeinden = ref([])
const isLoading = ref(false)
const searchQuery = ref('')

// --- Create form ---
const createVisible = ref(false)
const isCreating = ref(false)

const {
  defineField: defineCreateField,
  handleSubmit: handleCreate,
  errors: createErrors,
  resetForm: resetCreate
} = useForm({ validationSchema: gemeindeSchema })

const [createName] = defineCreateField('name')
const [createDomain] = defineCreateField('verwaltungEmailDomain')

const openCreate = () => {
  resetCreate()
  createVisible.value = true
}

// --- Edit form ---
const editVisible = ref(false)
const editId = ref(null)
const isSaving = ref(false)

const {
  defineField: defineEditField,
  handleSubmit: handleEdit,
  errors: editErrors,
  setValues: setEditValues
} = useForm({ validationSchema: gemeindeSchema })

const [editName] = defineEditField('name')
const [editDomain] = defineEditField('verwaltungEmailDomain')

// ---

const toast = useToast()

onKeyStroke('Enter', (e) => {
  if (createVisible.value) {
    e.preventDefault()
    submitCreate()
  }
  if (editVisible.value) {
    e.preventDefault()
    submitEdit()
  }
})

onKeyStroke('Escape', () => {
  if (createVisible.value) createVisible.value = false
  if (editVisible.value) editVisible.value = false
})

const filteredGemeinden = computed(() => {
  if (!searchQuery.value.trim()) return gemeinden.value
  const q = searchQuery.value.toLowerCase()
  return gemeinden.value.filter((g) => g.name.toLowerCase().includes(q))
})

const fetchGemeinden = async () => {
  isLoading.value = true
  try {
    const res = await apiClient.get('/admin/gemeinde')
    gemeinden.value = res.data
  } catch {
    gemeinden.value = []
  } finally {
    isLoading.value = false
  }
}

onMounted(fetchGemeinden)

const submitCreate = handleCreate(async (values) => {
  isCreating.value = true
  try {
    await apiClient.post('/admin/gemeinde', {
      name: values.name,
      verwaltung_email_domain: values.verwaltungEmailDomain || null
    })
    toast.add({ severity: 'success', summary: 'Kommune angelegt', life: 3000 })
    createVisible.value = false
    await fetchGemeinden()
  } catch {
    toast.add({
      severity: 'error',
      summary: 'Fehler',
      detail: 'Kommune konnte nicht angelegt werden.',
      life: 3000
    })
  } finally {
    isCreating.value = false
  }
})

const openEdit = (gemeinde) => {
  editId.value = gemeinde.id
  setEditValues({
    name: gemeinde.name,
    verwaltungEmailDomain: gemeinde.verwaltungEmailDomain || ''
  })
  editVisible.value = true
}

const submitEdit = handleEdit(async (values) => {
  isSaving.value = true
  try {
    const res = await apiClient.patch(`/admin/gemeinde/${editId.value}`, {
      name: values.name,
      verwaltung_email_domain: values.verwaltungEmailDomain || null
    })
    const idx = gemeinden.value.findIndex((g) => g.id === editId.value)
    if (idx !== -1) gemeinden.value[idx] = res.data
    editVisible.value = false
    toast.add({ severity: 'success', summary: 'Gespeichert', life: 3000 })
  } catch {
    toast.add({
      severity: 'error',
      summary: 'Fehler',
      detail: 'Änderung konnte nicht gespeichert werden.',
      life: 3000
    })
  } finally {
    isSaving.value = false
  }
})

const deleteGemeinde = async (id) => {
  try {
    await apiClient.delete(`/admin/gemeinde/${id}`)
    gemeinden.value = gemeinden.value.filter((g) => g.id !== id)
    toast.add({ severity: 'success', summary: 'Kommune gelöscht', life: 3000 })
  } catch {
    toast.add({
      severity: 'error',
      summary: 'Fehler',
      detail: 'Kommune konnte nicht gelöscht werden.',
      life: 3000
    })
  }
}
</script>

<style scoped>
.field {
  display: flex;
  flex-direction: column;
}
</style>
