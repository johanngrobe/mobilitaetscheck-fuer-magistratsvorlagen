<template>
  <div>
    <form @submit.prevent="onSubmit">
      <div class="w-full">
        <FloatLabel variant="on">
          <InputText id="name" v-model="name" class="w-full" :invalid="!!errors.name" />
          <label for="name" class="text-lg flex items-center justify-center gap-2 font-bold">
            Name des Mobilitätschecks
          </label>
        </FloatLabel>
      </div>
      <div v-for="(eingabeZielOber, index) in props.item.eingabeZielOber" :key="eingabeZielOber.id">
        <BaseCard>
          {{ eingabeZielOber.name }}
          <MobilitaetscheckFormularEingabeZielOberItem
            :editMode="props.editMode"
            :item="eingabeZielOber"
            :ref="(el) => registerOberRef(el, index)"
          />
        </BaseCard>
      </div>
      <div class="flex justify-end items-center mt-4">
        <Button
          icon="pi pi-save"
          @click="handleSubmit"
          type="submit"
          label="speichern"
          :loading="isLoading"
        />
      </div>
    </form>
  </div>
</template>

<script setup>
import { onMounted, ref, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useForm } from 'vee-validate'
import { updateItem } from '@/composables/crud'
import { schema } from '@/utils/schemas/mobilitaetscheckEingabe'
import InputText from 'primevue/inputtext'
import FloatLabel from 'primevue/floatlabel'
import Button from 'primevue/button'
import { toastService } from '@/services/toast'
import MobilitaetscheckFormularEingabeZielOberItem from '@/components/MobilitaetscheckFormularEingabeZielOberItem.vue'

const mobilitaetscheckFormularEingabeZielOberRefs = ref([])

const isLoading = ref(false)

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

const route = useRoute()
const router = useRouter()

const registerOberRef = (el, index) => {
  if (el) mobilitaetscheckFormularEingabeZielOberRefs.value[index] = el
}

const { defineField, handleSubmit, errors, setValues } = useForm({
  validationSchema: schema
})
const [name] = defineField('name')

onMounted(async () => {})

watch(
  () => props.item,
  (newItem) => {
    if (newItem) {
      setValues({
        name: props.item.name
      })
    }
  },
  { immediate: true }
)

const emit = defineEmits(['close-modal', 'reload-item'])

const onSubmit = handleSubmit(async (values) => {
  isLoading.value = true
  const refs = mobilitaetscheckFormularEingabeZielOberRefs.value.filter((ref) => ref)

  // Step 1: Call onSubmit() for each EingabeZielOberItem
  const submitResults = await Promise.all(refs.map((ref) => ref.onSubmit?.()))

  // Step 2: Check if any child onSubmit returned false (i.e., validation failed)
  const allSubmitted = submitResults.every((result) => result === true)

  if (!allSubmitted) {
    toastService.add({
      severity: 'error',
      summary: 'Fehler',
      detail: 'Bitte überprüfen Sie die Eingaben in den Zielen.'
    })
    isLoading.value = false
    return
  }
  await updateItem({
    model: 'mobilitaetscheck/eingabe',
    modelId: props.item.id,
    values,
    detail: {
      success: 'Mobilitätscheck erfolgreich aktualisiert',
      error: 'Fehler beim Aktualisieren des Mobilitätschecks'
    }
  })
  if (props.editMode) {
    emit('close-modal')
    emit('reload-item')
  } else {
    router.push({
      name: 'magistratsvorlage-id-mobilitaetscheck',
      params: { id: route.params.id }
    })
  }
  isLoading.value = false
})
</script>

<style></style>
