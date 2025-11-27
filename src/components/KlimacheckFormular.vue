<template>
  <form @submit.prevent="onSubmit" class="grid grid-cols-1 gap-y-4 my-7">
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
        <label for="name">Name des Klimachecks</label>
      </FloatLabel>
      <small v-if="errors.name" id="name-help" class="p-error block">{{ errors.name }}</small>
    </div>

    <div class="form-group field">
      <label
        for="klimarelevanzId"
        class="font-bold text-lg"
        :class="{ 'p-invalid': errors.klimarelevanzId }"
      >
        Einschätzung der Klimarelevanz
      </label>
      <SelectButton
        id="klimarelevanzId"
        v-model="klimarelevanzId"
        :options="klimarelevanzOptions"
        optionLabel="name"
        optionValue="id"
        :invalid="!!errors.klimarelevanzId"
        class="w-full mt-3"
      />
      <!-- Error Message -->
      <small v-if="errors.klimarelevanzId" id="klimarelevanzId-help" class="p-error">{{
        errors.klimarelevanzId
      }}</small>
    </div>

    <div v-if="fortsetzungFormular">
      <div class="form-group mt-7">
        <div class="flex">
          <div class="text-lg font-bold me-1">Art und Umfang der Auswirkungen</div>
          <HoverInfo icon="MaterialSymbolsInfo.svg">
            <template #title>Frage 2 zielt auf die Klimawirkung im jeweiligen Bereich ab.</template>
            <ul>
              <li>Zwei grünen Pfeile: erhebliche positive Auswirkungen &lt; 100 t CO2e pro Jahr</li>
              <li>Ein grüner Pfeil: positive Auswirkungen &lt; 100 t CO2e pro Jahr</li>
              <li>Ein roter Pfeil: negative Auswirkungen &lt; 100 t CO2e pro Jahr</li>
              <li>Zwei rote Pfeile: erhebliche negative Auswirkungen &lt; 100 t CO2e pro Jahr</li>
            </ul>
          </HoverInfo>
        </div>
        <div>
          <!-- Table-like structure with labels on the left and radio buttons on the right -->
          <div class="grid grid-cols-6 gap-4">
            <!-- Empty cell for top-left corner -->
            <div class="col-span-2"></div>

            <!-- Column labels for the radio buttons -->
            <div v-for="option in auswirkungOptions" :key="option.value" class="text-center">
              <label class="block text-gray-700 font-medium">
                {{ option.label }}
              </label>
            </div>

            <!-- Impact GHg Row -->
            <div class="flex col-span-2 items-center">
              <div class="text-md mr-1" :class="{ 'p-invalid': errors.auswirkungThg }">
                THG-Emissionen
              </div>
              <HoverInfo icon="MaterialSymbolsInfo.svg">Treibhausgasemissionen</HoverInfo>
            </div>
            <div v-for="option in auswirkungOptions" :key="option.value" class="text-center">
              <RadioButton
                :id="`ghg-${option.value}`"
                v-model="auswirkungThg"
                :value="option.value"
                name="auswirkungThg"
                :invalid="!!errors.auswirkungThg"
              />
            </div>

            <!-- Impact Adaption Row -->
            <div class="col-span-2">
              <div class="text-md mr-1" :class="{ 'p-invalid': errors.auswirkungKlimaanpassung }">
                Klimaanpassung
              </div>
            </div>
            <div v-for="option in auswirkungOptions" :key="option.value" class="text-center">
              <RadioButton
                :id="`adaption-${option.value}`"
                v-model="auswirkungKlimaanpassung"
                :value="option.value"
                name="auswirkungKlimaanpassung"
                :invalid="!!errors.auswirkungKlimaanpassung"
              />
            </div>
          </div>

          <!-- Error messages -->
          <small v-if="errors.auswirkungThg" id="impact-ghg-help" class="p-error">
            {{ errors.auswirkungThg }}
          </small>
          <small v-if="errors.auswirkungKlimaanpassung" id="impact-adaption-help" class="p-error">
            {{ errors.auswirkungKlimaanpassung }}
          </small>
        </div>

        <div class="form-group field mt-7">
          <FloatLabel variant="on">
            <label for="auswirkungBeschreibung">Kurzbeschreibung der Auswirkungen</label>
            <Textarea
              id="auswirkungBeschreibung"
              v-model="auswirkungBeschreibung"
              rows="5"
              aria-describedby="auswirkungBeschreibung-help"
              :invalid="!!errors.auswirkungBeschreibung"
              class="w-full"
              inputClass="w-full"
            />
          </FloatLabel>
          <small
            v-if="errors.auswirkungBeschreibung"
            id="auswirkungBeschreibung-help"
            class="p-error block"
            >{{ errors.auswirkungBeschreibung }}</small
          >
        </div>

        <div class="form-group field">
          <label
            for="impact"
            class="font-bold text-lg"
            :class="{ 'p-invalid': errors.klimarelevanz }"
          >
            Dauer der Auswirkungen
          </label>

          <SelectButton
            id="auswirkungDauerId"
            v-model="auswirkungDauerId"
            :options="auswirkungDauerOptions"
            optionLabel="name"
            optionValue="id"
            :invalid="!!errors.auswirkungDauerId"
            class="w-full mt-3"
          />
          <!-- Error Message -->
          <small v-if="errors.auswirkungDauerId" id="auswirkungDauerId-help" class="p-error">{{
            errors.auswirkungDauerId
          }}</small>
        </div>

        <div class="form-group field mt-7">
          <FloatLabel variant="on">
            <label for="alternativen"> Klimafreundliche Alternativen zu der Maßnahme </label>
            <Textarea
              id="alternativen"
              v-model="alternativen"
              rows="5"
              aria-describedby="alternativen-help"
              :invalid="!!errors.alternativen"
              class="w-full"
              inputClass="w-full"
            />
          </FloatLabel>
          <small>* Falls nicht vorhanden: Begründung der Alternativlosigkeit </small>

          <small v-if="errors.alternativen" id="alternativen-help" class="p-error block">{{
            errors.alternativen
          }}</small>
        </div>
      </div>
    </div>
    <div v-if="klimarelevanzId" class="flex w-full justify-end">
      <Button icon="pi pi-save" @click="closeModal" type="submit" label="speichern"></Button>
    </div>
  </form>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useForm } from 'vee-validate'
import { schema } from '@/utils/schemas/klimacheck'
import { toTypedSchema } from '@vee-validate/yup'
import { createItem, fetchItems } from '@/composables/crud'
import Button from 'primevue/button'
import InputText from 'primevue/inputtext'
import FloatLabel from 'primevue/floatlabel'
import Textarea from 'primevue/textarea'
import RadioButton from 'primevue/radiobutton'
import SelectButton from 'primevue/selectbutton'
import HoverInfo from '@/components/HoverInfo.vue'

const props = defineProps({
  editMode: {
    type: Boolean,
    default: false
  },
  item: {
    type: Object,
    default: null
  }
})

const klimarelevanzOptions = ref([])
const auswirkungOptions = ref([])
const auswirkungDauerOptions = ref([])
const route = useRoute()
const router = useRouter()

const fetchOptions = async () => {
  klimarelevanzOptions.value = await fetchItems('option/klimacheck/klimarelevanz')
  auswirkungOptions.value = await fetchItems('option/klimacheck/auswirkung')
  auswirkungDauerOptions.value = await fetchItems('option/klimacheck/auswirkung-dauer')
}

const { defineField, handleSubmit, errors, setFieldValue, setValues } = useForm({
  validationSchema: toTypedSchema(schema)
})

const [name] = defineField('name')
const [klimarelevanzId] = defineField('klimarelevanzId')
const [auswirkungThg] = defineField('auswirkungThg')
const [auswirkungKlimaanpassung] = defineField('auswirkungKlimaanpassung')
const [auswirkungBeschreibung] = defineField('auswirkungBeschreibung')
const [auswirkungDauerId] = defineField('auswirkungDauerId')
const [alternativen] = defineField('alternativen')

onMounted(async () => {
  await fetchOptions()
  if (props.editMode) {
    setValues({
      name: props.item.name,
      klimarelevanzId: props.item.klimarelevanzId,
      auswirkungThg: props.item.auswirkungThg,
      auswirkungKlimaanpassung: props.item.auswirkungKlimaanpassung,
      auswirkungBeschreibung: props.item.auswirkungBeschreibung,
      auswirkungDauerId: props.item.auswirkungDauerId,
      alternativen: props.item.alternativen
    })
  }
})

setFieldValue('magistratsvorlageId', route.params.id)

const fortsetzungFormular = computed(() => {
  switch (klimarelevanzId.value) {
    case 1:
      return true
    case 2:
      return true
    case 3:
      return false
    default:
      return false
  }
})

// Emit event to close modal
const emit = defineEmits(['close-modal', 'update-item', 'add-item', 'export-item', 'reload-item'])

const closeModal = () => {
  if (props.editMode) {
    emit('close-modal')
  }
}

// Handle form submission for both create (POST) and edit (PUT)
const onSubmit = handleSubmit(async (values) => {
  const formattedValues = { ...values }

  // Format the date to yyyy-mm-dd if it's a Date object
  if (values.verwaltungsvorgangDatum instanceof Date) {
    const tzoffset = new Date().getTimezoneOffset() * 60000 //offset in milliseconds
    formattedValues.verwaltungsvorgangDatum = new Date(values.verwaltungsvorgangDatum - tzoffset)
      .toISOString()
      .split('T')[0]
  }
  if (props.editMode) {
    emit('update-item', { modelId: props.item.id, values: formattedValues })
    emit('reload-item')
  } else {
    // POST request to create a new submission
    await createItem({
      model: 'klimacheck/eingabe',
      values: formattedValues,
      detail: {
        success: 'Klimacheck gespeichert',
        error: 'Fehler beim Speichern des Klimachecks'
      }
    })
    router.replace({
      name: 'magistratsvorlage-id-klimacheck',
      params: { id: route.params.id }
    })
  }
})
</script>

<style scoped>
.p-invalid {
  @apply border-red-600 text-red-600;
}

.p-error {
  @apply text-red-600;
}
</style>
