<template>
  <div>
    <form @submit.prevent="onSubmit" class="mt-4">
      <Stepper value="1">
        <StepList>
          <Step value="1"></Step>
          <Step value="2"></Step>
        </StepList>
        <StepPanels>
          <StepPanel v-slot="{ activateCallback }" value="1">
            <div>
              <p>Handelt es sich um einen Bebauungsplan?</p>
              <SelectButton
                v-model="b1q1"
                :options="optionBoolean"
                optionLabel="name"
                optionValue="id"
                :multiple="false"
                :invalid="!!errors.b1q1"
              />
            </div>
            <Divider />
            <div v-if="b1q1 === 1">
              <div>
                <p>Wurde im B-Plan eine PV-Pflicht verankert?</p>
                <SelectButton
                  v-model="b1q2"
                  :options="optionBoolean"
                  optionLabel="name"
                  optionValue="id"
                  :multiple="false"
                  :invalid="!!errors.b1q2"
                />
              </div>
              <div v-if="b1q2 === 2">
                <div>
                  <p>Warum nicht?</p>
                  <FloatLabel variant="on">
                    <InputText
                      id="b1q3"
                      v-model="b1q3"
                      aria-describedby="b1q4-help"
                      :invalid="!!errors.b1q3"
                      class="w-full"
                      inputClass="w-full"
                    />
                    <label for="b1q3">Begründung</label>
                  </FloatLabel>
                </div>
              </div>
              <Divider />
              <div>
                <p>Wurde im B-Plan eine Gründachpflicht verankert?</p>
                <SelectButton
                  v-model="b1q4"
                  :options="optionBoolean"
                  optionLabel="name"
                  optionValue="id"
                  :multiple="false"
                  :invalid="!!errors.b1q4"
                />
              </div>
              <div v-if="b1q4 === 2">
                <div>
                  <p>Warum nicht?</p>
                  <FloatLabel variant="on">
                    <InputText
                      id="b1q5"
                      v-model="b1q5"
                      aria-describedby="b1q5-help"
                      :invalid="!!errors.b1q5"
                      class="w-full"
                      inputClass="w-full"
                    />
                    <label for="b1q5">Begründung</label>
                  </FloatLabel>
                </div>
              </div>
              <Divider />
              <div>
                <p>
                  Wurde im B-Plan eine nachhaltige Regenwasserbewirtschaftung verankert? (z. B.
                  Sickergruben, Zisternen, Rückhaltebecken etc.)
                </p>
                <SelectButton
                  v-model="b1q6"
                  :options="optionBoolean"
                  optionLabel="name"
                  optionValue="id"
                  :multiple="false"
                  :invalid="!!errors.b1q6"
                />
              </div>
              <div v-if="b1q6 === 1">
                <div>
                  <p>In welcher Form?</p>
                  <FloatLabel variant="on">
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
                </div>
              </div>
              <div v-if="b1q6 === 2">
                <div>
                  <p>Warum nicht?</p>
                  <FloatLabel variant="on">
                    <InputText
                      id="b1q8"
                      v-model="b1q8"
                      aria-describedby="b1q8-help"
                      :invalid="!!errors.b1q8"
                      class="w-full"
                      inputClass="w-full"
                    />
                    <label for="b1q8">Begründung</label>
                  </FloatLabel>
                </div>
              </div>
              <Divider />
              <div>
                <p>Wurden im B-Plan weitere wasserrückhaltende Maßnahmen verankert?</p>
                <SelectButton
                  v-model="b1q9"
                  :options="optionBoolean"
                  optionLabel="name"
                  optionValue="id"
                  :multiple="false"
                  :invalid="!!errors.b1q9"
                />
              </div>
              <div v-if="b1q9 === 1">
                <div>
                  <p>In welcher Form?</p>
                  <FloatLabel variant="on">
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
                </div>
              </div>
              <div v-if="b1q9 === 2">
                <div>
                  <p>Warum nicht?</p>
                  <FloatLabel variant="on">
                    <InputText
                      id="b1q11"
                      v-model="b1q11"
                      aria-describedby="b1q11-help"
                      :invalid="!!errors.b1q11"
                      class="w-full"
                      inputClass="w-full"
                    />
                    <label for="b1q11">Begründung</label>
                  </FloatLabel>
                </div>
              </div>
              <Divider />
              <div>
                <p>
                  Wurden im B-Plan weitere hitzepräventive Maßnahmen verankert? (z.B. durch
                  Begrünung)
                </p>
                <SelectButton
                  v-model="b1q12"
                  :options="optionBoolean"
                  optionLabel="name"
                  optionValue="id"
                  :multiple="false"
                  :invalid="!!errors.b1q12"
                />
              </div>
              <div v-if="b1q12 === 1">
                <div>
                  <p>In welcher Form?</p>
                  <FloatLabel variant="on">
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
                </div>
              </div>
              <div v-if="b1q12 === 2">
                <div>
                  <p>Warum nicht?</p>
                  <FloatLabel variant="on">
                    <InputText
                      id="b1q14"
                      v-model="b1q14"
                      aria-describedby="b1q14-help"
                      :invalid="!!errors.b1q14"
                      class="w-full"
                      inputClass="w-full"
                    />
                    <label for="b1q14">Begründung</label>
                  </FloatLabel>
                </div>
              </div>
              <Divider />
              <div>
                <p>
                  Wurde im B-Plan ein Fokus auf platzsparendes Bauen gelegt und möglichst wenig
                  Fläche wird versiegelt?
                </p>
                <SelectButton
                  v-model="b1q15"
                  :options="optionBoolean"
                  optionLabel="name"
                  optionValue="id"
                  :multiple="false"
                  :invalid="!!errors.b1q15"
                />
              </div>
              <div v-if="b1q15 === 1">
                <div>
                  <p>In welcher Form?</p>
                  <FloatLabel variant="on">
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
                </div>
              </div>
              <div v-if="b1q15 === 2">
                <div>
                  <p>Warum nicht?</p>
                  <FloatLabel variant="on">
                    <InputText
                      id="b1q17"
                      v-model="b1q17"
                      aria-describedby="b1q17-help"
                      :invalid="!!errors.b1q17"
                      class="w-full"
                      inputClass="w-full"
                    />
                    <label for="b1q17">Begründung</label>
                  </FloatLabel>
                </div>
              </div>
              <Divider />
              <div>
                <p>Werden im B-Plan die Kaltluftschneisen geschützt.</p>
                <SelectButton
                  :options="optionBoolean"
                  optionLabel="name"
                  optionValue="id"
                  :multiple="false"
                  :invalid="!!errors.b1q18"
                />
              </div>
              <div v-if="b1q18 === 1">
                <div>
                  <p>In welcher Form?</p>
                  <FloatLabel variant="on">
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
                </div>
              </div>
              <div v-if="b1q18 === 2">
                <div>
                  <p>Warum nicht?</p>
                  <FloatLabel variant="on">
                    <InputText
                      id="b1q20"
                      v-model="b1q20"
                      aria-describedby="b1q20-help"
                      :invalid="!!errors.b1q20"
                      class="w-full"
                      inputClass="w-full"
                    />
                    <label for="b1q20">Begründung</label>
                  </FloatLabel>
                </div>
              </div>
            </div>

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
            <div>
              <div>
                <p>
                  Handelt es sich um ein Konzept/eine Planung (nicht B-Plan), die Auswirkungen auf
                  physische Maßnahmen (z.B. Begrünung, Abriss, Umbau, Installation, Anschaffung von
                  Maschinen, Abholzungen / Fällungen, Flächennutzungsänderungen, Baumaßnahmen etc.)
                  unbekannten Ausmaßes hat?
                </p>
                <SelectButton
                  v-model="b2q1"
                  :options="optionBoolean"
                  optionLabel="name"
                  optionValue="id"
                  :multiple="false"
                  :invalid="!!errors.b2q1"
                />
              </div>
              <div v-if="b2q1 === 1">
                <div>
                  <p>Inwiefern können positive Auswirkungen auf physische Maßnahmen entstehen?</p>
                  <FloatLabel variant="on">
                    <InputText
                      id="b2q2"
                      v-model="b2q2"
                      aria-describedby="t8q2-help"
                      :invalid="!!errors.b2q2"
                      class="w-full"
                      inputClass="w-full"
                    />
                    <label for="b2q2">Begründung</label>
                  </FloatLabel>
                </div>

                <div>
                  <p>Inwiefern können negative Auswirkungen auf physische Maßnahmen entstehen?</p>
                  <FloatLabel variant="on">
                    <InputText
                      id="b2q3"
                      v-model="b2q3"
                      aria-describedby="b2q3-help"
                      :invalid="!!errors.b2q3"
                      class="w-full"
                      inputClass="w-full"
                    />
                    <label for="b2q3">Begründung</label>
                  </FloatLabel>
                </div>
                <div>
                  <p>Wurden Nachhaltigkeitskriterien mitgedacht?</p>
                  <SelectButton
                    v-model="b2q4"
                    :options="optionBoolean"
                    optionLabel="name"
                    optionValue="id"
                    :multiple="false"
                    :invalid="!!errors.b2q4"
                  />
                </div>
                <div v-if="b2q4 === 1">
                  <div>
                    <p>Inwiefern?</p>
                    <FloatLabel variant="on">
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
                  </div>
                </div>
              </div>
            </div>
            <div class="flex pt-6 justify-between">
              <Button
                label="Zurück"
                severity="secondary"
                icon="pi pi-arrow-left"
                @click="activateCallback('1')"
              />
              <Button label="Speichern" icon="pi pi-save" iconPos="right" />
            </div>
          </StepPanel>
        </StepPanels>
      </Stepper>
    </form>
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import { useForm } from 'vee-validate'
import { schema } from '@/utils/schemas/klimarelevanzpruefungEingabeFb2'
import { fetchItems } from '@/composables/crud'
// import ToggleSwitch from 'primevue/toggleswitch'
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

const isLoading = ref(false)
const optionBoolean = ref()

onMounted(async () => {
  isLoading.value = true
  await fetchData()
  isLoading.value = false
})

const fetchData = async () => {
  optionBoolean.value = await fetchItems('/einstellungen/bool-erweitert')
}

const { defineField, handleSubmit, errors } = useForm({
  validationSchema: schema
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

const onSubmit = handleSubmit((values) => {
  console.log('Form Values:', values)
})
</script>

<style></style>
