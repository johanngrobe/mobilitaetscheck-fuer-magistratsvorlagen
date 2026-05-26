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
                <span>
                  Handelt es sich um ein Konzept/eine Kampagne, die das Verhalten der Bevölkerung
                  oder der kommunalen Mitarbeitenden in Bezug auf Klimaaspekte positiv beeinflusst?
                </span>
                <SelectButton
                  v-model="c1q1"
                  :options="optionBoolean"
                  optionLabel="name"
                  optionValue="id"
                  :multiple="false"
                  :invalid="!!errors.c1q1"
                />
              </li>
              <Divider />
              <template v-if="c1q1 === 1">
                <li>
                  <span>
                    Handelt es sich um ein Konzept/eine Kampagne, die das Konsumverhalten (Einkauf,
                    Essgewohnheiten, Abfallproduktion etc.) positiv beeinflusst?
                  </span>
                  <SelectButton
                    v-model="c1q2"
                    :options="optionBoolean"
                    optionLabel="name"
                    optionValue="id"
                    :multiple="false"
                    :invalid="!!errors.c1q2"
                  />
                </li>
                <li v-if="c1q2 === 1">
                  <span>Inwiefern?</span>
                  <FloatLabel variant="on" class="w-full">
                    <InputText
                      id="c1q3"
                      v-model="c1q3"
                      aria-describedby="c1q4-help"
                      :invalid="!!errors.c1q3"
                      class="w-full"
                      inputClass="w-full"
                    />
                    <label for="c1q3">Erläuterung</label>
                  </FloatLabel>
                </li>
                <Divider />
                <li>
                  <span>
                    Handelt es sich um ein Konzept/eine Kampagne, die die Mobilität (Nah- oder
                    Fernverkehr, auch Reisen) klimaschonend beeinflusst?
                  </span>
                  <SelectButton
                    v-model="c1q4"
                    :options="optionBoolean"
                    optionLabel="name"
                    optionValue="id"
                    :multiple="false"
                    :invalid="!!errors.c1q4"
                  />
                </li>
                <li v-if="c1q4 === 1">
                  <span>Inwiefern?</span>
                  <FloatLabel variant="on" class="w-full">
                    <InputText
                      id="c1q5"
                      v-model="c1q5"
                      aria-describedby="c1q5-help"
                      :invalid="!!errors.c1q5"
                      class="w-full"
                      inputClass="w-full"
                    />
                    <label for="c1q5">Erläuterung</label>
                  </FloatLabel>
                </li>
                <Divider />
                <li>
                  <span>
                    Handelt es sich um ein Konzept/eine Kampagne, die das Wissen über Klimaschutz
                    oder Klimaanpassung positiv beeinflusst?
                  </span>
                  <SelectButton
                    v-model="c1q6"
                    :options="optionBoolean"
                    optionLabel="name"
                    optionValue="id"
                    :multiple="false"
                    :invalid="!!errors.c1q6"
                  />
                </li>
                <li v-if="c1q6 === 1">
                  <span>Inwiefern?</span>
                  <FloatLabel variant="on" class="w-full">
                    <InputText
                      id="c1q7"
                      v-model="c1q7"
                      aria-describedby="c1q7-help"
                      :invalid="!!errors.c1q7"
                      class="w-full"
                      inputClass="w-full"
                    />
                    <label for="c1q7">Beschreibung</label>
                  </FloatLabel>
                </li>
                <Divider />
                <li>
                  <span>
                    Handelt es sich um ein Konzept/eine Kampagne, die anderweitig klimarelevantes
                    Verhalten (z.B. Entscheidung über EE im Eigenheim) positiv beeinflusst?
                  </span>
                  <SelectButton
                    v-model="c1q8"
                    :options="optionBoolean"
                    optionLabel="name"
                    optionValue="id"
                    :multiple="false"
                    :invalid="!!errors.c1q8"
                  />
                </li>
                <li v-if="c1q8 === 1">
                  <span>Inwiefern?</span>
                  <FloatLabel variant="on" class="w-full">
                    <InputText
                      id="c1q9"
                      v-model="c1q9"
                      aria-describedby="c1q9-help"
                      :invalid="!!errors.c1q9"
                      class="w-full"
                      inputClass="w-full"
                    />
                    <label for="c1q9">Beschreibung</label>
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
                  Handelt es sich um ein Konzept/eine Kampagne, die das Verhalten der Bevölkerung
                  oder der kommunalen Mitarbeitenden in Bezug auf Klimaaspekte negativ beeinflusst?
                </span>
                <SelectButton
                  v-model="c2q1"
                  :options="optionBoolean"
                  optionLabel="name"
                  optionValue="id"
                  :multiple="false"
                  :invalid="!!errors.c2q1"
                />
              </li>
              <template v-if="c2q1 === 1">
                <li>
                  <span>
                    Handelt es sich um ein Konzept/eine Kampagne, die das Konsumverhalten (Einkauf,
                    Essgewohnheiten, Abfallproduktion etc.) negativ beeinflusst?
                  </span>
                  <SelectButton
                    v-model="c2q2"
                    :options="optionBoolean"
                    optionLabel="name"
                    optionValue="id"
                    :multiple="false"
                    :invalid="!!errors.c2q2"
                  />
                </li>
                <li v-if="c2q2 === 1">
                  <span>Inwiefern?</span>
                  <FloatLabel variant="on" class="w-full">
                    <InputText
                      id="c2q3"
                      v-model="c2q3"
                      aria-describedby="c2q3-help"
                      :invalid="!!errors.c2q3"
                      class="w-full"
                      inputClass="w-full"
                    />
                    <label for="c2q3">Erläuterung</label>
                  </FloatLabel>
                </li>
                <Divider />
                <li>
                  <span>
                    Handelt es sich um ein Konzept/eine Kampagne, die die Mobilität (Nah- oder
                    Fernverkehr, auch Reisen) klimaschädigend beeinflusst?
                  </span>
                  <SelectButton
                    v-model="c2q4"
                    :options="optionBoolean"
                    optionLabel="name"
                    optionValue="id"
                    :multiple="false"
                    :invalid="!!errors.c2q4"
                  />
                </li>
                <li v-if="c2q4 === 1">
                  <span>Inwiefern?</span>
                  <FloatLabel variant="on" class="w-full">
                    <InputText
                      id="c2q5"
                      v-model="c2q5"
                      aria-describedby="c2q5-help"
                      :invalid="!!errors.c2q5"
                      class="w-full"
                      inputClass="w-full"
                    />
                    <label for="c2q5">Erläuterung</label>
                  </FloatLabel>
                </li>
                <Divider />
                <li>
                  <span>
                    Handelt es sich um ein Konzept/eine Kampagne, die das Wissen über Klimaschutz
                    oder Klimaanpassung negativ beeinflusst?
                  </span>
                  <SelectButton
                    v-model="c2q6"
                    :options="optionBoolean"
                    optionLabel="name"
                    optionValue="id"
                    :multiple="false"
                    :invalid="!!errors.c2q6"
                  />
                </li>
                <li v-if="c2q6 === 1">
                  <span>Inwiefern?</span>
                  <FloatLabel variant="on" class="w-full">
                    <InputText
                      id="c2q7"
                      v-model="c2q7"
                      aria-describedby="c2q7-help"
                      :invalid="!!errors.c2q7"
                      class="w-full"
                      inputClass="w-full"
                    />
                    <label for="c2q7">Beschreibung</label>
                  </FloatLabel>
                </li>
                <Divider />
                <li>
                  <span>
                    Handelt es sich um ein Konzept/eine Kampagne, die anderweitig klimarelevantes
                    Verhalten (z.B. Entscheidung über EE im Eigenheim) negativ beeinflusst?
                  </span>
                  <SelectButton
                    v-model="c2q8"
                    :options="optionBoolean"
                    optionLabel="name"
                    optionValue="id"
                    :multiple="false"
                    :invalid="!!errors.c2q8"
                  />
                </li>
                <li v-if="c2q8 === 1">
                  <span>Inwiefern?</span>
                  <FloatLabel variant="on" class="w-full">
                    <InputText
                      id="c2q9"
                      v-model="c2q9"
                      aria-describedby="c2q9-help"
                      :invalid="!!errors.c2q9"
                      class="w-full"
                      inputClass="w-full"
                    />
                    <label for="c2q9">Beschreibung</label>
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
import { schema } from '@/utils/schemas/klimarelevanzpruefungEingabeFb3'
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
  pos.c1q1 = n++
  if (c1q1.value === 1) {
    pos.c1q2 = n++
    if (c1q2.value === 1) pos.c1q3 = n++
    pos.c1q4 = n++
    if (c1q4.value === 1) pos.c1q5 = n++
    pos.c1q6 = n++
    if (c1q6.value === 1) pos.c1q7 = n++
    pos.c1q8 = n++
    if (c1q8.value === 1) pos.c1q9 = n++
  }
  return pos
})

const s2Counter = computed(() => {
  const pos = {}
  let n = 1
  pos.c2q1 = n++
  if (c2q1.value === 1) {
    pos.c2q2 = n++
    if (c2q2.value === 1) pos.c2q3 = n++
    pos.c2q4 = n++
    if (c2q4.value === 1) pos.c2q5 = n++
    pos.c2q6 = n++
    if (c2q6.value === 1) pos.c2q7 = n++
    pos.c2q8 = n++
    if (c2q8.value === 1) pos.c2q9 = n++
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

const [c1q1] = defineField('c1q1')
const [c1q2] = defineField('c1q2')
const [c1q3] = defineField('c1q3')
const [c1q4] = defineField('c1q4')
const [c1q5] = defineField('c1q5')
const [c1q6] = defineField('c1q6')
const [c1q7] = defineField('c1q7')
const [c1q8] = defineField('c1q8')
const [c1q9] = defineField('c1q9')
const [c2q1] = defineField('c2q1')
const [c2q2] = defineField('c2q2')
const [c2q3] = defineField('c2q3')
const [c2q4] = defineField('c2q4')
const [c2q5] = defineField('c2q5')
const [c2q6] = defineField('c2q6')
const [c2q7] = defineField('c2q7')
const [c2q8] = defineField('c2q8')
const [c2q9] = defineField('c2q9')

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
      model: 'klimarelevanzpruefung/eingabe/fb3',
      modelId: currentItemId.value,
      values: draftValues
    })
    return response ?? null
  } else {
    const response = await createItemSilent({
      model: 'klimarelevanzpruefung/eingabe/fb3',
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
    emit('update-item', { fb: 3, modelId: currentItemId.value, values: fullValues })
  } else {
    emit('add-item', { fb: 3, values: fullValues })
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
