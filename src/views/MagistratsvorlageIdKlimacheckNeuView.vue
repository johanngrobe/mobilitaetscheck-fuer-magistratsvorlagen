<template>
  <div>
    <div class="grid grid-cols-2 w-full items-center">
      <BaseHeading>Neuer Klimacheck</BaseHeading>
      <div class="flex w-full justify-end">
        <ButtonZuruecksetzen @click="refreshPage()">zurücksetzen</ButtonZuruecksetzen>
      </div>
    </div>
    <BaseCard
      :collapsible="true"
      :isCollapsed="formInfoCollapsed"
      :initiallyCollapsed="true"
      class="hover:bg-gray-200"
    >
      <template #header>
        <div v-tooltip.top="'Klicken zum Öffnen'" @click="toggleFormInfo">
          <BaseSubheading>Informationen zum Formular</BaseSubheading>
        </div>
      </template>
      Das Kyoto-Protokoll nennt sechs Treibhausgase: Kohlendioxid (CO2), Methan (CH4), und Lachgas
      (N2O) sowie die fluorierten Treibhausgase (F-Gase): wasserstoffhaltige Fluorkohlenwasserstoffe
      (HFKW), perfluorierte Kohlenwasserstoffe (FKW), und Schwefelhexafluorid (SF6). Ab 2015 wird
      Stickstofftrifluorid (NF3) zusätzlich einbezogen. Die verschiedenen Gase tragen nicht in
      gleichem Masse zum Treibhauseffekt bei und verbleiben über unterschiedlich lange Zeiträume in
      der Atmosphäre. Um die Wirkung verschiedener Treibhausgase vergleichbar zu machen, können
      Treibhausgase in CO2-Äquivalente umgerechnet und zusammengefasst werden. CO2-Äquivalente
      werden mit der Abkürzung «CO2e» bezeichnet.
    </BaseCard>
    <BaseCard>
      <KlimacheckFormular />
    </BaseCard>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import KlimacheckFormular from '@/components/KlimacheckFormular.vue'
import ButtonZuruecksetzen from '@/components/ButtonZuruecksetzen.vue'
import { useRouter } from 'vue-router'

const router = useRouter()

const refreshPage = () => {
  router.go() // Reloads the current route
}

const formInfoCollapsed = ref(true)

const toggleFormInfo = () => {
  formInfoCollapsed.value = !formInfoCollapsed.value
}
</script>
