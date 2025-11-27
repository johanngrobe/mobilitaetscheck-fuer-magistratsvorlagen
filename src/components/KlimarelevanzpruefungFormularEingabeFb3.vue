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
              <p>
                Handelt es sich um ein Konzept/eine Kampagne, die das Verhalten der Bevölkerung oder
                der kommunalen Mitarbeitenden in Bezug auf Klimaaspekte positiv beeinflusst?
              </p>
              <SelectButton
                v-model="c1q1"
                :options="optionBoolean"
                optionLabel="name"
                optionValue="id"
                :multiple="false"
                :invalid="!!errors.c1q1"
              />
            </div>
            <Divider />
            <div v-if="c1q1 === 1">
              <div>
                <p>
                  Handelt es sich um ein Konzept/eine Kampagne, die das Konsumverhalten (Einkauf,
                  Essgewohnheiten, Abfallproduktion etc.) positiv beeinflusst?
                </p>
                <SelectButton
                  v-model="c1q2"
                  :options="optionBoolean"
                  optionLabel="name"
                  optionValue="id"
                  :multiple="false"
                  :invalid="!!errors.c1q2"
                />
              </div>
              <div v-if="c1q2 === 2">
                <div>
                  <p>Inwiefern</p>
                  <FloatLabel variant="on">
                    <InputText
                      id="c1q3"
                      v-model="c1q3"
                      aria-describedby="c1q4-help"
                      :invalid="!!errors.c1q3"
                      class="w-full"
                      inputClass="w-full"
                    />
                    <label for="c1q3">Begründung</label>
                  </FloatLabel>
                </div>
              </div>
              <Divider />
              <div>
                <p>
                  Handelt es sich um ein Konzept/eine Kampagne, die die Mobilität (Nah- oder
                  Fernverkehr, auch Reisen) klimaschonend beeinflusst?
                </p>
                <SelectButton
                  v-model="c1q4"
                  :options="optionBoolean"
                  optionLabel="name"
                  optionValue="id"
                  :multiple="false"
                  :invalid="!!errors.c1q4"
                />
              </div>
              <div v-if="c1q4 === 1">
                <div>
                  <p>Inwiefern?</p>
                  <FloatLabel variant="on">
                    <InputText
                      id="c1q5"
                      v-model="c1q5"
                      aria-describedby="c1q5-help"
                      :invalid="!!errors.c1q5"
                      class="w-full"
                      inputClass="w-full"
                    />
                    <label for="c1q5">Begründung</label>
                  </FloatLabel>
                </div>
              </div>
              <Divider />
              <div>
                <p>
                  Handelt es sich um ein Konzept/eine Kampagne, die das Wissen über Klimaschutz oder
                  Klimaanpassung positiv beeinflusst?
                </p>
                <SelectButton
                  v-model="c1q6"
                  :options="optionBoolean"
                  optionLabel="name"
                  optionValue="id"
                  :multiple="false"
                  :invalid="!!errors.c1q6"
                />
              </div>
              <div v-if="c1q6 === 1">
                <div>
                  <p>Inwiefern?</p>
                  <FloatLabel variant="on">
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
                </div>
              </div>
              <Divider />
              <div>
                <p>
                  Handelt es sich um ein Konzept/eine Kampagne, die anderweitig klimarelevantes
                  Verhalten (z.B. Entscheidung über EE im Eigenheim) positiv beeinflusst?
                </p>
                <SelectButton
                  v-model="c1q8"
                  :options="optionBoolean"
                  optionLabel="name"
                  optionValue="id"
                  :multiple="false"
                  :invalid="!!errors.c1q8"
                />
              </div>
              <div v-if="c1q8 === true">
                <div>
                  <p>Inwiefern?</p>
                  <FloatLabel variant="on">
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
                  Handelt es sich um ein Konzept/eine Kampagne, die das Verhalten der Bevölkerung
                  oder der kommunalen Mitarbeitenden in Bezug auf Klimaaspekte negativ beeinflusst?
                </p>
                <SelectButton
                  v-model="c2q1"
                  :options="optionBoolean"
                  optionLabel="name"
                  optionValue="id"
                  :multiple="false"
                  :invalid="!!errors.c2q1"
                />
              </div>
              <div v-if="c2q1 === 1">
                <div>
                  <p>
                    Handelt es sich um ein Konzept/eine Kampagne, die das Konsumverhalten (Einkauf,
                    Essgewohnheiten, Abfallproduktion etc.) negativ beeinflusst?
                  </p>
                  <SelectButton
                    v-model="c2q2"
                    :options="optionBoolean"
                    optionLabel="name"
                    optionValue="id"
                    :multiple="false"
                    :invalid="!!errors.c2q2"
                  />
                </div>
                <div v-if="c2q2 === 1">
                  <div>
                    <p>Inwiefern?</p>
                    <FloatLabel variant="on">
                      <InputText
                        id="c2q3"
                        v-model="c2q3"
                        aria-describedby="c2q3-help"
                        :invalid="!!errors.c2q3"
                        class="w-full"
                        inputClass="w-full"
                      />
                      <label for="c2q3">Begründung</label>
                    </FloatLabel>
                  </div>
                </div>
                <Divider />
                <div>
                  <p>
                    Handelt es sich um ein Konzept/eine Kampagne, die die Mobilität (Nah- oder
                    Fernverkehr, auch Reisen) klimaschädigend beeinflusst?
                  </p>
                  <SelectButton
                    v-model="c2q4"
                    :options="optionBoolean"
                    optionLabel="name"
                    optionValue="id"
                    :multiple="false"
                    :invalid="!!errors.c2q4"
                  />
                </div>
                <div v-if="c2q4 === 1">
                  <div>
                    <p>Inwiefern?</p>
                    <FloatLabel variant="on">
                      <InputText
                        id="c2q5"
                        v-model="c2q5"
                        aria-describedby="c2q5-help"
                        :invalid="!!errors.c2q5"
                        class="w-full"
                        inputClass="w-full"
                      />
                      <label for="c2q5">Begründung</label>
                    </FloatLabel>
                  </div>
                </div>
                <Divider />
                <div>
                  <p>
                    Handelt es sich um ein Konzept/eine Kampagne, die das Wissen über Klimaschutz
                    oder Klimaanpassung negativ beeinflusst?
                  </p>
                  <SelectButton
                    v-model="c2q6"
                    :options="optionBoolean"
                    optionLabel="name"
                    optionValue="id"
                    :multiple="false"
                    :invalid="!!errors.c2q6"
                  />
                </div>
                <div v-if="c2q6 === 1">
                  <div>
                    <p>Inwiefern?</p>
                    <FloatLabel variant="on">
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
                  </div>
                </div>
                <Divider />
                <div>
                  <p>
                    Handelt es sich um ein Konzept/eine Kampagne, die anderweitig klimarelevantes
                    Verhalten (z.B. Entscheidung über EE im Eigenheim) negativ beeinflusst?
                  </p>
                  <SelectButton
                    v-model="c2q8"
                    :options="optionBoolean"
                    optionLabel="name"
                    optionValue="id"
                    :multiple="false"
                    :invalid="!!errors.c2q8"
                  />
                </div>
                <div v-if="c2q8 === 1">
                  <div>
                    <p>Inwiefern?</p>
                    <FloatLabel variant="on">
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
import { schema } from '@/utils/schemas/klimarelevanzpruefungEingabeFb3'
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

const onSubmit = handleSubmit((values) => {
  console.log('Form Values:', values)
})
</script>

<style></style>
