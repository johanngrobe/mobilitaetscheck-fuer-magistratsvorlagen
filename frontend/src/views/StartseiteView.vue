<template>
  <div>
    <!-- Hero -->
    <div class="text-center py-10 px-4">
      <div
        class="max-w-2xl mx-auto mb-8"
        v-html="startseiteInhalt || STARTSEITE_STANDARD_INHALT"
      />

      <div class="flex flex-col items-center gap-2">
        <label class="font-semibold text-lg">Kommune auswählen</label>
        <Select
          v-model="selectedGemeindeId"
          :options="gemeinden"
          optionLabel="name"
          optionValue="id"
          placeholder="Kommune auswählen..."
          class="w-80"
          :loading="isLoadingGemeinden"
          filter
          filterPlaceholder="Suchen..."
          @change="onGemeindeChange"
        />
      </div>
    </div>

    <!-- Magistratsvorlage list -->
    <template v-if="selectedGemeindeId !== null">
      <div class="flex items-center gap-3 mb-4">
        <InputText
          v-model="searchQuery"
          placeholder="Nach Magistratsvorlage suchen..."
          class="w-full max-w-md"
        />
        <span class="text-gray-500 text-sm whitespace-nowrap">
          {{ filteredVorlagen.length }} Vorlage{{ filteredVorlagen.length !== 1 ? 'n' : '' }}
        </span>
      </div>

      <BaseSpinner v-if="isLoadingVorlagen" class="m-10" />
      <template v-else>
        <p v-if="magistratsvorlagen.length === 0" class="text-gray-500 text-center py-8">
          Keine veröffentlichten Magistratsvorlagen für diese Kommune vorhanden.
        </p>
        <DataView v-else :value="filteredVorlagen" paginator :rows="10">
          <template #list="slotProps">
            <div class="flex flex-col">
              <div v-for="item in slotProps.items" :key="item.id">
                <router-link
                  :to="{
                    name: 'oeffentlich-magistratsvorlage-id',
                    params: { id: item.id },
                    query: { gemeinde: selectedGemeindeId }
                  }"
                  custom
                  v-slot="{ navigate, href }"
                >
                  <BaseCard
                    class="hover:bg-gray-50 cursor-pointer"
                    :data-href="href"
                    @click="navigate"
                    @keydown.enter.prevent="navigate"
                    @keydown.space.prevent="navigate"
                    tabindex="0"
                  >
                    <template #header>
                      <span class="font-bold text-lg">{{ item.name }}</span>
                    </template>
                    <div class="grid grid-cols-12 gap-4 mt-2">
                      <div class="col-span-7 grid grid-cols-5 gap-x-2 text-sm">
                        <div class="col-span-2 font-semibold grid grid-cols-1 gap-y-1">
                          <div>Nr.</div>
                          <div>Datum</div>
                          <div v-if="item.gemeindeGebiete?.length > 0">Gebiete</div>
                          <div v-if="item.tags?.length > 0">Tags</div>
                        </div>
                        <div class="col-span-3 grid grid-cols-1 gap-y-1">
                          <div>{{ item.verwaltungsvorgangNr }}</div>
                          <div>{{ datumFormatieren(item.verwaltungsvorgangDatum) }}</div>
                          <div v-if="item.gemeindeGebiete?.length > 0" class="flex flex-wrap gap-1">
                            <Tag
                              v-for="g in item.gemeindeGebiete"
                              :key="g.id"
                              :value="g.name"
                              severity="secondary"
                              size="small"
                            />
                          </div>
                          <div v-if="item.tags?.length > 0" class="flex flex-wrap gap-1">
                            <Tag
                              v-for="t in item.tags"
                              :key="t.id"
                              :value="'#' + t.name"
                              severity="info"
                              size="small"
                            />
                          </div>
                        </div>
                      </div>
                      <div class="col-span-5 flex items-center justify-center gap-4">
                        <div class="flex flex-col items-center gap-1">
                          <i
                            :class="[
                              'pi text-xl',
                              item.mobilitaetschecks?.length > 0
                                ? 'pi-check-circle text-green-500'
                                : 'pi-times-circle text-gray-300'
                            ]"
                          />
                          <span class="text-xs text-gray-500">Mobilitätschecks</span>
                        </div>
                        <i class="pi pi-chevron-right text-gray-400" />
                      </div>
                    </div>
                  </BaseCard>
                </router-link>
              </div>
            </div>
          </template>
        </DataView>
      </template>
    </template>
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { apiClient } from '@/services/axios'
import BaseSpinner from '@/components/BaseSpinner.vue'
import DataView from 'primevue/dataview'
import InputText from 'primevue/inputtext'
import Select from 'primevue/select'
import Tag from 'primevue/tag'
import { STARTSEITE_STANDARD_INHALT } from '@/utils/standardInhalte'

const route = useRoute()
const router = useRouter()

const gemeinden = ref([])
const selectedGemeindeId = ref(null)
const magistratsvorlagen = ref([])
const searchQuery = ref('')
const isLoadingGemeinden = ref(true)
const startseiteInhalt = ref('')
const isLoadingVorlagen = ref(false)

const filteredVorlagen = computed(() => {
  const q = searchQuery.value.trim().toLowerCase()
  if (!q) return magistratsvorlagen.value
  return magistratsvorlagen.value.filter(
    (v) => v.name?.toLowerCase().includes(q) || v.verwaltungsvorgangNr?.toLowerCase().includes(q)
  )
})

const fetchGemeinden = async () => {
  isLoadingGemeinden.value = true
  const res = await apiClient.get('/public/gemeinden')
  gemeinden.value = res.data
  isLoadingGemeinden.value = false
}

const fetchMagistratsvorlagen = async (gemeindeId) => {
  isLoadingVorlagen.value = true
  magistratsvorlagen.value = []
  const res = await apiClient.get('/public/magistratsvorlage', {
    params: { gemeinde_id: gemeindeId }
  })
  magistratsvorlagen.value = res.data
  isLoadingVorlagen.value = false
}

const onGemeindeChange = () => {
  searchQuery.value = ''
  router.replace({ query: { gemeinde: selectedGemeindeId.value } })
}

const fetchStartseiteInhalt = async () => {
  try {
    const res = await apiClient.get('/public/plattform-einstellung')
    startseiteInhalt.value = res.data.startseiteInhalt || ''
  } catch {
    startseiteInhalt.value = ''
  }
}

onMounted(async () => {
  await Promise.all([fetchGemeinden(), fetchStartseiteInhalt()])
  const fromQuery = route.query.gemeinde ? Number(route.query.gemeinde) : null
  if (fromQuery) {
    selectedGemeindeId.value = fromQuery
    await fetchMagistratsvorlagen(fromQuery)
  }
})

watch(selectedGemeindeId, (id) => {
  if (id) fetchMagistratsvorlagen(id)
  else magistratsvorlagen.value = []
})

const datumFormatieren = (datum) => {
  if (!datum) return '–'
  return new Date(datum).toLocaleDateString('de-DE', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit'
  })
}
</script>
