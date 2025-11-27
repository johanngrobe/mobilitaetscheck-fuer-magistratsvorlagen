import { ref } from 'vue'
import { defineStore } from 'pinia'

export const useMobilitaetscheckEingabeStore = defineStore('mobilitaetscheckEingabe', () => {
  const mobilitaetscheckEingabeItems = ref([])
  const isLoading = ref(false)

  const forumularGueltig = ref({
    eingabe: false,
    eingabeZiel: false
  })

  const currentEingabeId = ref(null)

  const editMode = ref(false)

  async function $reset() {
    currentEingabeId.value = null

    forumularGueltig.value = {
      eingabe: false,
      eingabeZiel: false
    }
    editMode.value = false
  }

  return {
    isLoading,
    forumularGueltig,
    currentEingabeId,
    editMode,
    mobilitaetscheckEingabeItems,
    $reset
  }
})
