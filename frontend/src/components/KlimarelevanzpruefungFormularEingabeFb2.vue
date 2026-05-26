<template>
  <div>
    <Message v-if="hasErrors" severity="error" class="mb-4">
      <ul class="list-disc list-inside">
        <li v-for="(error, field) in errors" :key="field">{{ dynamicErrorLabels[field] ?? error }}</li>
      </ul>
    </Message>
    <form @submit.prevent="onSubmit" class="mt-4">
      <Stepper value="1">
        <StepList>
          <Step value="1"></Step>
          <Step value="2"></Step>
        </StepList>
        <StepPanels>
          <StepPanel v-slot="{ activateCallback }" value="1">
            <ol>
              <li>
                <span>Handelt es sich um einen Bebauungsplan?</span>
                <SelectButton
                  v-model="b1q1"
                  :options="optionBoolean"
                  optionLabel="name"
                  optionValue="id"
                  :multiple="false"
                  :invalid="!!errors.b1q1"
                />
              </li>
              <Divider />
              <template v-if="b1q1 === 1">
                <li>
                  <span>Wurde im B-Plan eine PV-Pflicht verankert?</span>
                  <SelectButton
                    v-model="b1q2"
                    :options="optionBoolean"
                    optionLabel="name"
                    optionValue="id"
                    :multiple="false"
                    :invalid="!!errors.b1q2"
                  />
                </li>
                <li v-if="b1q2 === 2">
                  <span>Warum nicht?</span>
                  <FloatLabel variant="on" class="w-full">
                    <InputText
                      id="b1q3"
                      v-model="b1q3"
                      aria-describedby="b1q4-help"
                      :invalid="!!errors.b1q3"
                      class="w-full"
                      inputClass="w-full"
                    />
                    <label for="b1q3">Erläuterung</label>
                  </FloatLabel>
                </li>
                <Divider />
                <li>
                  <span>Wurde im B-Plan eine Gründachpflicht verankert?</span>
                  <SelectButton
                    v-model="b1q4"
                    :options="optionBoolean"
                    optionLabel="name"
                    optionValue="id"
                    :multiple="false"
                    :invalid="!!errors.b1q4"
                  />
                </li>
                <li v-if="b1q4 === 2">
                  <span>Warum nicht?</span>
                  <FloatLabel variant="on" class="w-full">
                    <InputText
                      id="b1q5"
                      v-model="b1q5"
                      aria-describedby="b1q5-help"
                      :invalid="!!errors.b1q5"
                      class="w-full"
                      inputClass="w-full"
                    />
                    <label for="b1q5">Erläuterung</label>
                  </FloatLabel>
                </li>
                <Divider />
                <li>
                  <span>
                    Wurde im B-Plan eine nachhaltige Regenwasserbewirtschaftung verankert? (z. B.
                    Sickergruben, Zisternen, Rückhaltebecken etc.)
                  </span>
                  <SelectButton
                    v-model="b1q6"
                    :options="optionBoolean"
                    optionLabel="name"
                    optionValue="id"
                    :multiple="false"
                    :invalid="!!errors.b1q6"
                  />
                </li>
                <li v-if="b1q6 === 1">
                  <span>In welcher Form?</span>
                  <FloatLabel variant="on" class="w-full">
                    <InputText
                      id="b1q7"
                      v-model="b1q7"
                      aria-describedby="b1q7-help"
                      :invalid="!!errors.b1q7"
                      class="w-full"
                      inputClass="w-full"
                    />
                    <label for="b1q7">Beschreibung</label>
                  </FloatLabel>
                </li>
                <li v-if="b1q6 === 2">
                  <span>Warum nicht?</span>
                  <FloatLabel variant="on" class="w-full">
                    <InputText
                      id="b1q8"
                      v-model="b1q8"
                      aria-describedby="b1q8-help"
                      :invalid="!!errors.b1q8"
                      class="w-full"
                      inputClass="w-full"
                    />
                    <label for="b1q8">Erläuterung</label>
                  </FloatLabel>
                </li>
                <Divider />
                <li>
                  <span>Wurden im B-Plan weitere wasserrückhaltende Maßnahmen verankert?</span>
                  <SelectButton
                    v-model="b1q9"
                    :options="optionBoolean"
                    optionLabel="name"
                    optionValue="id"
                    :multiple="false"
                    :invalid="!!errors.b1q9"
                  />
                </li>
                <li v-if="b1q9 === 1">
                  <span>In welcher Form?</span>
                  <FloatLabel variant="on" class="w-full">
                    <InputText
                      id="b1q10"
                      v-model="b1q10"
                      aria-describedby="b1q10-help"
                      :invalid="!!errors.b1q10"
                      class="w-full"
                      inputClass="w-full"
                    />
                    <label for="b1q10">Beschreibung</label>
                  </FloatLabel>
                </li>
                <li v-if="b1q9 === 2">
                  <span>Warum nicht?</span>
                  <FloatLabel variant="on" class="w-full">
                    <InputText
                      id="b1q11"
                      v-model="b1q11"
                      aria-describedby="b1q11-help"
                      :invalid="!!errors.b1q11"
                      class="w-full"
                      inputClass="w-full"
                    />
                    <label for="b1q11">Erläuterung</label>
                  </FloatLabel>
                </li>
                <Divider />
                <li>
                  <span>
                    Wurden im B-Plan weitere hitzepräventive Maßnahmen verankert? (z.B. durch
                    Begrünung)
                  </span>
                  <SelectButton
                    v-model="b1q12"
                    :options="optionBoolean"
                    optionLabel="name"
                    optionValue="id"
                    :multiple="false"
                    :invalid="!!errors.b1q12"
                  />
                </li>
                <li v-if="b1q12 === 1">
                  <span>In welcher Form?</span>
                  <FloatLabel variant="on" class="w-full">
                    <InputText
                      id="b1q13"
                      v-model="b1q13"
                      aria-describedby="b1q13-help"
                      :invalid="!!errors.b1q13"
                      class="w-full"
                      inputClass="w-full"
                    />
                    <label for="b1q13">Beschreibung</label>
                  </FloatLabel>
                </li>
                <li v-if="b1q12 === 2">
                  <span>Warum nicht?</span>
                  <FloatLabel variant="on" class="w-full">
                    <InputText
                      id="b1q14"
                      v-model="b1q14"
                      aria-describedby="b1q14-help"
                      :invalid="!!errors.b1q14"
                      class="w-full"
                      inputClass="w-full"
                    />
                    <label for="b1q14">Erläuterung</label>
                  </FloatLabel>
                </li>
                <Divider />
                <li>
                  <span>
                    Wurde im B-Plan ein Fokus auf platzsparendes Bauen gelegt und möglichst wenig
                    Fläche wird versiegelt?
                  </span>
                  <SelectButton
                    v-model="b1q15"
                    :options="optionBoolean"
                    optionLabel="name"
                    optionValue="id"
                    :multiple="false"
                    :invalid="!!errors.b1q15"
                  />
                </li>
                <li v-if="b1q15 === 1">
                  <span>In welcher Form?</span>
                  <FloatLabel variant="on" class="w-full">
                    <InputText
                      id="b1q16"
                      v-model="b1q16"
                      aria-describedby="b1q16-help"
                      :invalid="!!errors.b1q16"
                      class="w-full"
                      inputClass="w-full"
                    />
                    <label for="b1q16">Beschreibung</label>
                  </FloatLabel>
                </li>
                <li v-if="b1q15 === 2">
                  <span>Warum nicht?</span>
                  <FloatLabel variant="on" class="w-full">
                    <InputText
                      id="b1q17"
                      v-model="b1q17"
                      aria-describedby="b1q17-help"
                      :invalid="!!errors.b1q17"
                      class="w-full"
                      inputClass="w-full"
                    />
                    <label for="b1q17">Erläuterung</label>
                  </FloatLabel>
                </li>
                <Divider />
                <li>
                  <span>Werden im B-Plan die Kaltluftschneisen geschützt.</span>
                  <SelectButton
                    :options="optionBoolean"
                    v-model="b1q18"
                    optionLabel="name"
                    optionValue="id"
                    :multiple="false"
                    :invalid="!!errors.b1q18"
                  />
                </li>
                <li v-if="b1q18 === 1">
                  <span>In welcher Form?</span>
                  <FloatLabel variant="on" class="w-full">
                    <InputText
                      id="b1q19"
                      v-model="b1q19"
                      aria-describedby="b1q19-help"
                      :invalid="!!errors.b1q19"
                      class="w-full"
                      inputClass="w-full"
                    />
                    <label for="b1q19">Beschreibung</label>
                  </FloatLabel>
                </li>
                <li v-if="b1q18 === 2">
                  <span>Warum nicht?</span>
                  <FloatLabel variant="on" class="w-full">
                    <InputText
                      id="b1q20"
                      v-model="b1q20"
                      aria-describedby="b1q20-help"
                      :invalid="!!errors.b1q20"
                      class="w-full"
                      inputClass="w-full"
                    />
                    <label for="b1q20">Erläuterung</label>
                  </FloatLabel>
                </li>
              </template>
            </ol>

            <div class="flex pt-6 justify-end">
              <Button
                label="Weiter"
                icon="pi pi-arrow-right"
                iconPos="right"
                @click="activateCallback('2')"
              />
            </div>
          </StepPanel>

          <StepPanel v-slot="{ activateCallback }" value="2">
            <ol>
              <li>
                <span>
                  Handelt es sich um ein Konzept/eine Planung (nicht B-Plan), die Auswirkungen auf
                  physische Maßnahmen (z.B. Begrünung, Abriss, Umbau, Installation, Anschaffung von
                  Maschinen, Abholzungen / Fällungen, Flächennutzungsänderungen, Baumaßnahmen etc.)
                  unbekannten Ausmaßes hat?
                </span>
                <SelectButton
                  v-model="b2q1"
                  :options="optionBoolean"
                  optionLabel="name"
                  optionValue="id"
                  :multiple="false"
                  :invalid="!!errors.b2q1"
                />
              </li>
              <template v-if="b2q1 === 1">
                <li>
                  <span
                    >Inwiefern können klimapositive Auswirkungen auf physische Maßnahmen
                    entstehen?</span
                  >
                  <FloatLabel variant="on" class="w-full">
                    <InputText
                      id="b2q2"
                      v-model="b2q2"
                      aria-describedby="t8q2-help"
                      :invalid="!!errors.b2q2"
                      class="w-full"
                      inputClass="w-full"
                    />
                    <label for="b2q2">Erläuterung</label>
                  </FloatLabel>
                </li>

                <li>
                  <span
                    >Inwiefern können klimanegative Auswirkungen auf physische Maßnahmen
                    entstehen?</span
                  >
                  <FloatLabel variant="on" class="w-full">
                    <InputText
                      id="b2q3"
                      v-model="b2q3"
                      aria-describedby="b2q3-help"
                      :invalid="!!errors.b2q3"
                      class="w-full"
                      inputClass="w-full"
                    />
                    <label for="b2q3">Erläuterung</label>
                  </FloatLabel>
                </li>
                <li>
                  <span>Wurden Nachhaltigkeitskriterien mitgedacht?</span>
                  <SelectButton
                    v-model="b2q4"
                    :options="optionBoolean"
                    optionLabel="name"
                    optionValue="id"
                    :multiple="false"
                    :invalid="!!errors.b2q4"
                  />
                </li>
                <li v-if="b2q4 === 1">
                  <span>Inwiefern?</span>
                  <FloatLabel variant="on" class="w-full">
                    <InputText
                      id="b2q5"
                      v-model="b2q5"
                      aria-describedby="b2q5-help"
                      :invalid="!!errors.b2q5"
                      class="w-full"
                      inputClass="w-full"
                    />
                    <label for="b2q5">Beschreibung</label>
                  </FloatLabel>
                </li>
              </template>
            </ol>
            <div class="flex pt-6 justify-between">
              <Button
                label="Zurück"
                severity="secondary"
                icon="pi pi-arrow-left"
                @click="activateCallback('1')"
              />
              <Button label="Speichern" type="submit" icon="pi pi-save" iconPos="right" />
            </div>
          </StepPanel>
        </StepPanels>
      </Stepper>
    </form>
  </div>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue'
import { useForm } from 'vee-validate'
import { schema } from '@/utils/schemas/klimarelevanzpruefungEingabeFb2'
import { createItemSilent, fetchItems, updateItemSilent } from '@/composables/crud'
import Button from 'primevue/button'
import Divider from 'primevue/divider'
import InputText from 'primevue/inputtext'
import FloatLabel from 'primevue/floatlabel'
import SelectButton from 'primevue/selectbutton'
import Stepper from 'primevue/stepper'
import StepList from 'primevue/steplist'
import StepPanels from 'primevue/steppanels'
import Step from 'primevue/step'
import StepPanel from 'primevue/steppanel'
import Message from 'primevue/message'

const isLoading = ref(false)
const optionBoolean = ref()

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

onMounted(async () => {
  isLoading.value = true
  await fetchData()
  if (props.editMode && props.item) {
    setValues(props.item)
  }
  isLoading.value = false
})

const fetchData = async () => {
  optionBoolean.value = await fetchItems('/einstellungen/bool-erweitert')
}

const { defineField, handleSubmit, errors, setValues, values } = useForm({
  validationSchema: schema
})

const hasErrors = computed(() => Object.keys(errors.value).length > 0)

const s1Counter = computed(() => {
  const pos = {}
  let n = 1
  pos.b1q1 = n++
  if (b1q1.value === 1) {
    pos.b1q2 = n++
    if (b1q2.value === 2) pos.b1q3 = n++
    pos.b1q4 = n++
    if (b1q4.value === 2) pos.b1q5 = n++
    pos.b1q6 = n++
    if (b1q6.value === 1) pos.b1q7 = n++
    if (b1q6.value === 2) pos.b1q8 = n++
    pos.b1q9 = n++
    if (b1q9.value === 1) pos.b1q10 = n++
    if (b1q9.value === 2) pos.b1q11 = n++
    pos.b1q12 = n++
    if (b1q12.value === 1) pos.b1q13 = n++
    if (b1q12.value === 2) pos.b1q14 = n++
    pos.b1q15 = n++
    if (b1q15.value === 1) pos.b1q16 = n++
    if (b1q15.value === 2) pos.b1q17 = n++
    pos.b1q18 = n++
    if (b1q18.value === 1) pos.b1q19 = n++
    if (b1q18.value === 2) pos.b1q20 = n++
  }
  return pos
})

const s2Counter = computed(() => {
  const pos = {}
  let n = 1
  pos.b2q1 = n++
  if (b2q1.value === 1) {
    pos.b2q2 = n++
    pos.b2q3 = n++
    pos.b2q4 = n++
    if (b2q4.value === 1) pos.b2q5 = n++
  }
  return pos
})

const dynamicErrorLabels = computed(() => {
  const labels = {}
  for (const [field, n] of Object.entries(s1Counter.value)) {
    labels[field] = `Seite 1, Frage ${n}`
  }
  for (const [field, n] of Object.entries(s2Counter.value)) {
    labels[field] = `Seite 2, Frage ${n}`
  }
  return labels
})

const [b1q1] = defineField('b1q1')
const [b1q2] = defineField('b1q2')
const [b1q3] = defineField('b1q3')
const [b1q4] = defineField('b1q4')
const [b1q5] = defineField('b1q5')
const [b1q6] = defineField('b1q6')
const [b1q7] = defineField('b1q7')
const [b1q8] = defineField('b1q8')
const [b1q9] = defineField('b1q9')
const [b1q10] = defineField('b1q10')
const [b1q11] = defineField('b1q11')
const [b1q12] = defineField('b1q12')
const [b1q13] = defineField('b1q13')
const [b1q14] = defineField('b1q14')
const [b1q15] = defineField('b1q15')
const [b1q16] = defineField('b1q16')
const [b1q17] = defineField('b1q17')
const [b1q18] = defineField('b1q18')
const [b1q19] = defineField('b1q19')
const [b1q20] = defineField('b1q20')
const [b2q1] = defineField('b2q1')
const [b2q2] = defineField('b2q2')
const [b2q3] = defineField('b2q3')
const [b2q4] = defineField('b2q4')
const [b2q5] = defineField('b2q5')

const currentItemId = ref(props.item?.id ?? null)
const alreadySaved = ref(false)

const emit = defineEmits(['update-item', 'add-item'])

const triggerDraftSave = async () => {
  if (alreadySaved.value) return null
  const snapshot = { ...values }
  const hasData = Object.values(snapshot).some((v) => v !== null && v !== undefined)
  if (!hasData) return null
  const draftValues = { ...snapshot, fertig: false }
  if (currentItemId.value) {
    const response = await updateItemSilent({
      model: 'klimarelevanzpruefung/eingabe/fb2',
      modelId: currentItemId.value,
      values: draftValues
    })
    return response ?? null
  } else {
    const response = await createItemSilent({
      model: 'klimarelevanzpruefung/eingabe/fb2',
      values: draftValues
    })
    if (response) {
      currentItemId.value = response.id
      return response
    }
    return null
  }
}

defineExpose({ triggerDraftSave })

const onSubmit = handleSubmit(async (validatedValues) => {
  alreadySaved.value = true
  const fullValues = { ...validatedValues, fertig: true }
  if (currentItemId.value) {
    emit('update-item', { fb: 2, modelId: currentItemId.value, values: fullValues })
  } else {
    emit('add-item', { fb: 2, values: fullValues })
  }
})
</script>

<style scoped>
ol {
  counter-reset: question;
  list-style: none;
  padding-left: 0;
}

ol > li {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  counter-increment: question;
  margin-bottom: 1rem;
}

ol > li > span:first-child::before {
  content: counter(question) '. ';
  font-weight: bold;
}
</style>
