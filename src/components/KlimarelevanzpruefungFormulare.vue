<template>
  <div>
    <ol class="grid grid-cols-[9fr_3fr] gap-2 items-center list-outside list-decimal ms-6">
      <Dialog
        v-model:visible="visibleF1"
        position="top"
        modal
        header="Fragebogen A"
        :style="{ width: '50rem' }"
      >
        <KlimarelevanzpruefungFormularEingabeFb1 />
      </Dialog>
      <li>
        Es handelt sich um eine <strong>physische Maßnahme oder eine Beschaffung </strong> oder um
        die <strong>konkrete Planung/Konzept derer</strong>.<br />
        <small
          >(z.B. Begrünung, Abriss, Umbau, Installation, Anschaffung von Maschinen, Abholzungen /
          Fällungen, Flächennutzungsänderungen, Baumaßnahmen etc.)</small
        >
      </li>
      <Button
        label="zum Fragebogen"
        @click="visibleF1 = true"
        :disabled="!klimarelevanzpruefung.f1"
      />
      <Divider class="col-span-2" />
      <Dialog
        v-model:visible="visibleF2"
        position="top"
        modal
        header="Fragebogen B"
        :style="{ width: '50rem' }"
      >
        <KlimarelevanzpruefungFormularEingabeFb2 />
      </Dialog>
      <li>
        Es handelt sich um eine Planung / ein Konzept , das<strong>
          indirekt physische Maßnahmen nach sich zieht.</strong
        ><br /><small> (z.B. Bebauungsplan)</small>
      </li>
      <Button
        label="zum Fragebogen"
        @click="visibleF2 = true"
        :disabled="!klimarelevanzpruefung.f2"
      />

      <Divider class="col-span-2" />
      <Dialog
        v-model:visible="visibleF3"
        position="top"
        modal
        header="Fragebogen C"
        :style="{ width: '50rem' }"
      >
        <KlimarelevanzpruefungFormularEingabeFb3 />
      </Dialog>
      <li>
        Es handelt sich um eine Planung, ein Konzept, oder ein Vorhaben, die
        <strong
          >das Verhalten der Bevölkerung oder der kommunalen Mitarbeitenden in Bezug auf
          Klimaaspekte beeinflusst.</strong
        ><br />
        <small> (z.B. Klima-Bildungskampagne, Mobilitätsverhalten)</small>
      </li>
      <Button
        label="zum Fragebogen"
        @click="visibleF3 = true"
        :disabled="!klimarelevanzpruefung.f3"
      />

      <Divider class="col-span-2" />
      <Dialog
        v-model:visible="visibleF4"
        position="top"
        modal
        header="Fragebogen D"
        :style="{ width: '50rem' }"
      >
        <KlimarelevanzpruefungFormularEingabeFb4 />
      </Dialog>
      <li>
        Es handelt sich um ein Vorhaben, das
        <strong>nicht in eine der bisherigen Kategorien passt</strong>, aber dennoch klimawirksam
        ist.<br />
        <small>(z.B. Reisen)</small>
      </li>
      <Button
        label="zum Fragebogen"
        @click="visibleF4 = true"
        :disabled="!klimarelevanzpruefung.f4"
      />

      <Divider class="col-span-2" />
      <li>
        Es handelt sich um eine Maßnahme, die <strong>in keiner Weise klimawirksam</strong> ist.
        <br />
        <small>
          (z.B. Personaleinstellung, Mitgliedschaft außerhalb von Klimaschutz- /Klimaanpassung,
          Beantwortung von Anfragen, Wahlen etc.)</small
        >
      </li>
      <Button label="Kein Fragebogen" :disabled="true" />
    </ol>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { fetchItem } from '@/composables/crud'
import Button from 'primevue/button'
import Dialog from 'primevue/dialog'
import Divider from 'primevue/divider'
import KlimarelevanzpruefungFormularEingabeFb1 from './KlimarelevanzpruefungFormularEingabeFb1.vue'
import KlimarelevanzpruefungFormularEingabeFb2 from './KlimarelevanzpruefungFormularEingabeFb2.vue'
import KlimarelevanzpruefungFormularEingabeFb3 from './KlimarelevanzpruefungFormularEingabeFb3.vue'
import KlimarelevanzpruefungFormularEingabeFb4 from './KlimarelevanzpruefungFormularEingabeFb4.vue'

const route = useRoute()

const isLoading = ref(false)
const klimarelevanzpruefung = ref({ f1: false, f2: false, f3: false, f4: false, f5: false })
const visibleF1 = ref(false)
const visibleF2 = ref(false)
const visibleF3 = ref(false)
const visibleF4 = ref(false)

onMounted(async () => {
  isLoading.value = true
  await fetchData()
  isLoading.value = false
})

const fetchData = async () => {
  klimarelevanzpruefung.value = await fetchItem(
    `/klimarelevanzpruefung/eingabe/${route.params.klimarelevanzpruefungId}`
  )
}
</script>

<style></style>
