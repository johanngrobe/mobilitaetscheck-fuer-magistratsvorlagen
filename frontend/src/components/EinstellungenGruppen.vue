<template>
  <div class="flex flex-col gap-4">
    <BaseCard>
      <Tabs :value="activeTab" @update:value="activeTab = $event">
        <TabList>
          <Tab value="verwaltung">Verwaltung</Tab>
          <Tab value="politik">Politik</Tab>
        </TabList>
        <TabPanels>
          <TabPanel value="verwaltung">
            <div class="flex items-center justify-between mb-4 mt-2">
              <h5 class="text-lg font-semibold">Gruppen</h5>
              <Button icon="pi pi-plus" label="Neue Gruppe" @click="openCreate('Verwaltung')" />
            </div>
            <BaseSpinner v-if="isLoading" />
            <DataTable v-else :value="verwaltungGruppen" class="w-full">
              <template #empty>
                <span class="text-gray-400 text-sm">Keine Gruppen vorhanden.</span>
              </template>
              <Column field="name" header="Name" />
              <Column header="" style="width: 100px">
                <template #body="{ data }">
                  <div class="flex gap-1">
                    <Button icon="pi pi-pencil" text @click="openEdit(data)" />
                    <Button icon="pi pi-trash" severity="danger" text @click="deleteGruppe(data.id)" />
                  </div>
                </template>
              </Column>
            </DataTable>

            <div class="border-t border-gray-200 my-4" />
            <h5 class="text-lg font-semibold mb-1">Benutzerzuweisung</h5>
            <p class="text-sm text-gray-500 mb-4">Benutzer per Drag &amp; Drop oder Auswahl zuweisen.</p>
            <BaseSpinner v-if="isLoadingUsers" />
            <div v-else class="flex gap-3 overflow-x-auto pb-4 items-start">
              <div class="w-56 flex-shrink-0 bg-gray-50 rounded-lg p-3">
                <div class="flex items-center gap-2 mb-3">
                  <span class="text-sm font-semibold text-gray-500">Ohne Gruppe</span>
                  <span class="ml-auto text-xs bg-gray-200 text-gray-600 rounded-full px-2 py-0.5">
                    {{ groupUserLists['none-verwaltung']?.length ?? 0 }}
                  </span>
                </div>
                <draggable
                  :list="groupUserLists['none-verwaltung'] ?? []"
                  group="verwaltung-users"
                  item-key="id"
                  handle=".drag-handle"
                  class="min-h-12"
                  @change="onDragChange(null, $event)"
                >
                  <template #item="{ element }">
                    <UserAssignItem
                      :user="element"
                      :options="verwaltungGruppeSelectOptions"
                      @change-gruppe="(v) => onSelectGruppe(element, v)"
                    />
                  </template>
                </draggable>
              </div>
              <div
                v-for="g in verwaltungGruppen"
                :key="g.id"
                class="w-56 flex-shrink-0 bg-gray-50 rounded-lg p-3"
              >
                <div class="flex items-center gap-2 mb-3">
                  <span class="text-sm font-semibold truncate">{{ g.name }}</span>
                  <span class="ml-auto text-xs bg-primary-100 text-primary-700 rounded-full px-2 py-0.5 flex-shrink-0">
                    {{ groupUserLists[g.id]?.length ?? 0 }}
                  </span>
                </div>
                <draggable
                  :list="groupUserLists[g.id] ?? []"
                  group="verwaltung-users"
                  item-key="id"
                  handle=".drag-handle"
                  class="min-h-12"
                  @change="onDragChange(g.id, $event)"
                >
                  <template #item="{ element }">
                    <UserAssignItem
                      :user="element"
                      :options="verwaltungGruppeSelectOptions"
                      @change-gruppe="(v) => onSelectGruppe(element, v)"
                    />
                  </template>
                </draggable>
              </div>
            </div>
          </TabPanel>

          <TabPanel value="politik">
            <div class="flex items-center justify-between mb-4 mt-2">
              <h5 class="text-lg font-semibold">Gruppen</h5>
              <Button icon="pi pi-plus" label="Neue Gruppe" @click="openCreate('Politik')" />
            </div>
            <BaseSpinner v-if="isLoading" />
            <DataTable v-else :value="politikGruppen" class="w-full">
              <template #empty>
                <span class="text-gray-400 text-sm">Keine Gruppen vorhanden.</span>
              </template>
              <Column field="name" header="Name" />
              <Column header="" style="width: 100px">
                <template #body="{ data }">
                  <div class="flex gap-1">
                    <Button icon="pi pi-pencil" text @click="openEdit(data)" />
                    <Button icon="pi pi-trash" severity="danger" text @click="deleteGruppe(data.id)" />
                  </div>
                </template>
              </Column>
            </DataTable>

            <div class="border-t border-gray-200 my-4" />
            <h5 class="text-lg font-semibold mb-1">Benutzerzuweisung</h5>
            <p class="text-sm text-gray-500 mb-4">Benutzer per Drag &amp; Drop oder Auswahl zuweisen.</p>
            <BaseSpinner v-if="isLoadingUsers" />
            <div v-else class="flex gap-3 overflow-x-auto pb-4 items-start">
              <div class="w-56 flex-shrink-0 bg-gray-50 rounded-lg p-3">
                <div class="flex items-center gap-2 mb-3">
                  <span class="text-sm font-semibold text-gray-500">Ohne Gruppe</span>
                  <span class="ml-auto text-xs bg-gray-200 text-gray-600 rounded-full px-2 py-0.5">
                    {{ groupUserLists['none-politik']?.length ?? 0 }}
                  </span>
                </div>
                <draggable
                  :list="groupUserLists['none-politik'] ?? []"
                  group="politik-users"
                  item-key="id"
                  handle=".drag-handle"
                  class="min-h-12"
                  @change="onDragChange(null, $event)"
                >
                  <template #item="{ element }">
                    <UserAssignItem
                      :user="element"
                      :options="politikGruppeSelectOptions"
                      @change-gruppe="(v) => onSelectGruppe(element, v)"
                    />
                  </template>
                </draggable>
              </div>
              <div
                v-for="g in politikGruppen"
                :key="g.id"
                class="w-56 flex-shrink-0 bg-gray-50 rounded-lg p-3"
              >
                <div class="flex items-center gap-2 mb-3">
                  <span class="text-sm font-semibold truncate">{{ g.name }}</span>
                  <span class="ml-auto text-xs bg-primary-100 text-primary-700 rounded-full px-2 py-0.5 flex-shrink-0">
                    {{ groupUserLists[g.id]?.length ?? 0 }}
                  </span>
                </div>
                <draggable
                  :list="groupUserLists[g.id] ?? []"
                  group="politik-users"
                  item-key="id"
                  handle=".drag-handle"
                  class="min-h-12"
                  @change="onDragChange(g.id, $event)"
                >
                  <template #item="{ element }">
                    <UserAssignItem
                      :user="element"
                      :options="politikGruppeSelectOptions"
                      @change-gruppe="(v) => onSelectGruppe(element, v)"
                    />
                  </template>
                </draggable>
              </div>
            </div>
          </TabPanel>
        </TabPanels>
      </Tabs>
    </BaseCard>

    <!-- Create Dialog -->
    <Dialog
      v-model:visible="createVisible"
      header="Neue Gruppe anlegen"
      :modal="true"
      class="w-full max-w-sm"
    >
      <form @submit.prevent="submitCreate" class="mt-2 flex flex-col gap-4">
        <div class="field">
          <FloatLabel variant="on">
            <InputText
              id="createName"
              v-model="createName"
              class="w-full"
              :invalid="!!createErrors.name"
            />
            <label for="createName">Name</label>
          </FloatLabel>
          <small v-if="createErrors.name" class="text-red-600 text-sm block mt-1">{{
            createErrors.name
          }}</small>
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
      header="Gruppe bearbeiten"
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
      </form>
      <template #footer>
        <Button label="Abbrechen" text @click="editVisible = false" />
        <Button label="Speichern" @click="submitEdit" :loading="isSaving" />
      </template>
    </Dialog>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted, watch, defineComponent, h } from 'vue'
import { onKeyStroke } from '@vueuse/core'
import { useForm } from 'vee-validate'
import * as yup from 'yup'
import draggable from 'vuedraggable'
import Button from 'primevue/button'
import InputText from 'primevue/inputtext'
import FloatLabel from 'primevue/floatlabel'
import Select from 'primevue/select'
import DataTable from 'primevue/datatable'
import Column from 'primevue/column'
import Dialog from 'primevue/dialog'
import Tabs from 'primevue/tabs'
import TabList from 'primevue/tablist'
import Tab from 'primevue/tab'
import TabPanels from 'primevue/tabpanels'
import TabPanel from 'primevue/tabpanel'
import { apiClient } from '@/services/axios'
import { useToast } from 'primevue/usetoast'

// --- Inline sub-component for each user item ---
const UserAssignItem = defineComponent({
  props: {
    user: Object,
    options: Array,
  },
  emits: ['change-gruppe'],
  setup(props, { emit }) {
    return () =>
      h('div', { class: 'flex gap-2 bg-white rounded p-2 mb-1 border border-gray-100 shadow-sm' }, [
        h('i', { class: 'pi pi-bars drag-handle text-gray-300 cursor-grab mt-1 flex-shrink-0' }),
        h('div', { class: 'flex-1 min-w-0' }, [
          h('div', { class: 'text-sm font-medium truncate' }, `${props.user.vorname} ${props.user.nachname}`),
          props.user.rolleName ? h('div', { class: 'text-xs text-gray-400' }, props.user.rolleName) : null,
          h(Select, {
            modelValue: props.user.gruppeId ?? null,
            options: props.options,
            optionLabel: 'name',
            optionValue: 'id',
            placeholder: 'Keine Gruppe',
            class: 'w-full mt-1',
            size: 'small',
            'onUpdate:modelValue': (v) => emit('change-gruppe', v),
          }),
        ]),
      ])
  },
})

// ---

const gruppeSchema = yup.object({
  name: yup.string().required('Name ist erforderlich.').label('Name'),
})

const activeTab = ref('verwaltung')

const gruppen = ref([])
const verwaltungGruppen = computed(() => gruppen.value.filter((g) => g.rolleId != null ? rollenMap.value[g.rolleId] === 'Verwaltung' : false))
const politikGruppen = computed(() => gruppen.value.filter((g) => g.rolleId != null ? rollenMap.value[g.rolleId] === 'Politik' : false))
const rollenMap = ref({}) // rolleId -> rolleName
const isLoading = ref(false)
const toast = useToast()

const gruppeUsers = ref([])
const isLoadingUsers = ref(false)
const groupUserLists = reactive({})

const verwaltungGruppeSelectOptions = computed(() => [
  { id: null, name: 'Keine Gruppe' },
  ...verwaltungGruppen.value,
])

const politikGruppeSelectOptions = computed(() => [
  { id: null, name: 'Keine Gruppe' },
  ...politikGruppen.value,
])

const buildGroupUserLists = () => {
  const newData = {}
  newData['none-verwaltung'] = gruppeUsers.value
    .filter((u) => (u.gruppeId === null || u.gruppeId === undefined) && u.rolleName === 'Verwaltung')
    .map((u) => ({ ...u }))
  newData['none-politik'] = gruppeUsers.value
    .filter((u) => (u.gruppeId === null || u.gruppeId === undefined) && u.rolleName === 'Politik')
    .map((u) => ({ ...u }))
  for (const g of gruppen.value) {
    newData[g.id] = gruppeUsers.value
      .filter((u) => u.gruppeId === g.id)
      .map((u) => ({ ...u }))
  }
  for (const key in groupUserLists) delete groupUserLists[key]
  Object.assign(groupUserLists, newData)
}

const fetchGruppen = async () => {
  isLoading.value = true
  try {
    const [gruppenRes, rollenRes] = await Promise.all([
      apiClient.get('/einstellungen/gruppe'),
      apiClient.get('/option/user-rolle'),
    ])
    gruppen.value = gruppenRes.data
    rollenMap.value = Object.fromEntries(rollenRes.data.map((r) => [r.id, r.name]))
  } catch {
    gruppen.value = []
  } finally {
    isLoading.value = false
  }
}

const fetchVerwaltungUsers = async () => {
  isLoadingUsers.value = true
  try {
    const res = await apiClient.get('/einstellungen/gruppe/users')
    gruppeUsers.value = res.data
    buildGroupUserLists()
  } catch {
    gruppeUsers.value = []
  } finally {
    isLoadingUsers.value = false
  }
}

onMounted(async () => {
  await fetchGruppen()
  await fetchVerwaltungUsers()
})

watch(gruppen, () => {
  buildGroupUserLists()
})

const onDragChange = async (toGruppeId, event) => {
  if (!event.added) return
  const user = event.added.element
  user.gruppeId = toGruppeId
  try {
    await apiClient.patch(`/einstellungen/gruppe/users/${user.id}`, {
      gruppe_id: toGruppeId,
    })
  } catch {
    await fetchVerwaltungUsers()
    toast.add({ severity: 'error', summary: 'Fehler', detail: 'Zuweisung konnte nicht gespeichert werden.', life: 3000 })
  }
}

const noneKey = (user) => user.rolleName === 'Politik' ? 'none-politik' : 'none-verwaltung'

const onSelectGruppe = async (user, newGruppeId) => {
  if (user.gruppeId === newGruppeId) return
  const fromKey = user.gruppeId === null || user.gruppeId === undefined ? noneKey(user) : user.gruppeId
  const toKey = newGruppeId === null ? noneKey(user) : newGruppeId

  const fromList = groupUserLists[fromKey]
  const idx = fromList?.findIndex((u) => u.id === user.id) ?? -1
  if (idx !== -1) fromList.splice(idx, 1)

  user.gruppeId = newGruppeId
  if (!groupUserLists[toKey]) groupUserLists[toKey] = []
  groupUserLists[toKey].push(user)

  try {
    await apiClient.patch(`/einstellungen/gruppe/users/${user.id}`, {
      gruppe_id: newGruppeId,
    })
  } catch {
    await fetchVerwaltungUsers()
    toast.add({ severity: 'error', summary: 'Fehler', detail: 'Zuweisung konnte nicht gespeichert werden.', life: 3000 })
  }
}

// --- Create form ---
const createVisible = ref(false)
const isCreating = ref(false)
const createRolleName = ref(null)

const {
  defineField: defineCreateField,
  handleSubmit: handleCreate,
  errors: createErrors,
  resetForm: resetCreate,
} = useForm({ validationSchema: gruppeSchema })

const [createName] = defineCreateField('name')

const openCreate = (rolleName) => {
  resetCreate()
  createRolleName.value = rolleName
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
  setValues: setEditValues,
} = useForm({ validationSchema: gruppeSchema })

const [editName] = defineEditField('name')

const openEdit = (gruppe) => {
  editId.value = gruppe.id
  setEditValues({ name: gruppe.name })
  editVisible.value = true
}

// --- Keyboard shortcuts ---
onKeyStroke('Enter', (e) => {
  if (createVisible.value) { e.preventDefault(); submitCreate() }
  if (editVisible.value) { e.preventDefault(); submitEdit() }
})

onKeyStroke('Escape', () => {
  if (createVisible.value) createVisible.value = false
  if (editVisible.value) editVisible.value = false
})

// --- CRUD handlers ---
const submitCreate = handleCreate(async (values) => {
  isCreating.value = true
  const rolleId = Object.entries(rollenMap.value).find(([, name]) => name === createRolleName.value)?.[0]
  try {
    await apiClient.post('/einstellungen/gruppe', { name: values.name, rolle_id: rolleId ? Number(rolleId) : null })
    toast.add({ severity: 'success', summary: 'Gruppe angelegt', life: 3000 })
    createVisible.value = false
    await fetchGruppen()
  } catch {
    toast.add({ severity: 'error', summary: 'Fehler', detail: 'Gruppe konnte nicht angelegt werden.', life: 3000 })
  } finally {
    isCreating.value = false
  }
})

const submitEdit = handleEdit(async (values) => {
  isSaving.value = true
  try {
    const res = await apiClient.patch(`/einstellungen/gruppe/${editId.value}`, { name: values.name })
    const idx = gruppen.value.findIndex((g) => g.id === editId.value)
    if (idx !== -1) gruppen.value[idx] = res.data
    editVisible.value = false
    toast.add({ severity: 'success', summary: 'Gespeichert', life: 3000 })
  } catch {
    toast.add({ severity: 'error', summary: 'Fehler', detail: 'Änderung konnte nicht gespeichert werden.', life: 3000 })
  } finally {
    isSaving.value = false
  }
})

const deleteGruppe = async (id) => {
  try {
    await apiClient.delete(`/einstellungen/gruppe/${id}`)
    gruppen.value = gruppen.value.filter((g) => g.id !== id)
    toast.add({ severity: 'success', summary: 'Gruppe gelöscht', life: 3000 })
    // Users assigned to deleted group now have no group — refresh
    await fetchVerwaltungUsers()
  } catch {
    toast.add({ severity: 'error', summary: 'Fehler', detail: 'Gruppe konnte nicht gelöscht werden.', life: 3000 })
  }
}
</script>

<style scoped>
.field {
  display: flex;
  flex-direction: column;
}
</style>
