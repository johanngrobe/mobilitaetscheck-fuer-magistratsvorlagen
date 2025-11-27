<template>
  <form @submit.prevent="onSubmit">
    <div>
      <div class="flex items-center" @click="toggleTarget">
        <Checkbox
          class="flex-none"
          id="sub-checkbox"
          v-model="target"
          :binary="true"
          :invalid="!!errors.target"
          @click="toggleTarget"
        />
        <label for="sub-checkbox" class="text-lg font-bold flex justify-center">
          <span
            >{{ subObjective.subObjective.mainObjectiveId }}.{{
              subObjective.subObjective.no
            }}</span
          >
          <span>{{ subObjective.subObjective.label }}</span>
        </label>
      </div>
      <div v-if="target">
        <div class="grid grid-cols-2 gap-4">
          <div class="w-full my-auto max-w-md">
            <label for="impact">Wirkungsrichtung und -stärke</label>
            <Slider
              id="impact"
              v-model.number="impact"
              :min="-3"
              :max="3"
              :step="1"
              :invalid="!!errors.impact"
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
                  {{ tickmarkLabels[tick - 4] }}
                </span>
              </span>
            </div>
          </div>
          <div class="ms-5 mt-7 my-auto max-w-md">
            <FloatLabel variant="on">
              <Select
                id="spatial-impact"
                v-model="spatialImpact"
                :options="optionsSpatialImpact"
                optionLabel="label"
                optionValue="value"
                :invalid="!!errors.spatialImpact"
                class="w-full dont-close-on-select"
              />
              <label for="spatial-impact">Räumliche Auswirkung</label>
            </FloatLabel>
          </div>
        </div>
        <div class="mt-7 max-w-5xl">
          <FloatLabel variant="on">
            <Textarea
              id="annotation"
              v-model="annotation"
              rows="5"
              :invalid="!!errors.annotation"
              class="w-full"
            />
            <label for="annotation">Erläuterung</label>
          </FloatLabel>
        </div>
        <AddTextBlock class="mt-3 w-full" @add-text-block="appendTextBlock($event)" />
        <div class="mt-7 max-w-5xl">
          <FloatLabel variant="on">
            <MultiSelect
              id="indicators"
              v-model="indicatorIds"
              :options="optionsIndicators"
              filter
              optionLabel="label"
              optionValue="id"
              class="w-full dont-close-on-select"
              display="chip"
              :invalid="!!errors.indicatorIds"
              empty-filter-message="Keine Ergebnisse gefunden"
              :pt="{
                header: () => ({
                  id: `indicators_header`
                })
              }"
            />
            <label for="indicators">Indikatoren auswählen</label>
          </FloatLabel>
        </div>
      </div>
    </div>
  </form>
</template>

<script setup>
import { onMounted } from 'vue'
import { useStorage } from '@vueuse/core'
import { fetchItems } from '@/composables/crud'
import { useForm } from 'vee-validate'
import { schema } from '@/utils/schemas/mobilitySubmissionSubObjectiveForm'
import Checkbox from 'primevue/checkbox'
import FloatLabel from 'primevue/floatlabel'
import Select from 'primevue/select'
import MultiSelect from 'primevue/multiselect'
import Textarea from 'primevue/textarea'
import Slider from 'primevue/slider'
import AddTextBlock from '@/components/ButtonTextblockHinzufuegen.vue'

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

const optionsIndicators = useStorage('cachedIndicators', [])
const tickmarkLabels = useStorage('cachedTickmarkLabels', {})
const optionsSpatialImpact = useStorage('cachedSpatialImpactOptions', [])

const fetchOptions = async () => {
  optionsSpatialImpact.value = await fetchItems('/option/mobility/spatial-impact')
  if (Object.keys(tickmarkLabels.value).length === 0) {
    const response = await fetchItems('/option/mobility/impact-tickmarks')
    tickmarkLabels.value = response.data.reduce((acc, { label, value }) => {
      acc[value] = label
      return acc
    }, {})
  }
  optionsIndicators.value = await fetchItems('/indicator')
}

const { defineField, handleSubmit, errors, setFieldValue, setValues } = useForm({
  validationSchema: schema
})

const [target] = defineField('target')
const [impact] = defineField('impact')
const [spatialImpact] = defineField('spatialImpact')
const [annotation] = defineField('annotation')
const [indicatorIds] = defineField('indicatorIds')

onMounted(async () => {
  await fetchOptions()
  if (props.editMode) {
    setValues(props.item)
  }
})

const toggleTarget = () => {
  setFieldValue('target', !target.value)
}

const moveSlider = (tickValue) => {
  setFieldValue('impact', tickValue)
}

const appendTextBlock = (event) => {
  if (annotation) {
    setFieldValue('annotation', `${annotation.value}\n${event}`)
  } else {
    setFieldValue('annotation', event)
  }
}

const emit = defineEmits(['submit-item'])

const onSubmit = handleSubmit(async (values) => {
  emit('submit-item', values)
})
</script>

<style scoped></style>
