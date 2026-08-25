<template>
  <div>
    <BaseHeading>Über das Tool</BaseHeading>

    <BaseSpinner v-if="isLoading" />
    <div v-else-if="inhalt" v-html="inhalt" />

    <table v-else class="table-auto border-separate border-spacing-3">
      <tbody>
        <tr>
          <td><strong>Projekt:</strong></td>
          <td>Plattform für integrierte Mobilität in Oberursel (pimoo)</td>
        </tr>

        <tr>
          <td class="align-top"><strong>Organisation:</strong></td>
          <td>Hochschule RheinMain<br />Kurt-Schumacher-Ring 18<br />65197 Wiesbaden</td>
        </tr>

        <tr>
          <td><strong>Ansprechpartner:</strong></td>
          <td>Johann Grobe</td>
        </tr>

        <tr>
          <td><strong>Email:</strong></td>
          <td><a href="mailto:johanngrobe@hs-rm.de"></a>johann.grobe@hs-rm.de</td>
        </tr>

        <tr>
          <td><strong>Telefon:</strong></td>
          <td>+49 611 9495 - 1963</td>
        </tr>
      </tbody>
    </table>

    <div class="mt-8 border-t pt-6">
      <h2 class="text-lg font-bold">Entwickelt durch pimoo</h2>

      <p class="mt-2">
        Entwickelt wurde das Tool im Projekt pimoo (Plattform für integrierte Mobilität in
        Oberursel) von der Hochschule RheinMain gemeinsam mit der Stadt Oberursel (Taunus) sowie
        den Transferkommunen Taunusstein und Frankfurt am Main mit Förderung des
        Bundesministeriums für Forschung, Technologie und Raumfahrt (FKZ 01UV2428B).
      </p>

      <div class="flex flex-wrap items-center gap-6 mt-6">
        <a href="https://pimoo.de" target="_blank" rel="noopener noreferrer">
          <img :src="logoPimoo" alt="Logo pimoo" class="h-14" />
        </a>
      </div>

      <div class="flex flex-wrap items-center gap-6 mt-4">
        <a href="https://www.hs-rm.de" target="_blank" rel="noopener noreferrer">
          <img :src="logoHsrm" alt="Logo Hochschule RheinMain" class="h-14" />
        </a>
        <a href="https://www.oberursel.de" target="_blank" rel="noopener noreferrer">
          <img :src="logoOberursel" alt="Logo Stadt Oberursel (Taunus)" class="h-14" />
        </a>
      </div>

      <p class="mt-6"><strong>Gefördert durch:</strong></p>

      <div class="flex flex-wrap items-center gap-6 mt-2">
        <a href="https://www.bmftr.bund.de" target="_blank" rel="noopener noreferrer">
          <img
            :src="logoBmftr"
            alt="Logo Bundesministerium für Forschung, Technologie und Raumfahrt"
            class="h-14"
          />
        </a>
        <a href="https://www.fona.de" target="_blank" rel="noopener noreferrer">
          <img :src="logoFona" alt="Logo FONA" class="h-14" />
        </a>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { apiClient } from '@/services/axios'
import logoHsrm from '@/assets/logos/HSRM_Unterzeile_farbig_RGB.png'
import logoOberursel from '@/assets/logos/oberursel-logo.webp'
import logoPimoo from '@/assets/logos/Pimoo-Logo-Primaer.png'
import logoBmftr from '@/assets/logos/BMFTR.jpg'
import logoFona from '@/assets/logos/FONA.jpg'

const isLoading = ref(false)
const inhalt = ref('')

onMounted(async () => {
  isLoading.value = true
  try {
    const res = await apiClient.get('/public/plattform-einstellung')
    inhalt.value = res.data.ueberDasToolInhalt || ''
  } catch {
    inhalt.value = ''
  } finally {
    isLoading.value = false
  }
})
</script>

<style scoped></style>
