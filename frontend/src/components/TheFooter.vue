<template>
  <div>
    <footer class="footer w-full bg-blue text-white py-4 text-center mt-12">
      <div class="footer-content mt-4 max-w-screen-lg mx-auto">
        <div class="grid grid-cols-2 items-center justify-center gap-4">
          <div class="flex flex-wrap items-center justify-center gap-2">
            <template v-if="footerLogos.length > 0">
              <div
                v-for="logo in footerLogos"
                :key="logo.id"
                class="bg-white flex w-fit p-2 rounded justify-center items-center"
              >
                <BrandingLogoLink :href="logo.link">
                  <img :src="logo.asset.url" alt="Logo" class="h-14" />
                </BrandingLogoLink>
              </div>
            </template>
            <template v-else>
              <div class="bg-white flex w-fit p-2 rounded justify-center items-center">
                <div class="flex items-center justify-center gap-x-6 h-10 mx-auto">
                  <img :src="defaultLogo1" alt="Logo" class="h-10" />
                  <img :src="defaultLogo2" alt="Logo" class="h-11" />
                </div>
              </div>
              <div class="bg-white flex w-fit p-2 rounded justify-center items-center">
                <img :src="defaultLogo3" class="h-20 sm:h-20" alt="Logo" />
              </div>
              <div class="bg-white flex w-fit p-2 rounded justify-center items-center">
                <img :src="defaultLogo4" class="h-20 sm:h-14" alt="Logo" />
              </div>
            </template>
          </div>
          <div>
            <div class="mt-2">
              <router-link :to="{ name: 'ueber-das-tool' }" class="hover:underline"
                >Über das Tool</router-link
              >
            </div>
            <div class="mt-2">
              <a
                class="hover:underline"
                href="https://ritmo-hsrm.github.io/mobilitaetscheck-fuer-magistratsvorlagen/"
                target="_blank"
                >Dokumentation und Hilfe</a
              >
            </div>
            <div class="mt-2">
              <a
                class="hover:underline"
                href="https://github.com/ritmo-hsrm/mobilitaetscheck-fuer-magistratsvorlagen"
                target="_blank"
                >Github-Repo</a
              >
            </div>
            <div class="mt-2">
              <a
                v-if="einstellung.impressumModus === 'url' && einstellung.impressumUrl"
                class="hover:underline"
                :href="einstellung.impressumUrl"
                target="_blank"
                rel="noopener noreferrer"
                >Impressum</a
              >
              <router-link v-else class="hover:underline" :to="{ name: 'impressum' }"
                >Impressum</router-link
              >
            </div>
            <div class="mt-2">
              <a
                v-if="einstellung.datenschutzModus === 'url' && einstellung.datenschutzUrl"
                class="hover:underline"
                :href="einstellung.datenschutzUrl"
                target="_blank"
                rel="noopener noreferrer"
                >Datenschutzerklärung</a
              >
              <router-link v-else class="hover:underline" :to="{ name: 'datenschutzerklaerung' }"
                >Datenschutzerklärung</router-link
              >
            </div>
          </div>
        </div>
        <div></div>
        <p class="mt-4">&copy; 2026 Hochschule RheinMain</p>
      </div>
    </footer>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { apiClient } from '@/services/axios'
import BrandingLogoLink from './BrandingLogoLink.vue'
import defaultLogo1 from '../assets/logos/HSRM_Unterzeile_farbig_RGB.png'
import defaultLogo2 from '../assets/logos/oberursel-logo.webp'
import defaultLogo3 from '../assets/logos/BMFTR.jpg'
import defaultLogo4 from '../assets/logos/FONA.jpg'

const einstellung = ref({})
const footerLogos = ref([])

onMounted(async () => {
  try {
    const [einstellungRes, footerLogosRes] = await Promise.all([
      apiClient.get('/public/plattform-einstellung'),
      apiClient.get('/branding/logo-listen/footer')
    ])
    einstellung.value = einstellungRes.data
    footerLogos.value = footerLogosRes.data
  } catch {
    einstellung.value = {}
    footerLogos.value = []
  }
})
</script>

<style scoped>
/* Tailwind CSS is used, no additional styles needed */
</style>
