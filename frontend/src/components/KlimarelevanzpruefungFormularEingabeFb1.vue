<template>
  <div>
    <form @submit.prevent="onSubmit" class="mt-4">
      <Message v-if="hasErrors" severity="error" class="mb-4">
        <ul class="list-disc list-inside">
          <li v-for="(error, field) in errors" :key="field">
            {{ dynamicErrorLabels[field] ?? error }}
          </li>
        </ul>
      </Message>
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
            <ol class="list-decimal list-inside space-y-4">
              <li>
                <span>Werden im Rahmen des Vorhabens Maschinen oder Materialen angeschafft?</span>
                <SelectButton
                  v-model="a1q1"
                  :options="optionBoolean"
                  optionLabel="name"
                  optionValue="id"
                  :multiple="false"
                  :invalid="!!errors.a1q1"
                  class="mt-2"
                />
              </li>
              <template v-if="a1q1 === 1">
                <li>
                  <span>Was wurde hauptsächlich angeschafft?</span>
                  <FloatLabel variant="on" class="mt-2 w-full">
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
                </li>
                <li>
                  <span>
                    Wurde bei der Auswahl auf Nachhaltigkeitskriterien geachtet und sich ganz oder
                    teilweise für eine klimaschonende Ausführung entschieden?
                  </span>
                  <SelectButton
                    v-model="a1q3"
                    :options="optionBoolean"
                    optionLabel="name"
                    optionValue="id"
                    :multiple="false"
                    :invalid="!!errors.a1q3"
                    class="mt-2"
                  />
                </li>
                <li v-if="a1q3 === 1">
                  <span>Inwiefern?</span>
                  <FloatLabel variant="on" class="mt-2 w-full">
                    <InputText
                      id="a1q4"
                      v-model="a1q4"
                      aria-describedby="a1q4-help"
                      :invalid="!!errors.a1q4"
                      class="w-full"
                      inputClass="w-full"
                    />
                    <label for="a1q4">Erläuterung</label>
                  </FloatLabel>
                </li>
                <li v-if="a1q3 === 2">
                  <span>
                    Warum wurde sich nicht für die nachhaltige Variante entschieden? Bitte begründen
                    Sie kurz.
                  </span>
                  <FloatLabel variant="on" class="mt-2 w-full">
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
                </li>
              </template>
            </ol>
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
            <ol class="list-decimal list-inside space-y-4">
              <li>
                <span>Werden bauliche Maßnahmen durchgeführt?</span>
                <SelectButton
                  v-model="a2q1"
                  :options="optionBoolean"
                  optionLabel="name"
                  optionValue="id"
                  :multiple="false"
                  :invalid="!!errors.a2q1"
                  class="mt-2"
                />
              </li>
              <template v-if="a2q1 === 1">
                <li>
                  <span>Worum handelt es sich bei dem Vorhaben?</span>
                  <SelectButton
                    v-model="a2q2"
                    :options="optionVorhaben"
                    optionLabel="name"
                    optionValue="id"
                    :multiple="false"
                    :invalid="!!errors.a2q2"
                    class="mt-2"
                  />
                </li>
                <template v-if="[3, 4].includes(a2q2)">
                  <li>
                    <span
                      >Wird durch das Bauvorhaben ein bestehendes Gebäude energetisch
                      aufgewertet?</span
                    >
                    <SelectButton
                      v-model="a2q3"
                      :options="optionBoolean"
                      optionLabel="name"
                      optionValue="id"
                      :multiple="false"
                      :invalid="!!errors.a2q3"
                      class="mt-2"
                    />
                  </li>
                  <template v-if="a2q3 === 1">
                    <li>
                      <span>Welcher Energiestandard wird erreicht?</span>
                      <Select
                        v-model="a2q4"
                        :options="optionVorhaben.find((x) => x.id === 3)?.energiestandards || []"
                        optionLabel="name"
                        optionValue="id"
                        class="w-full mt-2"
                        :invalid="!!errors.a2q4"
                        aria-describedby="a2q4-help"
                      />
                    </li>
                    <li v-if="typeof a2q4 === 'number'">
                      <span>Warum wurde sich für den genannten Energiestandard entschieden?</span>
                      <FloatLabel variant="on" class="mt-2 w-full">
                        <InputText
                          id="a2q5"
                          v-model="a2q5"
                          aria-describedby="a2q4-help"
                          :invalid="!!errors.a2q5"
                          class="w-full"
                          inputClass="w-full"
                        />
                        <label for="a2q5">Erläuterung</label>
                      </FloatLabel>
                    </li>
                  </template>
                </template>
                <template v-if="[1, 2].includes(a2q2)">
                  <li>
                    <span>Welcher Energiestandard wird erreicht?</span>
                    <Select
                      v-model="a2q6"
                      :options="optionVorhaben.find((x) => x.id === 1)?.energiestandards || []"
                      optionLabel="name"
                      optionValue="id"
                      class="w-full mt-2"
                      :invalid="!!errors.a2q6"
                      aria-describedby="a2q6-help"
                    />
                  </li>
                  <li v-if="typeof a2q6 === 'number'">
                    <span>Warum wurde sich für den genannten Energiestandard entschieden?</span>
                    <FloatLabel variant="on" class="mt-2 w-full">
                      <InputText
                        id="a2q7"
                        v-model="a2q7"
                        aria-describedby="a2q7-help"
                        :invalid="!!errors.a2q7"
                        class="w-full"
                        inputClass="w-full"
                      />
                      <label for="a2q7">Erläuterung</label>
                    </FloatLabel>
                  </li>
                </template>
                <li>
                  <span>
                    Wird bei dem Bauvorhaben darauf geachtet, dass Niederschlag möglichst vor Ort
                    versickert?
                  </span>
                  <SelectButton
                    v-model="a2q8"
                    :options="optionBoolean"
                    optionLabel="name"
                    optionValue="id"
                    :multiple="false"
                    :invalid="!!errors.a2q8"
                    class="mt-2"
                  />
                </li>
                <li v-if="a2q8 === 2">
                  <span>Warum nicht?</span>
                  <FloatLabel variant="on" class="mt-2 w-full">
                    <InputText
                      id="a2q9"
                      v-model="a2q9"
                      aria-describedby="a2q9-help"
                      :invalid="!!errors.a2q9"
                      class="w-full"
                      inputClass="w-full"
                    />
                    <label for="a2q9">Erläuterung</label>
                  </FloatLabel>
                </li>
                <li>
                  <span>
                    Wird bei dem Bauvorhaben darauf geachtet, dass Kaltluftströme ungehindert
                    fließen können?
                  </span>
                  <SelectButton
                    v-model="a2q10"
                    :options="optionBoolean"
                    optionLabel="name"
                    optionValue="id"
                    :multiple="false"
                    :invalid="!!errors.a2q10"
                    class="mt-2"
                  />
                </li>
                <li v-if="a2q10 === 2">
                  <span>Warum nicht?</span>
                  <FloatLabel variant="on" class="mt-2 w-full">
                    <InputText
                      id="a2q11"
                      v-model="a2q11"
                      aria-describedby="a2q11-help"
                      :invalid="!!errors.a2q11"
                      class="w-full"
                      inputClass="w-full"
                    />
                    <label for="a2q11">Erläuterung</label>
                  </FloatLabel>
                </li>
                <li>
                  <span>
                    Wird bei dem Vorhaben durch geeignete Maßnahmen der örtlichen Hitzebildung
                    vorgebeugt? (z. B. Verschattungselemente oder Begrünung)
                  </span>
                  <SelectButton
                    v-model="a2q12"
                    :options="optionBoolean"
                    optionLabel="name"
                    optionValue="id"
                    :multiple="false"
                    :invalid="!!errors.a2q12"
                    class="mt-2"
                  />
                </li>
                <li v-if="a2q12 === 2">
                  <span>Warum nicht?</span>
                  <FloatLabel variant="on" class="mt-2 w-full">
                    <InputText
                      id="a2q13"
                      v-model="a2q13"
                      aria-describedby="a2q13-help"
                      :invalid="!!errors.a2q13"
                      class="w-full"
                      inputClass="w-full"
                    />
                    <label for="a2q13">Erläuterung</label>
                  </FloatLabel>
                </li>
                <li>
                  <span>Wurde bei den Vergabekriterien auf Nachhaltigkeit geachtet?</span>
                  <SelectButton
                    v-model="a2q14"
                    :options="optionBoolean"
                    optionLabel="name"
                    optionValue="id"
                    :multiple="false"
                    :invalid="!!errors.a2q14"
                    class="mt-2"
                  />
                </li>
                <li v-if="a2q14 === 2">
                  <span>Warum nicht?</span>
                  <FloatLabel variant="on" class="mt-2 w-full">
                    <InputText
                      id="a2q15"
                      v-model="a2q15"
                      aria-describedby="a2q15-help"
                      :invalid="!!errors.a2q15"
                      class="w-full"
                      inputClass="w-full"
                    />
                    <label for="a2q15">Erläuterung</label>
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
              <Button
                label="Weiter"
                icon="pi pi-arrow-right"
                iconPos="right"
                @click="activateCallback('3')"
              />
            </div>
          </StepPanel>
          <StepPanel v-slot="{ activateCallback }" value="3">
            <ol class="list-decimal list-inside space-y-4">
              <li>
                <span>Werden bei dem Vorhaben Flächen neu versiegelt?</span>
                <SelectButton
                  v-model="a3q1"
                  :options="optionBoolean"
                  optionLabel="name"
                  optionValue="id"
                  :multiple="false"
                  :invalid="!!errors.a3q1"
                  class="mt-2"
                />
              </li>
              <template v-if="a3q1 === 1">
                <li>
                  <span>In welchem Umfang werden Flächen neu versiegelt? (Angabe in m²)</span>
                  <FloatLabel variant="on" class="mt-2 w-full">
                    <InputNumber
                      id="a3q2"
                      v-model="a3q2"
                      :min="0"
                      :step="1"
                      mode="decimal"
                      suffix=" m²"
                      :useGrouping="false"
                      aria-describedby="a3q2-help"
                      :invalid="!!errors.a3q2"
                      class="w-full"
                      inputClass="w-full"
                    />
                    <label for="a3q2">Angabe in m²</label>
                  </FloatLabel>
                </li>
                <li>
                  <span>Wie wurde die Fläche bisher genutzt?</span>
                  <FloatLabel variant="on" class="mt-2 w-full">
                    <InputText
                      id="a3q3"
                      v-model="a3q3"
                      aria-describedby="a3q3-help"
                      :invalid="!!errors.a3q3"
                      class="w-full"
                      inputClass="w-full"
                    />
                    <label for="a3q3">Angabe der bisherigen Nutzung</label>
                  </FloatLabel>
                </li>
                <li>
                  <span>Sind für die Versiegelung Ausgleichsmaßnahmen vorgesehen?</span>
                  <SelectButton
                    v-model="a3q4"
                    :options="optionBoolean"
                    optionLabel="name"
                    optionValue="id"
                    :multiple="false"
                    :invalid="!!errors.a3q4"
                    class="mt-2"
                  />
                </li>
                <li v-if="a3q4 === 1">
                  <span>In welcher Form und Umfang sind die Ausgleichsmaßnahmen vorgesehen?</span>
                  <FloatLabel variant="on" class="mt-2 w-full">
                    <InputText
                      id="a3q5"
                      v-model="a3q5"
                      aria-describedby="a3q5-help"
                      :invalid="!!errors.a3q5"
                      class="w-full"
                      inputClass="w-full"
                    />
                    <label for="a3q5">Angaben zu Ausgleichsmaßnahmen</label>
                  </FloatLabel>
                </li>
                <li v-if="a3q4 === 2">
                  <span>Warum nicht?</span>
                  <FloatLabel variant="on" class="mt-2 w-full">
                    <InputText
                      id="a3q6"
                      v-model="a3q6"
                      aria-describedby="a3q6-help"
                      :invalid="!!errors.a3q6"
                      class="w-full"
                      inputClass="w-full"
                    />
                    <label for="a3q6">Erläuterung</label>
                  </FloatLabel>
                </li>
              </template>
            </ol>
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
            <ol class="list-decimal list-inside space-y-4">
              <li>
                <span>Werden bei dem Vorhaben Flächen entsiegelt?</span>
                <SelectButton
                  v-model="a4q1"
                  :options="optionBoolean"
                  optionLabel="name"
                  optionValue="id"
                  :multiple="false"
                  :invalid="!!errors.a4q1"
                  class="mt-2"
                />
              </li>
              <template v-if="a4q1 === 1">
                <li>
                  <span>In welchem Umfang werden Flächen entsiegelt? (Angabe in m²)</span>
                  <FloatLabel variant="on" class="mt-2 w-full">
                    <InputNumber
                      id="a4q2"
                      v-model="a4q2"
                      :min="0"
                      :step="1"
                      mode="decimal"
                      suffix=" m²"
                      :useGrouping="false"
                      aria-describedby="a4q2-help"
                      :invalid="!!errors.a4q2"
                      class="w-full"
                      inputClass="w-full"
                    />
                    <label for="a4q2">Angabe in m²</label>
                  </FloatLabel>
                </li>
                <li>
                  <span>Wie wurde die Fläche bisher genutzt?</span>
                  <FloatLabel variant="on" class="mt-2 w-full">
                    <InputText
                      id="a4q3"
                      v-model="a4q3"
                      aria-describedby="a4q3-help"
                      :invalid="!!errors.a4q3"
                      class="w-full"
                      inputClass="w-full"
                    />
                    <label for="a4q3">Angabe der bisherigen Nutzung</label>
                  </FloatLabel>
                </li>
                <li v-if="a4q3">
                  <span>
                    Wird die Entsiegelung als Ausgleichsmaßnahme für ein anderes Vorhaben
                    durchgeführt?
                  </span>
                  <SelectButton
                    v-model="a4q4"
                    :options="optionBoolean"
                    optionLabel="name"
                    optionValue="id"
                    :multiple="false"
                    :invalid="!!errors.a4q4"
                    class="mt-2"
                  />
                </li>
              </template>
            </ol>
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
            <ol class="list-decimal list-inside space-y-4">
              <li>
                <span>
                  Werden bei dem Vorhaben Grünflächen mit CO2-bindender Funktion aufgewertet? (Z.B.
                  durch die Pflanung von Bäumen und Sträuchern)
                </span>
                <SelectButton
                  v-model="a5q1"
                  :options="optionBoolean"
                  optionLabel="name"
                  optionValue="id"
                  :multiple="false"
                  :invalid="!!errors.a5q1"
                  class="mt-2"
                />
              </li>
              <template v-if="a5q1 === 1">
                <li>
                  <span>In welchem Umfang werden die Grünflächen aufgewertet? (Angabe in m²)</span>
                  <FloatLabel variant="on" class="mt-2 w-full">
                    <InputNumber
                      id="a5q2"
                      v-model="a5q2"
                      aria-describedby="a5q2-help"
                      suffix=" m²"
                      :invalid="!!errors.a5q2"
                      class="w-full"
                      inputClass="w-full"
                    />
                    <label for="a5q2">Angabe in m²</label>
                  </FloatLabel>
                </li>
                <li>
                  <span>Wie wurde die Fläche bisher genutzt?</span>
                  <FloatLabel variant="on" class="mt-2 w-full">
                    <InputText
                      id="a5q3"
                      v-model="a5q3"
                      aria-describedby="a5q3-help"
                      :invalid="!!errors.a5q3"
                      class="w-full"
                      inputClass="w-full"
                    />
                    <label for="a5q3">Erläuterung</label>
                  </FloatLabel>
                </li>
                <li>
                  <span>In welcher Form werden die Grünflächen aufgewertet?</span>
                  <FloatLabel variant="on" class="mt-2 w-full">
                    <InputText
                      id="a5q5"
                      v-model="a5q5"
                      aria-describedby="a5q5-help"
                      :invalid="!!errors.a5q5"
                      class="w-full"
                      inputClass="w-full"
                    />
                    <label for="a5q5">Erläuterung</label>
                  </FloatLabel>
                </li>
                <li>
                  <span>
                    Wird die Maßnahme als Ausgleichsmaßnahme für ein anderes Vorhaben durchgeführt?
                  </span>
                  <SelectButton
                    v-model="a5q4"
                    :options="optionBoolean"
                    optionLabel="name"
                    optionValue="id"
                    :multiple="false"
                    :invalid="!!errors.a5q4"
                    class="mt-2"
                  />
                </li>
              </template>
            </ol>
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
            <ol class="list-decimal list-inside space-y-4">
              <li>
                <span>Wird im Rahmen des Vorhabens eine bestehende Begrünung entfernt?</span>
                <SelectButton
                  v-model="a6q1"
                  :options="optionBoolean"
                  optionLabel="name"
                  optionValue="id"
                  :multiple="false"
                  :invalid="!!errors.a6q1"
                  class="mt-2"
                />
              </li>
              <template v-if="a6q1 === 1">
                <li>
                  <span>In welchem Umfang?</span>
                  <FloatLabel variant="on" class="mt-2 w-full">
                    <InputText
                      id="a6q2"
                      v-model="a6q2"
                      aria-describedby="a6q2-help"
                      :invalid="!!errors.a6q2"
                      class="w-full"
                      inputClass="w-full"
                    />
                    <label for="a6q2">Umfang</label>
                  </FloatLabel>
                </li>
                <li>
                  <span>Sind Ausgleichsmaßnahmen vorgesehen?</span>
                  <SelectButton
                    v-model="a6q3"
                    :options="optionBoolean"
                    optionLabel="name"
                    optionValue="id"
                    :multiple="false"
                    :invalid="!!errors.a6q3"
                    class="mt-2"
                  />
                </li>
                <li v-if="a6q3 === 1">
                  <span>In welcher Form und Umfang sind die Ausgleichsmaßnahmen vorgesehen?</span>
                  <FloatLabel variant="on" class="mt-2 w-full">
                    <InputText
                      id="a6q4"
                      v-model="a6q4"
                      aria-describedby="a6q4-help"
                      :invalid="!!errors.a6q4"
                      class="w-full"
                      inputClass="w-full"
                    />
                    <label for="a6q4">Erläuterung</label>
                  </FloatLabel>
                </li>
                <li v-if="a6q3 === 2">
                  <span>Warum nicht?</span>
                  <FloatLabel variant="on" class="mt-2 w-full">
                    <InputText
                      id="a6q5"
                      v-model="a6q5"
                      aria-describedby="a6q5-help"
                      :invalid="!!errors.a6q5"
                      class="w-full"
                      inputClass="w-full"
                    />
                    <label for="a6q5">Erläuterung</label>
                  </FloatLabel>
                </li>
              </template>
            </ol>
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
            <ol class="list-decimal list-inside space-y-4">
              <li>
                <span>
                  Hat das Vorhaben in anderer Weise klimaschädliche Wirkung? (z.B. Kraftwerkbau,
                  Abwärme, Wasserbedarf…)
                </span>
                <SelectButton
                  v-model="a7q1"
                  :options="optionBoolean"
                  optionLabel="name"
                  optionValue="id"
                  :multiple="false"
                  :invalid="!!errors.a7q1"
                  class="mt-2"
                />
              </li>
              <li v-if="a7q1 === 1">
                <span>Inwiefern?</span>
                <FloatLabel variant="on" class="mt-2 w-full">
                  <InputText
                    id="a7q2"
                    v-model="a7q2"
                    aria-describedby="a7q2-help"
                    :invalid="!!errors.a7q2"
                    class="w-full"
                    inputClass="w-full"
                  />
                  <label for="a7q2">Erläuterung</label>
                </FloatLabel>
              </li>
            </ol>
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
            <ol class="list-decimal list-inside space-y-4">
              <li>
                <span>
                  Hat das Vorhaben in anderer Weise klimaschützende / Klimaresilienz fördernde
                  Wirkung? (z.B. Wasserretention, Energiesparmaßnahme, Verkehrsregulierung)
                </span>
                <SelectButton
                  v-model="a8q1"
                  :options="optionBoolean"
                  optionLabel="name"
                  optionValue="id"
                  :multiple="false"
                  :invalid="!!errors.a8q1"
                  class="mt-2"
                />
              </li>
              <li v-if="a8q1 === 1">
                <span>Inwiefern?</span>
                <FloatLabel variant="on" class="mt-2 w-full">
                  <InputText
                    id="a8q2"
                    v-model="a8q2"
                    aria-describedby="a8q2-help"
                    :invalid="!!errors.a8q2"
                    class="w-full"
                    inputClass="w-full"
                  />
                  <label for="a8q2">Erläuterung</label>
                </FloatLabel>
              </li>
            </ol>
            <div class="flex pt-6 justify-between">
              <Button
                label="Zurück"
                severity="secondary"
                icon="pi pi-arrow-left"
                @click="activateCallback('7')"
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
import { schema } from '@/utils/schemas/klimarelevanzpruefungEingabeFb1'
import { createItemSilent, fetchItems, updateItemSilent } from '@/composables/crud'
// import ToggleSwitch from 'primevue/toggleswitch'
import Button from 'primevue/button'
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
import Message from 'primevue/message'

const isLoading = ref(false)
const optionBoolean = ref()
const optionVorhaben = ref()

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
  isLoading.value = 1
  await fetchData()
  if (props.editMode && props.item) {
    setValues(props.item)
  }
  isLoading.value = false
})

const fetchData = async () => {
  optionBoolean.value = await fetchItems('/einstellungen/bool-erweitert')
  optionVorhaben.value = await fetchItems('/klimarelevanzpruefung/vorhaben')
}

const { defineField, handleSubmit, errors, setValues, values } = useForm({
  validationSchema: schema
})

const hasErrors = computed(() => Object.keys(errors.value).length > 0)

// Compute the actual visible counter position for each Seite 2 field,
// mirroring the CSS counter that increments on every rendered <li>.
const s2Counter = computed(() => {
  const pos = {}
  let n = 1
  pos.a2q1 = n++
  if (a2q1.value === 1) {
    pos.a2q2 = n++
    if ([3, 4].includes(a2q2.value)) {
      pos.a2q3 = n++
      if (a2q3.value === 1) {
        pos.a2q4 = n++
        if (typeof a2q4.value === 'number') pos.a2q5 = n++
      }
    }
    if ([1, 2].includes(a2q2.value)) {
      pos.a2q6 = n++
      if (typeof a2q6.value === 'number') pos.a2q7 = n++
    }
    pos.a2q8 = n++
    if (a2q8.value === 2) pos.a2q9 = n++
    pos.a2q10 = n++
    if (a2q10.value === 2) pos.a2q11 = n++
    pos.a2q12 = n++
    if (a2q12.value === 2) pos.a2q13 = n++
    pos.a2q14 = n++
    if (a2q14.value === 2) pos.a2q15 = n++
  }
  return pos
})

// Override error labels for Seite 2 fields with their dynamic position numbers.
const dynamicErrorLabels = computed(() => {
  const labels = {}
  for (const [field, n] of Object.entries(s2Counter.value)) {
    labels[field] = `Seite 2, Frage ${n}`
  }
  return labels
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
const [a5q5] = defineField('a5q5')
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
  return 1
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
  return 1
})

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
      model: 'klimarelevanzpruefung/eingabe/fb1',
      modelId: currentItemId.value,
      values: draftValues
    })
    return response ?? null
  } else {
    const response = await createItemSilent({
      model: 'klimarelevanzpruefung/eingabe/fb1',
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
    emit('update-item', { fb: 1, modelId: currentItemId.value, values: fullValues })
  } else {
    emit('add-item', { fb: 1, values: fullValues })
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
}

ol > li > span:first-child::before {
  content: counter(question) '. ';
  font-weight: bold;
}
</style>
