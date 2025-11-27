<template>
  <form @submit.prevent="onSubmit">
    <div class="ms-6 mt-5">
      <div class="flex items-center gap-2" @click="toggleTangiert">
        <Checkbox
          class="flex-none"
          id="sub-checkbox"
          v-model="tangiert"
          :binary="true"
          :invalid="!!errors.tangiert"
          @click="toggleTangiert"
        />
        <label for="sub-checkbox" class="text-lg font-bold flex justify-center gap-2">
          <span>{{ props.zielOberNr }}.{{ item.zielUnter.nr }}</span>
          <span>{{ item.zielUnter.name }}</span>
        </label>
      </div>
      <div v-if="tangiert">
        <div class="grid grid-cols-2 gap-4">
          <div class="w-full my-auto max-w-md">
            <label for="auswirkung">Wirkungsrichtung und -stärke</label>
            <Slider
              id="auswirkung"
              v-model.number="auswirkung"
              :min="-3"
              :max="3"
              :step="1"
              :defaultValue="0"
              :invalid="!!errors.auswirkung"
              class="w-full mt-3"
            />
            <div class="relative w-full flex justify-between mt-2">
              <span
                v-for="tick in 7"
                :key="tick"
                class="relative flex flex-col items-center cursor-pointer"
                @click="moveSlider(index, tick - 4)"
              >
                <!-- Enlarge the clickable area around the tick -->
                <div
                  class="h-10 w-10 absolute top-0 left-1/2 transform -translate-x-1/2 bg-transparent"
                ></div>

                <span class="w-0.5 h-2 bg-gray-800"></span>
                <!-- Invisible but clickable -->
                <span class="absolute top-2 left-1/2 transform -translate-x-1/2 text-xs">
                  {{ tickmarkLabels[tick] }}
                </span>
              </span>
            </div>
          </div>
          <div class="ms-5 mt-7 my-auto max-w-md">
            <FloatLabel variant="on">
              <Select
                id="auswirkungRaeumlichId"
                v-model="auswirkungRaeumlichId"
                :options="optionsAuswirkungRaeumlich"
                optionLabel="name"
                optionValue="id"
                :invalid="!!errors.auswirkungRaeumlichId"
                class="w-full dont-close-on-select"
              />
              <label for="auswirkungRaeumlichId">Räumliche Auswirkung</label>
            </FloatLabel>
          </div>
        </div>
        <div class="mt-7 max-w-5xl">
          <FloatLabel variant="on">
            <Textarea
              id="anmerkung"
              v-model="anmerkung"
              rows="5"
              :invalid="!!errors.anmerkung"
              class="w-full"
            />
            <label for="anmerkung">Erläuterung</label>
          </FloatLabel>
        </div>
        <ButtonTextblockHinzufuegen
          class="mt-3 w-full"
          @textblock-hinzufuegen="textblockHinzufuegen($event)"
        />
        <div class="mt-7 max-w-5xl">
          <FloatLabel variant="on">
            <MultiSelect
              id="indikatoren"
              v-model="indikatorIds"
              :options="optionsIndikatoren"
              filter
              optionLabel="name"
              optionValue="id"
              class="w-full dont-close-on-select"
              display="chip"
              :invalid="!!errors.indikatorIds"
              empty-filter-message="Keine Ergebnisse gefunden"
              :pt="{
                header: () => ({
                  id: `indicators_header`
                })
              }"
            />
            <label for="indikatoren">Indikatoren auswählen</label>
          </FloatLabel>
        </div>
      </div>
    </div>
  </form>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import { useStorage } from '@vueuse/core'
import { fetchItem, fetchItems, updateItemSilent } from '@/composables/crud'
import { useForm } from 'vee-validate'
import { schema } from '@/utils/schemas/mobilitaetscheckEingabeZielUnter'
import Checkbox from 'primevue/checkbox'
import FloatLabel from 'primevue/floatlabel'
import Select from 'primevue/select'
import MultiSelect from 'primevue/multiselect'
import Textarea from 'primevue/textarea'
import Slider from 'primevue/slider'
import ButtonTextblockHinzufuegen from '@/components/ButtonTextblockHinzufuegen.vue'

const props = defineProps({
  editMode: {
    type: Boolean,
    default: false
  },
  item: {
    type: Object,
    default: null
  },
  zielOberNr: {
    type: Number
  }
})

const optionsIndikatoren = ref([])
const tickmarkLabels = useStorage('cachedTickmarkLabels', {})
const optionsAuswirkungRaeumlich = useStorage('cachedAuswirkungRaeumlich', [])

const fetchOptions = async () => {
  if (
    !Array.isArray(optionsAuswirkungRaeumlich.value) ||
    optionsAuswirkungRaeumlich.value.length === 0
  ) {
    optionsAuswirkungRaeumlich.value = await fetchItems(
      '/option/mobilitaetscheck/auswirkung-raeumlich'
    )
  }
  if (Object.keys(tickmarkLabels.value).length === 0) {
    tickmarkLabels.value = await fetchItem('/option/mobilitaetscheck/auswirkung-tickmarks')
  }
  optionsIndikatoren.value = await fetchItems('/einstellungen/indikator')
}

const { defineField, handleSubmit, validate, errors, setFieldValue, setValues } = useForm({
  validationSchema: schema
})

const [tangiert] = defineField('tangiert')
const [auswirkung] = defineField('auswirkung')
const [auswirkungRaeumlichId] = defineField('auswirkungRaeumlichId')
const [anmerkung] = defineField('anmerkung')
const [indikatorIds] = defineField('indikatorIds')

onMounted(async () => {
  await fetchOptions()
})

watch(
  () => props.item,
  (newItem) => {
    if (!newItem) return
    const {
      tangiert,
      auswirkung,
      auswirkungRaeumlichId,
      anmerkung,
      indikatorIds,
      eingabeZielOberId,
      zielUnterId
    } = newItem

    setValues({
      tangiert,
      auswirkung,
      auswirkungRaeumlichId,
      anmerkung,
      indikatorIds,
      eingabeZielOberId,
      zielUnterId
    })
  },
  { immediate: true } // sofort beim ersten gesetzten Wert ausführen
)

const toggleTangiert = () => {
  setFieldValue('tangiert', !tangiert.value)
}

const moveSlider = (tickValue) => {
  setFieldValue('auswirkung', tickValue)
}

const textblockHinzufuegen = (event) => {
  const current = anmerkung?.value?.trim()

  if (current && current.length > 0) {
    // hat schon Inhalt → neuen Absatz anhängen
    setFieldValue('anmerkung', `${anmerkung.value}\n${event}`)
  } else {
    // noch leer → direkt Text einsetzen
    setFieldValue('anmerkung', event)
  }
}

const onSubmit = handleSubmit(async (values) => {
  await updateItemSilent({
    model: 'mobilitaetscheck/eingabe/ziel/unter',
    modelId: props.item.id,
    values
  })
})

defineExpose({ onSubmit, validate })
</script>

<style scoped></style>
