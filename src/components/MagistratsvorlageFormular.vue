<template>
  <div>
    <ConfirmDialog></ConfirmDialog>
    <BaseSpinner v-if="isLoading" />
    <form v-else class="grid grid-cols-1 gap-y-4 my-7" @submit.prevent="onSubmit">
      <div class="form-group field">
        <FloatLabel variant="on">
          <InputText
            id="verwaltungsvorgangNr"
            v-model="verwaltungsvorgangNr"
            :invalid="!!errors.verwaltungsvorgangNr"
            class="w-full"
            inputClass="w-full"
          />
          <label for="verwaltungsvorgangNr">Magistratsvorlagennummer</label>
        </FloatLabel>
        <small
          v-if="errors.verwaltungsvorgangNr"
          id="verwaltungsvorgangNr-help"
          class="p-error block"
        >
          {{ errors.verwaltungsvorgangNr }}
        </small>
      </div>

      <div class="form-group field">
        <FloatLabel variant="on">
          <DatePicker
            id="verwaltungsvorgangDatum"
            v-model="verwaltungsvorgangDatum"
            showIcon
            iconDisplay="input"
            :invalid="!!errors.verwaltungsvorgangDatum"
          />
          <label for="verwaltungsvorgangDatum"> Datum der Magistratssitzung </label>
        </FloatLabel>
        <small
          v-if="errors.verwaltungsvorgangDatum"
          id="verwaltungsvorgangDatum-help"
          class="p-error block"
        >
          {{ errors.verwaltungsvorgangDatum }}
        </small>
      </div>

      <div class="form-group field">
        <FloatLabel variant="on">
          <InputText
            id="name"
            v-model="name"
            aria-describedby="name-help"
            :invalid="!!errors.name"
            class="w-full"
            inputClass="w-full"
          />
          <label for="name">Titel der Magistratsvorlage</label>
        </FloatLabel>
        <small v-if="errors.name" id="name-help" class="p-error block">{{ errors.name }}</small>
      </div>
      <div>
        <FloatLabel variant="on">
          <MultiSelect
            id="gemeindeGebietIds"
            v-model="gemeindeGebietIds"
            :options="gebiete"
            optionLabel="name"
            optionValue="id"
            display="chip"
            class="w-full"
            filter
            :invalid="!!errors.gemeindeGebietIds"
          />
          <label for="gemeindeGebietIds">Gebiete auswählen</label>
        </FloatLabel>
        <small v-if="errors.gemeindeGebietIds" id="gemeindeGebietIds-help" class="p-error block">{{
          errors.gemeindeGebietIds
        }}</small>
      </div>
      <div>
        <FloatLabel variant="on">
          <MultiSelect
            id="tagIds"
            v-model="tagIds"
            :options="tagOptions"
            optionLabel="name"
            optionValue="id"
            display="chip"
            class="w-full"
            filter
            :invalid="!!errors.tagIds"
          />
          <label for="tagIds">Tags auswählen</label>
        </FloatLabel>
        <small v-if="errors.gemeindeGebietIds" id="tagIds-help" class="p-error block">{{
          errors.tagIds
        }}</small>
      </div>
      <div class="form-group field">
        <FloatLabel variant="on">
          <Textarea
            id="beschreibung"
            v-model="beschreibung"
            rows="5"
            aria-describedby="beschreibung-help"
            :invalid="!!errors.beschreibung"
            class="w-full"
            inputClass="w-full"
          />
          <label for="beschreibung">Beschreibung der Maßnahme</label>
        </FloatLabel>
        <small v-if="errors.beschreibung" id="beschreibung-help" class="p-error block">{{
          errors.beschreibung
        }}</small>
      </div>
      <div class="flex justify-end w-full">
        <Button icon="pi pi-save" type="submit" label="speichern" :loading="isLoading" />
      </div>
      <div v-if="editMode">
        <Divider />
        <BaseSubheading>Danger Zone</BaseSubheading>
        <div class="mt-4">
          <Button
            @click="confirmDelete()"
            icon="pi pi-trash"
            label="Magistratsvorlage löschen"
            severity="danger"
          />
        </div>
      </div>
    </form>
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useForm } from 'vee-validate'
import { schema } from '@/utils/schemas/magistratsvorlage'
import { toTypedSchema } from '@vee-validate/yup'
import { createItem, deleteItem, fetchItems, updateItem } from '@/composables/crud'
import { useConfirm } from 'primevue/useconfirm'
import Button from 'primevue/button'
import ConfirmDialog from 'primevue/confirmdialog'
import Divider from 'primevue/divider'
import InputText from 'primevue/inputtext'
import DatePicker from 'primevue/datepicker'
import Textarea from 'primevue/textarea'
import FloatLabel from 'primevue/floatlabel'
import MultiSelect from 'primevue/multiselect'

const confirm = useConfirm()

const props = defineProps({
  editMode: {
    type: Boolean,
    default: true
  }
})

const router = useRouter()
const route = useRoute()
const isLoading = ref(false)
const gebiete = ref([])
const tagOptions = ref([])

const { defineField, handleSubmit, errors, setValues } = useForm({
  validationSchema: toTypedSchema(schema)
})

const [verwaltungsvorgangNr] = defineField('verwaltungsvorgangNr')
const [verwaltungsvorgangDatum] = defineField('verwaltungsvorgangDatum')
const [name] = defineField('name')
const [beschreibung] = defineField('beschreibung')
const [gemeindeGebietIds] = defineField('gemeindeGebietIds')
const [tagIds] = defineField('tagIds')

onMounted(async () => {
  if (props.editMode) {
    await fetchMagistratsvorlage()
  }
  await fetchOptions()
})

const fetchOptions = async () => {
  isLoading.value = true
  gebiete.value = await fetchItems('einstellungen/gebiet')
  tagOptions.value = await fetchItems('/einstellungen/tag')
  isLoading.value = false
}

const fetchMagistratsvorlage = async () => {
  isLoading.value = true
  const response = await fetchItems(`/magistratsvorlage/${route.params.id}`)
  setValues({
    verwaltungsvorgangNr: response.verwaltungsvorgangNr,
    verwaltungsvorgangDatum: new Date(response.verwaltungsvorgangDatum),
    name: response.name,
    beschreibung: response.beschreibung,
    gemeindeId: response.gemeindeId,
    gemeindeGebietIds: response.gemeindeGebietIds,
    tagIds: response.tagIds
  })
  isLoading.value = false
}

const onSubmit = handleSubmit(async (values) => {
  if (props.editMode) {
    await updateItem({
      model: 'magistratsvorlage',
      modelId: route.params.id,
      values: values,
      detail: {
        success: 'Magistratsvorlage erfolgreich aktualisiert',
        error: 'Fehler beim Aktualisieren der Magistratsvorlage'
      }
    })
  } else {
    isLoading.value = true
    const response = await createItem({
      model: 'magistratsvorlage',
      values: values,
      detail: {
        success: 'Magistratsvorlage erfolgreich erstellt',
        error: 'Fehler beim Erstellen der Magistratsvorlage'
      }
    })

    router.replace({
      name: 'magistratsvorlage-id-daten',
      params: { id: response.id }
    })
    isLoading.value = false
  }
})

const confirmDelete = () => {
  confirm.require({
    message: 'Möchten Sie diese Magistratsvorlage löschen?',
    header: 'Löschen bestätigen',
    icon: 'pi pi-exclamation-triangle',
    rejectProps: {
      label: 'Abbrechen',
      severity: 'secondary',
      outlined: true
    },
    acceptProps: {
      label: 'löschen',
      severity: 'danger'
    },
    accept: async () => {
      await deleteItem({
        model: 'magistratsvorlage',
        modelId: route.params.id,
        detail: {
          success: 'Magistratsvorlage erfolgreich gelöscht.',
          error: 'Fehler beim Löschen der Magistratsvorlage.'
        }
      })
      router.push({ name: 'magistratsvorlage-liste' })
    }
  })
}
</script>

<style scoped>
.p-invalid {
  @apply border-red-600 text-red-600;
}

.p-error {
  @apply text-red-600;
}
</style>
