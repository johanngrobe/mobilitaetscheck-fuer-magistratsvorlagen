<template>
  <div>
    <Drawer v-model:visible="drawerVisible" header="Filter" position="right">
      <div class="grid grid-cols-1 gap-4">
        <div>
          <label class="mb-2 block font-bold">Verwaltungsvorgänge</label>
          <Listbox
            v-model="selectedVorgaenge"
            :options="vorgangOptions"
            class="w-64"
            multiple
            showClear
          />
        </div>
        <div>
          <label class="mb-2 block font-bold">Gemeindegebiet</label>
          <Listbox
            v-model="selectedGebiete"
            :options="gebietOptions"
            optionLabel="name"
            optionValue="id"
            class="w-64"
            multiple
            showClear
          />
        </div>
        <div>
          <label class="mb-2 block font-bold">Tag</label>
          <Listbox
            v-model="selectedTags"
            :options="tagOptions"
            optionLabel="name"
            optionValue="id"
            class="w-64"
            multiple
            showClear
          />
        </div>

        <DatePicker
          v-model="selectedDatum"
          placeholder="Datum auswählen"
          showIcon
          selectionMode="range"
          :manualInput="false"
          class="w-64"
        />
        <Card>
          <template #content>
            <div class="grid grid-cols-1 gap-4">
              <div class="flex items-center justify-between">
                <label>Mobilitätscheck vorhanden</label>
                <ToggleSwitch v-model="filterMobilitaetscheckVorhanden" />
              </div>
              <div class="flex items-center justify-between">
                <label>Klimacheck vorhanden</label>
                <ToggleSwitch v-model="filterKlimacheckVorhanden" />
              </div>
              <div class="flex items-center justify-between">
                <label>Klimarelevanzprüfung vorhanden</label>
                <ToggleSwitch v-model="filterKlimarelevanzpruefungVorhanden" />
              </div>
            </div>
          </template>
        </Card>

        <Button
          icon="pi pi-undo"
          label="Filter zurücksetzen"
          @click="resetFilters"
          severity="secondary"
          outlined
        />
      </div>
    </Drawer>

    <div class="flex flex-wrap items-center justify-between gap-4 mb-4">
      <InputText v-model="searchQuery" placeholder="Nach Magistratsvorlage suchen" class="w-1/2" />
      <SelectButton
        v-model="filterVonMirErstellt"
        :options="[
          { label: 'Alle', value: false, icon: 'pi pi-users' },
          { label: 'Von mir', value: true, icon: 'pi pi-user' }
        ]"
        optionLabel="label"
        optionValue="value"
      >
        <template #option="slotProps">
          <i :class="slotProps.option.icon"></i>
          <span class="ml-2">{{ slotProps.option.label }}</span>
        </template>
      </SelectButton>
      <div class="flex gap-4">
        <Button
          v-tooltip.top="'Filter zurücksetzen'"
          icon="pi pi-undo"
          @click="resetFilters"
          severity="secondary"
          outlined
        />
        <Button
          v-tooltip.top="'Filter'"
          icon="pi pi-sliders-h"
          @click="drawerVisible = true"
          :badge="countFilter"
        />
      </div>
    </div>
    <DataView
      :value="isLoading ? Array(5).fill({}) : filteredMagistratsvorlagen"
      paginator
      :rows="10"
    >
      <template #list="slotProps">
        <div class="flex flex-col">
          <template v-if="isLoading === true">
            <div v-for="i in slotProps.items" :key="i">
              <BaseCard>
                <div class="flex flex-col xl:flex-row xl:items-start gap-6">
                  <Skeleton class="!w-9/12 sm:!w-64 xl:!w-40 !h-24 mx-auto" />
                  <div
                    class="flex flex-col sm:flex-row justify-between items-center xl:items-start flex-1 gap-6"
                  >
                    <div class="flex flex-col items-center sm:items-start gap-4">
                      <Skeleton width="8rem" height="2rem" />
                      <Skeleton width="6rem" height="1rem" />

                      <div class="flex items-center gap-4">
                        <Skeleton width="6rem" height="1rem" />
                        <Skeleton width="3rem" height="1rem" />
                      </div>
                    </div>
                    <div class="flex sm:flex-col items-center sm:items-end gap-4 sm:gap-2">
                      <Skeleton width="4rem" height="2rem" />
                      <Skeleton size="3rem" shape="circle" />
                    </div>
                  </div>
                </div>
              </BaseCard>
            </div>
          </template>
          <template v-else>
            <div v-for="(item, index) in slotProps.items" :key="index">
              <router-link
                :to="{ name: 'magistratsvorlage-id-daten', params: { id: item.id } }"
                custom
                v-slot="{ navigate, href }"
              >
                <BaseCard
                  class="hover:bg-gray-100"
                  :data-href="href"
                  @click="navigate"
                  @keydown.enter.prevent="navigate"
                  @keydown.space.prevent="navigate"
                  tabindex="0"
                >
                  <template #header
                    ><span class="font-bold text-lg">{{ item.name }}</span></template
                  >
                  <div class="grid grid-cols-12 gap-4">
                    <div class="col-span-5 flex grid grid-cols-5 gap-x-2 gap-y-4">
                      <div class="col-span-1 font-bold grid grid-cols-1 gap-y-1.5">
                        <div>Nr.</div>
                        <div>Datum</div>
                        <div v-if="item.gemeindeGebiete.length > 0">Gebiete</div>
                        <div v-if="item.tags.length > 0">Tags</div>
                      </div>
                      <div class="col-span-4 grid grid-cols-1 gap-y-1.5">
                        <div>{{ item.verwaltungsvorgangNr }}</div>
                        <div>{{ datumFormatieren(item.verwaltungsvorgangDatum) }}</div>
                        <div v-if="item.gemeindeGebiete.length > 0" class="flex items-center gap-2">
                          <span v-for="gebiet in item.gemeindeGebiete" :key="gebiet.id">
                            <Tag :value="gebiet.name" severity="secondary" />
                          </span>
                        </div>
                        <div v-if="item.tags.length > 0" class="flex items-center gap-2">
                          <span v-for="tag in item.tags" :key="tag.id">
                            <Tag :value="'#' + tag.name" severity="info" />
                          </span>
                        </div>
                      </div>
                    </div>
                    <div class="col-span-3 font-bold">
                      <div class="flex items-center gap-2">
                        <router-link
                          :to="{
                            name: 'magistratsvorlage-id-mobilitaetscheck',
                            params: { id: item.id }
                          }"
                        >
                          <Button
                            :icon="
                              item.mobilitaetschecks.length > 0
                                ? 'pi pi-check-circle text-green-500'
                                : 'pi pi-times-circle text-red-400'
                            "
                            label="Mobilitätscheck"
                            variant="text"
                          />
                        </router-link>
                      </div>
                      <div class="flex items-center gap-2">
                        <router-link
                          :to="{
                            name: 'magistratsvorlage-id-klimacheck',
                            params: { id: item.id }
                          }"
                        >
                          <Button
                            :icon="
                              item.klimachecks.length > 0
                                ? 'pi pi-check-circle text-green-500'
                                : 'pi pi-times-circle text-red-400'
                            "
                            label="Klimacheck"
                            variant="text"
                          />
                        </router-link>
                      </div>
                    </div>
                    <!-- TODO Klimarelevanzprüfung -->
                    <div class="col-span-3 font-bold">
                      <div class="flex items-center gap-2">
                        <router-link
                          :to="{
                            name: 'magistratsvorlage-id-klimarelevanzpruefung',
                            params: { id: item.id }
                          }"
                        >
                          <Button
                            :icon="
                              item.klimachecks.length > 0
                                ? 'pi pi-check-circle text-green-500'
                                : 'pi pi-times-circle text-red-400'
                            "
                            label="Klimarelevanzprüfung"
                            variant="text"
                          />
                        </router-link>
                      </div>
                    </div>
                  </div>
                </BaseCard>
              </router-link>
            </div>
          </template>
        </div>
      </template>
    </DataView>
  </div>
</template>

<script setup>
import { computed, ref, onMounted } from 'vue'
import { fetchItems } from '@/composables/crud'
import Button from 'primevue/button'
import Card from 'primevue/card'
import DataView from 'primevue/dataview'
import DatePicker from 'primevue/datepicker'
import Drawer from 'primevue/drawer'
import InputText from 'primevue/inputtext'
import Tag from 'primevue/tag'
import SelectButton from 'primevue/selectbutton'
import Skeleton from 'primevue/skeleton'
import ToggleSwitch from 'primevue/toggleswitch'
import Listbox from 'primevue/listbox'

const magistratsvorlageListe = ref([])
const searchQuery = ref('')
const selectedGebiete = ref([])
const selectedTags = ref([])
const selectedDatum = ref()
const selectedVorgaenge = ref([])
const gebietOptions = ref([])
const tagOptions = ref([])
const vorgangOptions = ref([])
const isLoading = ref(true)
const drawerVisible = ref(false)
const filterMobilitaetscheckVorhanden = ref(false)
const filterKlimacheckVorhanden = ref(false)
const filterKlimarelevanzpruefungVorhanden = ref(false)
const filterVonMirErstellt = ref(false)

onMounted(async () => {
  isLoading.value = true
  await fetchData()
  isLoading.value = false
})

const fetchData = async () => {
  magistratsvorlageListe.value = await fetchItems('/magistratsvorlage')
  gebietOptions.value = await fetchItems('/einstellungen/gebiet')
  tagOptions.value = await fetchItems('/einstellungen/tag')
  vorgangOptions.value = await fetchItems('/magistratsvorlage/vorgaenge')
}

const countFilter = computed(() => {
  let count = 0
  if (selectedVorgaenge.value.length > 0) count++
  if (selectedGebiete.value.length > 0) count++
  if (selectedTags.value.length > 0) count++
  if (selectedDatum.value && selectedDatum.value.length === 2) count++
  if (filterMobilitaetscheckVorhanden.value) count++
  if (filterKlimacheckVorhanden.value) count++
  if (filterKlimarelevanzpruefungVorhanden.value) count++
  if (filterVonMirErstellt.value) count++
  return String(count)
})

const resetFilters = () => {
  selectedVorgaenge.value = []
  selectedGebiete.value = []
  selectedTags.value = []
  selectedDatum.value = null
  searchQuery.value = ''
  filterMobilitaetscheckVorhanden.value = false
  filterKlimacheckVorhanden.value = false
  filterKlimarelevanzpruefungVorhanden.value = false
  filterVonMirErstellt.value = false
}

const datumFormatieren = (datum) => {
  return new Date(datum).toLocaleDateString('de-DE', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit'
  })
}

const filteredMagistratsvorlagen = computed(() => {
  const query = searchQuery.value?.toLowerCase().trim() || ''

  const extractVal = (s) => {
    if (s === null || s === undefined) return String(s)
    if (typeof s === 'object') return String(s.id ?? s.value ?? s)
    return String(s)
  }

  const selectedVorgangValues = (selectedVorgaenge.value || []).map(extractVal)
  const selectedGebieteValues = (selectedGebiete.value || []).map(extractVal)
  const selectedTagValues = (selectedTags.value || []).map(extractVal)

  return magistratsvorlageListe.value.filter((item) => {
    const matchName = !query || item.name?.toLowerCase().includes(query)

    const matchVorgang = (() => {
      if (!selectedVorgangValues || selectedVorgangValues.length === 0) return true
      return selectedVorgangValues.includes(String(item.verwaltungsvorgangNr))
    })()

    const matchGebiet =
      !selectedGebiete.value ||
      selectedGebiete.value.length === 0 ||
      item.gemeindeGebiete?.some((g) => selectedGebieteValues.includes(String(g.id)))

    const matchTag =
      !selectedTags.value ||
      selectedTags.value.length === 0 ||
      item.tags?.some((t) => selectedTagValues.includes(String(t.id)))

    const matchDatum = (() => {
      if (!selectedDatum.value || selectedDatum.value.length < 2) return true
      const [start, end] = selectedDatum.value
      const itemDate = new Date(item.verwaltungsvorgangDatum)
      return itemDate >= new Date(start) && itemDate <= new Date(end)
    })()

    const matchMobilitaetscheck =
      !filterMobilitaetscheckVorhanden.value ||
      (item.mobilitaetschecks && item.mobilitaetschecks.length > 0)

    const matchKlimacheck =
      !filterKlimacheckVorhanden.value || (item.klimachecks && item.klimachecks.length > 0)

    const matchKlimarelevanzpruefung =
      !filterKlimarelevanzpruefungVorhanden.value ||
      (item.klimarelevanzpruefung && item.klimarelevanzpruefung.length > 0) ||
      (item.klimarelevanzpruefungen && item.klimarelevanzpruefungen.length > 0)

    const matchVonMir = (() => {
      if (!filterVonMirErstellt.value) return true
      return localStorage.getItem('userId').includes(String(item.erstelltVon))
    })()

    return (
      matchName &&
      matchGebiet &&
      matchTag &&
      matchVorgang &&
      matchDatum &&
      matchMobilitaetscheck &&
      matchKlimacheck &&
      matchKlimarelevanzpruefung &&
      matchVonMir
    )
  })
})
</script>

<style></style>
