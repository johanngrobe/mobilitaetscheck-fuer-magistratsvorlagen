<template>
  <div>
    <form @submit.prevent="onSubmit" class="mt-4">
      <Stepper value="1">
        <StepList>
          <Step value="1"></Step>
          <Step value="2"></Step>
          <Step value="3"></Step>
          <Step value="4"></Step>
          <Step value="5"></Step>
          <Step value="6"></Step>
          <Step value="7"></Step>
          <Step value="8"></Step>
        </StepList>
        <StepPanels>
          <StepPanel v-slot="{ activateCallback }" value="1">
            <div>
              <p>Werden im Rahmen des Vorhabens Maschinen oder Materialen angeschafft?</p>
              <SelectButton
                v-model="a1q1"
                :options="optionBoolean"
                optionLabel="name"
                optionValue="id"
                :multiple="false"
                :invalid="!!errors.a1q1"
              />
            </div>
            <div v-if="a1q1 === 1">
              <Divider />
              <div>
                <p>Was wurde hauptsächlich angeschafft?</p>
                <FloatLabel variant="on">
                  <InputText
                    id="a1q2"
                    v-model="a1q2"
                    aria-describedby="a1q2-help"
                    :invalid="!!errors.a1q2"
                    class="w-full"
                    inputClass="w-full"
                  />
                  <label for="a1q2"
                    >z.B. Fahrzeuge, IT-Ausstattung, Möbel, Werkzeuge, Maschinen</label
                  >
                </FloatLabel>
              </div>

              <div>
                <p>
                  Wurde bei der Auswahl auf Nachhaltigkeitskriterien geachtet und sich ganz oder
                  teilweise für eine klimaschonende Ausführung entschieden?
                </p>
                <SelectButton
                  v-model="a1q3"
                  :options="optionBoolean"
                  optionLabel="name"
                  optionValue="id"
                  :multiple="false"
                  :invalid="!!errors.a1q3"
                />
              </div>
              <div v-if="a1q3 === 1">
                <p>Inwiefern?</p>
                <FloatLabel variant="on">
                  <InputText
                    id="a1q4"
                    v-model="a1q4"
                    aria-describedby="a1q4-help"
                    :invalid="!!errors.a1q4"
                    class="w-full"
                    inputClass="w-full"
                  />
                  <label for="a1q4">Begründung</label>
                </FloatLabel>
              </div>
              <div v-if="a1q3 === 2">
                <p>
                  Warum wurde sich nicht für die nachhaltige Variante entschieden? Bitte begründen
                  Sie kurz.
                </p>
                <FloatLabel variant="on">
                  <InputText
                    id="a1q5"
                    v-model="a1q5"
                    aria-describedby="a1q5-help"
                    :invalid="!!errors.a1q5"
                    class="w-full"
                    inputClass="w-full"
                  />
                  <label for="a1q5">Begründung</label>
                </FloatLabel>
              </div>
            </div>
            <div class="flex pt-6 justify-end">
              <Button
                label="Weiter"
                icon="pi pi-arrow-right"
                iconPos="right"
                :disbaled="a2WeiterButtonDisabled"
                @click="activateCallback('2')"
                :disabled="a1WeiterButtonDisabled"
              />
            </div>
          </StepPanel>
          <StepPanel v-slot="{ activateCallback }" value="2">
            <div>
              <p>Werden bauliche Maßnahmen durchgeführt?</p>
              <SelectButton
                v-model="a2q1"
                :options="optionBoolean"
                optionLabel="name"
                optionValue="id"
                :multiple="false"
                :invalid="!!errors.a2q1"
              />
            </div>
            <div v-if="a2q1 === 1">
              <div>
                <p>Worum handelt es sich bei dem Vorhaben?</p>
                <SelectButton
                  v-model="a2q2"
                  :options="optionVorhaben"
                  optionLabel="name"
                  optionValue="id"
                  :multiple="false"
                  :invalid="!!errors.a2q2"
                />
              </div>
              <div v-if="[3, 4].includes(a2q2)">
                <div>
                  <p>Wird durch das Bauvorhaben ein bestehendes Gebäude energetisch aufgewertet?</p>
                  <SelectButton
                    v-model="a2q3"
                    :options="optionBoolean"
                    optionLabel="name"
                    optionValue="id"
                    :multiple="false"
                    :invalid="!!errors.a2q3"
                  />
                </div>
                <div v-if="a2q3 === 1">
                  <div>
                    <p>Welcher Energiestandard wird erreicht?</p>
                    <Select
                      v-model="a2q4"
                      :options="optionVorhaben.find((x) => x.id === 3)?.energiestandards || []"
                      optionLabel="name"
                      optionValue="id"
                      class="w-full"
                      :invalid="!!errors.a2q4"
                      aria-describedby="a2q4-help"
                    />
                  </div>
                  <div v-if="typeof a2q4 === 'number'">
                    <p>Warum wurde sich für den genannten Energiestandard entschieden?</p>
                    <FloatLabel variant="on">
                      <InputText
                        id="a2q5"
                        v-model="a2q5"
                        aria-describedby="a2q4-help"
                        :invalid="!!errors.a2q5"
                        class="w-full"
                        inputClass="w-full"
                      />
                      <label for="a2q5">Begründung</label>
                    </FloatLabel>
                  </div>
                </div>
              </div>
              <div v-if="[1, 2].includes(a2q2)">
                <div>
                  <p>Welcher Energiestandard wird erreicht?</p>
                  <Select
                    v-model="a2q6"
                    :options="optionVorhaben.find((x) => x.id === 1)?.energiestandards || []"
                    optionLabel="name"
                    optionValue="id"
                    class="w-full"
                    :invalid="!!errors.a2q6"
                    aria-describedby="a2q6-help"
                  />
                </div>
                <div v-if="typeof a2q6 === 'number'">
                  <p>Warum wurde sich für den genannten Energiestandard entschieden?</p>
                  <FloatLabel variant="on">
                    <InputText
                      id="a2q7"
                      v-model="a2q7"
                      aria-describedby="a2q7-help"
                      :invalid="!!errors.a2q7"
                      class="w-full"
                      inputClass="w-full"
                    />
                    <label for="a2q7">Begründung</label>
                  </FloatLabel>
                </div>
              </div>
              <div>
                <p>
                  Wird bei dem Bauvorhaben darauf geachtet, dass Niederschlag möglichst vor Ort
                  versickert?
                </p>
                <SelectButton
                  v-model="a2q8"
                  :options="optionBoolean"
                  optionLabel="name"
                  optionValue="id"
                  :multiple="false"
                  :invalid="!!errors.a2q8"
                />
              </div>
              <div v-if="a2q8 === false">
                <p>Warum nicht?</p>
                <FloatLabel variant="on">
                  <InputText
                    id="a2q9"
                    v-model="a2q9"
                    aria-describedby="a2q9-help"
                    :invalid="!!errors.a2q9"
                    class="w-full"
                    inputClass="w-full"
                  />
                  <label for="a2q9">Begründung</label>
                </FloatLabel>
              </div>
              <div>
                <p>
                  Wird bei dem Bauvorhaben darauf geachtet, dass Kaltluftströme ungehindert fließen
                  können?
                </p>
                <SelectButton
                  v-model="a2q10"
                  :options="optionBoolean"
                  optionLabel="name"
                  optionValue="id"
                  :multiple="false"
                  :invalid="!!errors.a2q10"
                />
              </div>
              <div v-if="a2q10 === 2">
                <p>Warum nicht?</p>
                <FloatLabel variant="on">
                  <InputText
                    id="a2q11"
                    v-model="a2q11"
                    aria-describedby="a2q11-help"
                    :invalid="!!errors.a2q11"
                    class="w-full"
                    inputClass="w-full"
                  />
                  <label for="a2q11">Begründung</label>
                </FloatLabel>
              </div>
              <div>
                <p>
                  Wird bei dem Vorhaben durch geeignete Maßnahmen der örtlichen Hitzebildung
                  vorgebeugt? (z. B. Verschattungselemente oder Begrünung)
                </p>
                <SelectButton
                  v-model="a2q12"
                  :options="optionBoolean"
                  optionLabel="name"
                  optionValue="id"
                  :multiple="false"
                  :invalid="!!errors.a2q12"
                />
              </div>
              <div v-if="a2q12 === false">
                <p>Warum nicht?</p>
                <FloatLabel variant="on">
                  <InputText
                    id="a2q13"
                    v-model="a2q13"
                    aria-describedby="a2q13-help"
                    :invalid="!!errors.a2q11"
                    class="w-full"
                    inputClass="w-full"
                  />
                  <label for="a2q13">Begründung</label>
                </FloatLabel>
              </div>
              <div>
                <p>Wurde bei den Vergabekriterien auf Nachhaltigkeit geachtet?</p>
                <SelectButton
                  v-model="a2q14"
                  :options="optionBoolean"
                  optionLabel="name"
                  optionValue="id"
                  :multiple="false"
                  :invalid="!!errors.a2q14"
                />
              </div>
              <div v-if="a2q14 === false">
                <p>Warum nicht?</p>
                <FloatLabel variant="on">
                  <InputText
                    id="a2q15"
                    v-model="a2q15"
                    aria-describedby="a2q15-help"
                    :invalid="!!errors.a2q15"
                    class="w-full"
                    inputClass="w-full"
                  />
                  <label for="a2q15">Begründung</label>
                </FloatLabel>
              </div>
            </div>
            <div class="flex pt-6 justify-between">
              <Button
                label="Zurück"
                severity="secondary"
                icon="pi pi-arrow-left"
                @click="activateCallback('1')"
              />
              <Button
                label="Weiter"
                icon="pi pi-arrow-right"
                iconPos="right"
                @click="activateCallback('3')"
              />
            </div>
          </StepPanel>
          <StepPanel v-slot="{ activateCallback }" value="3">
            <div>
              <div>
                <p>Werden bei dem Vorhaben Flächen neu versiegelt?</p>
                <SelectButton
                  v-model="a3q1"
                  :options="optionBoolean"
                  optionLabel="name"
                  optionValue="id"
                  :multiple="false"
                  :invalid="!!errors.a3q1"
                />
              </div>
              <div v-if="a3q1 === true">
                <div>
                  <p>In welchem Umfang werden Flächen neu versiegelt? (Angabe in m^2)</p>
                  <FloatLabel variant="on">
                    <InputNumber
                      id="a3q2"
                      v-model="a3q2"
                      :min="0"
                      :step="1"
                      mode="decimal"
                      :useGrouping="false"
                      aria-describedby="a3q2-help"
                      :invalid="!!errors.a3q2"
                      class="w-full"
                      inputClass="w-full"
                    />
                    <label for="a3q2">Angabe in m²</label>
                  </FloatLabel>
                </div>
                <div>
                  <p>Wie wurde die Fläche bisher genutzt?</p>
                  <FloatLabel variant="on">
                    <InputText
                      id="a3q3"
                      v-model="a3q3"
                      aria-describedby="a3q3-help"
                      :invalid="!!errors.a3q3"
                      class="w-full"
                      inputClass="w-full"
                    />
                    <label for="a3q3">Begründung</label>
                  </FloatLabel>
                </div>
                <div>
                  <p>Sind für die Versiegelung Ausgleichsmaßnahmen vorgesehen?</p>
                  <SelectButton
                    v-model="a3q4"
                    :options="optionBoolean"
                    optionLabel="name"
                    optionValue="id"
                    :multiple="false"
                    :invalid="!!errors.a3q4"
                  />
                </div>
                <div v-if="a3q4 === 1">
                  <p>In welcher Form und Umfang sind die Ausgleichsmaßnahmen vorgesehen?</p>
                  <FloatLabel variant="on">
                    <InputText
                      id="a3q5"
                      v-model="a3q5"
                      aria-describedby="a3q5-help"
                      :invalid="!!errors.a3q5"
                      class="w-full"
                      inputClass="w-full"
                    />
                    <label for="a3q5">Begründung</label>
                  </FloatLabel>
                </div>
                <div v-if="a3q4 === 2">
                  <p>Warum nicht?</p>
                  <FloatLabel variant="on">
                    <InputText
                      id="a3q6"
                      v-model="a3q6"
                      aria-describedby="a3q6-help"
                      :invalid="!!errors.a3q6"
                      class="w-full"
                      inputClass="w-full"
                    />
                    <label for="a3q6">Begründung</label>
                  </FloatLabel>
                </div>
              </div>
            </div>
            <div class="flex pt-6 justify-between">
              <Button
                label="Zurück"
                severity="secondary"
                icon="pi pi-arrow-left"
                @click="activateCallback('2')"
              />
              <Button
                label="Weiter"
                icon="pi pi-arrow-right"
                iconPos="right"
                @click="activateCallback('4')"
              />
            </div>
          </StepPanel>
          <StepPanel v-slot="{ activateCallback }" value="4">
            <div>
              <div>
                <p>Werden bei dem Vorhaben Flächen entsiegelt?</p>
                <SelectButton
                  v-model="a4q1"
                  :options="optionBoolean"
                  optionLabel="name"
                  optionValue="id"
                  :multiple="false"
                  :invalid="!!errors.a4q1"
                />
              </div>
              <div v-if="a4q1 === 1">
                <div>
                  <p>In welchem Umfang werden Flächen entsiegelt? (Angabe in m^2)</p>
                  <FloatLabel variant="on">
                    <InputNumber
                      id="a4q2"
                      v-model="a4q2"
                      :min="0"
                      :step="1"
                      mode="decimal"
                      :useGrouping="false"
                      aria-describedby="a4q2-help"
                      :invalid="!!errors.a4q2"
                      class="w-full"
                      inputClass="w-full"
                    />
                    <label for="a4q2">Angabe in m²</label>
                  </FloatLabel>
                </div>

                <div>
                  <p>Wie wurde die Fläche bisher genutzt?</p>
                  <FloatLabel variant="on">
                    <InputText
                      id="a4q3"
                      v-model="a4q3"
                      aria-describedby="a4q3-help"
                      :invalid="!!errors.a4q3"
                      class="w-full"
                      inputClass="w-full"
                    />
                    <label for="a4q3">Begründung</label>
                  </FloatLabel>
                </div>
                <div v-if="a4q3">
                  <p>
                    Wird die Entsiegelung als Ausgleichsmaßnahme für ein anderes Vorhaben
                    durchgeführt?
                  </p>
                  <SelectButton
                    v-model="a4q4"
                    :options="optionBoolean"
                    optionLabel="name"
                    optionValue="id"
                    :multiple="false"
                    :invalid="!!errors.a4q4"
                  />
                </div>
              </div>
            </div>
            <div class="flex pt-6 justify-between">
              <Button
                label="Zurück"
                severity="secondary"
                icon="pi pi-arrow-left"
                @click="activateCallback('3')"
              />
              <Button
                label="Weiter"
                icon="pi pi-arrow-right"
                iconPos="right"
                @click="activateCallback('5')"
              />
            </div>
          </StepPanel>
          <StepPanel v-slot="{ activateCallback }" value="5">
            <div>
              <div>
                <p>
                  Werden bei dem Vorhaben Grünflächen mit CO2-bindender Funktion aufgewertet? (Z.B.
                  durch die Pflanung von Bäumen und Sträuchern)
                </p>
                <SelectButton
                  v-model="a5q1"
                  :options="optionBoolean"
                  optionLabel="name"
                  optionValue="id"
                  :multiple="false"
                  :invalid="!!errors.a5q1"
                />
              </div>
              <div v-if="a5q1 === 1">
                <div>
                  <p>In welchem Umfang werden die Grünflächen aufgewertet?</p>
                  <FloatLabel variant="on">
                    <InputText
                      id="a5q2"
                      v-model="a5q2"
                      aria-describedby="a5q2-help"
                      :invalid="!!errors.a5q2"
                      class="w-full"
                      inputClass="w-full"
                    />
                    <label for="a5q2">Begründung</label>
                  </FloatLabel>
                </div>
                <div>
                  <div>
                    <p>Wie wurde die Fläche bisher genutzt?</p>
                    <FloatLabel variant="on">
                      <InputText
                        id="a5q3"
                        v-model="a5q3"
                        aria-describedby="a5q3-help"
                        :invalid="!!errors.a5q3"
                        class="w-full"
                        inputClass="w-full"
                      />
                      <label for="a5q3">Begründung</label>
                    </FloatLabel>
                  </div>
                  <div>
                    <p>
                      Wird die Maßnahme als Ausgleichsmaßnahme für ein anderes Vorhaben
                      durchgeführt?
                    </p>
                    <SelectButton
                      v-model="a5q4"
                      :options="optionBoolean"
                      optionLabel="name"
                      optionValue="id"
                      :multiple="false"
                      :invalid="!!errors.a5q4"
                    />
                  </div>
                </div>
              </div>
            </div>
            <div class="flex pt-6 justify-between">
              <Button
                label="Zurück"
                severity="secondary"
                icon="pi pi-arrow-left"
                @click="activateCallback('4')"
              />
              <Button
                label="Weiter"
                icon="pi pi-arrow-right"
                iconPos="right"
                @click="activateCallback('6')"
              />
            </div>
          </StepPanel>
          <StepPanel v-slot="{ activateCallback }" value="6">
            <div>
              <div>
                <p>Wird im Rahmen des Vorhabens eine bestehende Begrünung entfernt?</p>
                <SelectButton
                  v-model="a6q1"
                  :options="optionBoolean"
                  optionLabel="name"
                  optionValue="id"
                  :multiple="false"
                  :invalid="!!errors.a6q1"
                />
              </div>
              <div v-if="a6q1 === 1">
                <div>
                  <p>In welchem Umfang?</p>
                  <FloatLabel variant="on">
                    <InputText
                      id="a6q2"
                      v-model="a6q2"
                      aria-describedby="a6q2-help"
                      :invalid="!!errors.a6q2"
                      class="w-full"
                      inputClass="w-full"
                    />
                    <label for="a6q2">Begründung</label>
                  </FloatLabel>
                </div>
                <div>
                  <div>
                    <p>Sind Ausgleichsmaßnahmen vorgesehen?</p>
                    <SelectButton
                      v-model="a6q3"
                      :options="optionBoolean"
                      optionLabel="name"
                      optionValue="id"
                      :multiple="false"
                      :invalid="!!errors.a6q3"
                    />
                  </div>
                  <div v-if="a6q3 === 1">
                    <p>In welcher Form und Umfang sind die Ausgleichsmaßnahmen vorgesehen?</p>
                    <FloatLabel variant="on">
                      <InputText
                        id="a6q4"
                        v-model="a6q4"
                        aria-describedby="a6q4-help"
                        :invalid="!!errors.a6q4"
                        class="w-full"
                        inputClass="w-full"
                      />
                      <label for="a6q4">Begründung</label>
                    </FloatLabel>
                  </div>
                  <div v-if="a6q3 === 2">
                    <p>Warum nicht?</p>
                    <FloatLabel variant="on">
                      <InputText
                        id="a6q5"
                        v-model="a6q5"
                        aria-describedby="a6q5-help"
                        :invalid="!!errors.a6q5"
                        class="w-full"
                        inputClass="w-full"
                      />
                      <label for="a6q5">Begründung</label>
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
                @click="activateCallback('5')"
              />
              <Button
                label="Weiter"
                icon="pi pi-arrow-right"
                iconPos="right"
                @click="activateCallback('7')"
              />
            </div>
          </StepPanel>
          <StepPanel v-slot="{ activateCallback }" value="7">
            <div>
              <div>
                <p>
                  Hat das Vorhaben in anderer Weise klimaschädliche Wirkung? (z.B. Kraftwerkbau,
                  Abwärme, Wasserbedarf…)
                </p>
                <SelectButton
                  v-model="a7q1"
                  :options="optionBoolean"
                  optionLabel="name"
                  optionValue="id"
                  :multiple="false"
                  :invalid="!!errors.a7q1"
                />
              </div>
              <div v-if="a7q1 === true">
                <p>Inwiefern?</p>
                <FloatLabel variant="on">
                  <InputText
                    id="a7q2"
                    v-model="a7q2"
                    aria-describedby="a7q2-help"
                    :invalid="!!errors.a7q2"
                    class="w-full"
                    inputClass="w-full"
                  />
                  <label for="a7q2">Begründung</label>
                </FloatLabel>
              </div>
            </div>
            <div class="flex pt-6 justify-between">
              <Button
                label="Zurück"
                severity="secondary"
                icon="pi pi-arrow-left"
                @click="activateCallback('6')"
              />
              <Button
                label="Weiter"
                icon="pi pi-arrow-right"
                iconPos="right"
                @click="activateCallback('8')"
              />
            </div>
          </StepPanel>
          <StepPanel v-slot="{ activateCallback }" value="8">
            <div>
              <div>
                <p>
                  Hat das Vorhaben in anderer Weise klimaschützende / Klimaresilienz fördernde
                  Wirkung? (z.B. Wasserretention, Energiesparmaßnahme, Verkehrsregulierung)
                </p>
                <SelectButton
                  v-model="a8q1"
                  :options="optionBoolean"
                  optionLabel="name"
                  optionValue="id"
                  :multiple="false"
                  :invalid="!!errors.a8q1"
                />
              </div>
              <div v-if="a8q1 === true">
                <p>Inwiefern?</p>
                <FloatLabel variant="on">
                  <InputText
                    id="a8q2"
                    v-model="a8q2"
                    aria-describedby="a8q2-help"
                    :invalid="!!errors.a8q2"
                    class="w-full"
                    inputClass="w-full"
                  />
                  <label for="a8q2">Begründung</label>
                </FloatLabel>
              </div>
            </div>
            <div class="flex pt-6 justify-between">
              <Button
                label="Zurück"
                severity="secondary"
                icon="pi pi-arrow-left"
                @click="activateCallback('6')"
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
import { computed, onMounted, ref } from 'vue'
import { useForm } from 'vee-validate'
import { schema } from '@/utils/schemas/klimarelevanzpruefungEingabeFb1'
import { fetchItems } from '@/composables/crud'
// import ToggleSwitch from 'primevue/toggleswitch'
import Button from 'primevue/button'
import Divider from 'primevue/divider'
import InputText from 'primevue/inputtext'
import InputNumber from 'primevue/inputnumber'
import FloatLabel from 'primevue/floatlabel'
import Select from 'primevue/select'
import SelectButton from 'primevue/selectbutton'
import Stepper from 'primevue/stepper'
import StepList from 'primevue/steplist'
import StepPanels from 'primevue/steppanels'
import Step from 'primevue/step'
import StepPanel from 'primevue/steppanel'

const isLoading = ref(false)
const optionBoolean = ref()
const optionVorhaben = ref()

onMounted(async () => {
  isLoading.value = true
  await fetchData()
  isLoading.value = false
})

const fetchData = async () => {
  optionBoolean.value = await fetchItems('/einstellungen/bool-erweitert')
  optionVorhaben.value = await fetchItems('/klimarelevanzpruefung/vorhaben')
}

const { defineField, handleSubmit, errors } = useForm({
  validationSchema: schema
})

const [a1q1] = defineField('a1q1')
const [a1q2] = defineField('a1q2')
const [a1q3] = defineField('a1q3')
const [a1q4] = defineField('a1q4')
const [a1q5] = defineField('a1q5')
const [a2q1] = defineField('a2q1')
const [a2q2] = defineField('a2q2')
const [a2q3] = defineField('a2q3')
const [a2q4] = defineField('a2q4')
const [a2q5] = defineField('a2q5')
const [a2q6] = defineField('a2q6')
const [a2q7] = defineField('a2q7')
const [a2q8] = defineField('a2q8')
const [a2q9] = defineField('a2q9')
const [a2q10] = defineField('a2q10')
const [a2q11] = defineField('a2q11')
const [a2q12] = defineField('a2q12')
const [a2q13] = defineField('a2q13')
const [a2q14] = defineField('a2q14')
const [a2q15] = defineField('a2q15')
const [a3q1] = defineField('a3q1')
const [a3q2] = defineField('a3q2')
const [a3q3] = defineField('a3q3')
const [a3q4] = defineField('a3q4')
const [a3q5] = defineField('a3q5')
const [a3q6] = defineField('a3q6')
const [a4q1] = defineField('a4q1')
const [a4q2] = defineField('a4q2')
const [a4q3] = defineField('a4q3')
const [a4q4] = defineField('a4q4')
const [a5q1] = defineField('a5q1')
const [a5q2] = defineField('a5q2')
const [a5q3] = defineField('a5q3')
const [a5q4] = defineField('a5q4')
const [a6q1] = defineField('a6q1')
const [a6q2] = defineField('a6q2')
const [a6q3] = defineField('a6q3')
const [a6q4] = defineField('a6q4')
const [a6q5] = defineField('a6q5')
const [a7q1] = defineField('a7q1')
const [a7q2] = defineField('a7q2')
const [a8q1] = defineField('a8q1')
const [a8q2] = defineField('a8q2')

const a1WeiterButtonDisabled = computed(() => {
  if (
    [2, 3].includes(a1q1.value) ||
    (a1q2.value && (a1q4.value || a1q5.value || a1q3.value === 3) && a1q3.value)
  ) {
    return false
  }
  return true
})

const a2WeiterButtonDisabled = computed(() => {
  if (a2q1.value === 2) {
    return false
  }
  if (a2q1.value === 1) {
    if (
      a2q2.value &&
      (([3, 4].includes(a2q2.value) &&
        a2q3.value &&
        ((a2q4.value && a2q5.value) || a2q4.value === 1)) ||
        ([1, 2].includes(a2q2.value) && a2q6.value && (a2q7.value || a2q6.value === 5))) &&
      a2q8.value &&
      (a2q8.value === 1 || a2q9.value) &&
      a2q10.value &&
      (a2q10.value === 1 || a2q11.value) &&
      a2q12.value &&
      (a2q12.value === 1 || a2q13.value) &&
      a2q14.value &&
      (a2q14.value === 1 || a2q15.value)
    ) {
      return false
    }
  }
  return true
})

const onSubmit = handleSubmit((values) => {
  console.log('Form Values:', values)
})
</script>

<style></style>
