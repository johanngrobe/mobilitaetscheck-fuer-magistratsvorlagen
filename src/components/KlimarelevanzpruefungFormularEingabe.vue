<template>
  <div>
    <form @submit.prevent="onSubmit" class="mt-4">
      <div class="mb-8">
        <FloatLabel variant="on">
          <InputText
            id="name"
            v-model="name"
            aria-describedby="name-help"
            :invalid="!!errors.name"
            class="w-full"
            inputClass="w-full"
          />
          <label for="name">Name der Klimarelevanzprüfung</label>
        </FloatLabel>
        <small v-if="errors.name" id="name-help" class="p-error block">{{ errors.name }}</small>
      </div>
      <ol class="grid grid-cols-[11fr_1fr] gap-2 items-center list-outside list-decimal ms-6">
        <li @click="f1 = !f1">
          Es handelt sich um eine <strong>physische Maßnahme oder eine Beschaffung </strong> oder um
          die <strong>konkrete Planung/Konzept derer</strong>.<br />
          <small
            >(z.B. Begrünung, Abriss, Umbau, Installation, Anschaffung von Maschinen, Abholzungen /
            Fällungen, Flächennutzungsänderungen, Baumaßnahmen etc.)</small
          >
        </li>
        <ToggleSwitch v-model="f1" :disbaled="disableF1to4" :invalied="!!errors.f1" />
        <Divider class="col-span-2" />
        <li @click="f2 = !f2">
          Es handelt sich um eine Planung / ein Konzept , das<strong>
            indirekt physische Maßnahmen nach sich zieht.</strong
          ><br /><small> (z.B. Bebauungsplan)</small>
        </li>
        <ToggleSwitch v-model="f2" :disbaled="disableF1to4" :invalied="!!errors.f2" />

        <Divider class="col-span-2" />
        <li @click="f3 = !f3">
          Es handelt sich um eine Planung, ein Konzept, oder ein Vorhaben, die
          <strong
            >das Verhalten der Bevölkerung oder der kommunalen Mitarbeitenden in Bezug auf
            Klimaaspekte beeinflusst.</strong
          ><br />
          <small> (z.B. Klima-Bildungskampagne, Mobilitätsverhalten)</small>
        </li>
        <ToggleSwitch v-model="f3" :disbaled="disableF1to4" :invalied="!!errors.f3" />

        <Divider class="col-span-2" />
        <li @click="f4 = !f4">
          Es handelt sich um ein Vorhaben, das
          <strong>nicht in eine der bisherigen Kategorien passt</strong>, aber dennoch klimawirksam
          ist.<br />
          <small>(z.B. Reisen)</small>
        </li>
        <ToggleSwitch v-model="f4" :disbaled="disableF1to4" :invalied="!!errors.f4" />

        <Divider class="col-span-2" />
        <li @click="f5 = !f5">
          Es handelt sich um eine Maßnahme, die <strong>in keiner Weise klimawirksam</strong> ist.
          <br />
          <small>
            (z.B. Personaleinstellung, Mitgliedschaft außerhalb von Klimaschutz- /Klimaanpassung,
            Beantwortung von Anfragen, Wahlen etc.)</small
          >
        </li>
        <ToggleSwitch v-model="f5" :disabled="disableF5" :invalied="!!errors.f5" />
        <small v-if="errors.f5" id="f5-help" class="p-error col-span-2">{{ errors.f5 }}</small>
      </ol>
      <div class="flex justify-end items-center mt-8">
        <Button icon="pi pi-angle-right" label="weiter" type="submit" />
      </div>
    </form>
  </div>
</template>

<script setup>
import { computed, watch } from 'vue'
import { useForm } from 'vee-validate'
import { schema } from '@/utils/schemas/klimarelevanzpruefungEingabe'
import { createItem } from '@/composables/crud'
import { useRoute, useRouter } from 'vue-router'
import Button from 'primevue/button'
import InputText from 'primevue/inputtext'
import FloatLabel from 'primevue/floatlabel'
import ToggleSwitch from 'primevue/toggleswitch'
import Divider from 'primevue/divider'

const route = useRoute()
const router = useRouter()

const { defineField, handleSubmit, setValues, errors } = useForm({
  validationSchema: schema
})

const [name] = defineField('name')
const [f1] = defineField('f1')
const [f2] = defineField('f2')
const [f3] = defineField('f3')
const [f4] = defineField('f4')
const [f5] = defineField('f5')

setValues({
  f1: false,
  f2: false,
  f3: false,
  f4: false,
  f5: false
})

const disableF1to4 = computed(() => f5.value === true)

watch(f5, (newVal) => {
  if (newVal === true) {
    setValues({
      f1: false,
      f2: false,
      f3: false,
      f4: false
    })
  }
})
const disableF5 = computed(
  () => f1.value === true || f2.value === true || f3.value === true || f4.value === true
)

watch([f1, f2, f3, f4], ([val1, val2, val3, val4]) => {
  if (val1 || val2 || val3 || val4) {
    setValues({
      f5: false
    })
  }
})

const onSubmit = handleSubmit(async (values) => {
  const response = await createItem({
    model: 'klimarelevanzpruefung/eingabe',
    values,
    detail: {
      success: 'Klimarelevanzprüfung erfolgreich hinzugefügt',
      error: 'Fehler beim Hinzufügen der Klimarelevanzprüfung'
    }
  })
  router.push({
    name: 'magistratsvorlage-id-klimarelevanzpruefung-id',
    params: { id: route.params.id, klimarelevanzpruefungId: response.id }
  })
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
