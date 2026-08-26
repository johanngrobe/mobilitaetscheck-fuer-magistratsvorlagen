<template>
  <div>
    <footer class="footer w-full bg-blue text-white py-8 text-center mt-12">
      <div class="footer-content max-w-screen-lg mx-auto px-4">
        <div class="grid grid-cols-1 sm:grid-cols-[auto_auto] items-start justify-center text-left gap-8">
          <div class="flex flex-wrap items-center justify-center gap-2 sm:col-span-2 sm:col-start-1 sm:row-start-1 sm:mx-auto">
            <template v-if="brandingStore.footerLogos.length > 0">
              <div
                v-for="logo in brandingStore.footerLogos"
                :key="logo.id"
                class="bg-white flex w-fit p-2 rounded justify-center items-center transition-transform duration-200 hover:-translate-y-0.5 hover:shadow-lg"
              >
                <BrandingLogoLink :href="logo.link">
                  <img :src="logo.asset.url" alt="Logo" class="h-14" />
                </BrandingLogoLink>
              </div>
            </template>
            <template v-else>
              <div class="bg-white flex w-fit p-2 rounded justify-center items-center transition-transform duration-200 hover:-translate-y-0.5 hover:shadow-lg">
                <div class="flex items-center justify-center gap-x-6 h-10 mx-auto">
                  <img :src="defaultLogo1" alt="Logo" class="h-10" />
                  <img :src="defaultLogo2" alt="Logo" class="h-11" />
                </div>
              </div>
              <div class="bg-white flex w-fit p-2 rounded justify-center items-center transition-transform duration-200 hover:-translate-y-0.5 hover:shadow-lg">
                <img :src="defaultLogo3" class="h-20 sm:h-20" alt="Logo" />
              </div>
              <div class="bg-white flex w-fit p-2 rounded justify-center items-center transition-transform duration-200 hover:-translate-y-0.5 hover:shadow-lg">
                <img :src="defaultLogo4" class="h-20 sm:h-14" alt="Logo" />
              </div>
            </template>
          </div>

          <nav class="flex flex-col gap-2.5 items-start">
            <router-link :to="{ name: 'ueber-das-tool' }" class="footer-link">
              <Info :size="18" class="shrink-0" />
              <span>Über das Tool</span>
            </router-link>
            <a
              class="footer-link"
              href="https://ritmo-hsrm.github.io/mobilitaetscheck-fuer-magistratsvorlagen/"
              target="_blank"
            >
              <BookOpen :size="18" class="shrink-0" />
              <span>Dokumentation und Hilfe</span>
            </a>
            <a
              class="footer-link"
              href="https://github.com/ritmo-hsrm/mobilitaetscheck-fuer-magistratsvorlagen"
              target="_blank"
            >
              <Github :size="18" class="shrink-0" />
              <span>Github-Repo</span>
            </a>
          </nav>

          <nav class="flex flex-col gap-2.5 items-start">
            <a
              v-if="einstellungStore.einstellung.impressumModus === 'url' && einstellungStore.einstellung.impressumUrl"
              class="footer-link"
              :href="einstellungStore.einstellung.impressumUrl"
              target="_blank"
              rel="noopener noreferrer"
            >
              <ScrollText :size="18" class="shrink-0" />
              <span>Impressum</span>
            </a>
            <router-link v-else class="footer-link" :to="{ name: 'impressum' }">
              <ScrollText :size="18" class="shrink-0" />
              <span>Impressum</span>
            </router-link>

            <a
              v-if="einstellungStore.einstellung.datenschutzModus === 'url' && einstellungStore.einstellung.datenschutzUrl"
              class="footer-link"
              :href="einstellungStore.einstellung.datenschutzUrl"
              target="_blank"
              rel="noopener noreferrer"
            >
              <ShieldCheck :size="18" class="shrink-0" />
              <span>Datenschutzerklärung</span>
            </a>
            <router-link v-else class="footer-link" :to="{ name: 'datenschutzerklaerung' }">
              <ShieldCheck :size="18" class="shrink-0" />
              <span>Datenschutzerklärung</span>
            </router-link>

            <a
              v-if="einstellungStore.einstellung.nutzungsbedingungenModus === 'url' && einstellungStore.einstellung.nutzungsbedingungenUrl"
              class="footer-link"
              :href="einstellungStore.einstellung.nutzungsbedingungenUrl"
              target="_blank"
              rel="noopener noreferrer"
            >
              <FileCheck2 :size="18" class="shrink-0" />
              <span>Nutzungsbedingungen</span>
            </a>
            <router-link v-else class="footer-link" :to="{ name: 'nutzungsbedingungen' }">
              <FileCheck2 :size="18" class="shrink-0" />
              <span>Nutzungsbedingungen</span>
            </router-link>
          </nav>
        </div>
        <p class="mt-8 text-blue-200 flex items-center justify-center gap-1.5">
          <Heart :size="14" class="shrink-0 fill-current text-red-400" />
          <span>&copy; 2026 Hochschule RheinMain</span>
        </p>
      </div>
    </footer>
  </div>
</template>

<script setup>
import { useBrandingStore } from '@/stores/branding'
import { useEinstellungStore } from '@/stores/einstellung'
import BrandingLogoLink from './BrandingLogoLink.vue'
import defaultLogo1 from '../assets/logos/HSRM_Unterzeile_farbig_RGB.png'
import defaultLogo2 from '../assets/logos/oberursel-logo.webp'
import defaultLogo3 from '../assets/logos/BMFTR.jpg'
import defaultLogo4 from '../assets/logos/FONA.jpg'
import { Info, BookOpen, Github, ScrollText, ShieldCheck, FileCheck2, Heart } from 'lucide-vue-next'

const brandingStore = useBrandingStore()
const einstellungStore = useEinstellungStore()
</script>

<style scoped>
.footer-link {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  transition:
    transform 0.15s ease,
    color 0.15s ease;
}

.footer-link:hover {
  color: theme('colors.blue.200');
  transform: translateX(3px);
}

.footer-link:hover :deep(svg) {
  transform: scale(1.15) rotate(-6deg);
}

.footer-link :deep(svg) {
  transition: transform 0.15s ease;
}
</style>
