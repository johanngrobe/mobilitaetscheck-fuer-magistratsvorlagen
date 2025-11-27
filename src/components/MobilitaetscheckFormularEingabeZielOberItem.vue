<template>
  <div>
    <form @submit.prevent="onSubmit">
      <div>
        <div class="flex items-center gap-2 p-2" @click="toggleTangiert">
          <Checkbox
            id="checkbox"
            v-model="tangiert"
            :binary="true"
            class="flex-none"
            :invalid="!!errors.tangiert"
            @click="toggleTangiert"
          />
          <label for="checkbox" class="text-lg flex items-center justify-center gap-2 font-bold">
            <span>{{ props.item.zielOber.nr }}</span>
            <span>{{ props.item.zielOber.name }}</span>
          </label>
        </div>
        <div v-if="tangiert">
          <div
            v-for="(eingabeZielUnter, index) in props.item.eingabeZielUnter"
            :key="eingabeZielUnter.id"
          >
            <MobilitaetscheckFormularEingabeZielUnterItem
              :editMode="props.editMode"
              :item="eingabeZielUnter"
              :zielOberNr="props.item.zielOber.nr"
              :ref="(el) => registerUnterRef(el, index)"
            />
          </div>
        </div>
      </div>
    </form>
  </div>
</template>

<script setup>
import { onMounted, ref, watch } from 'vue'
import { useForm } from 'vee-validate'
import { updateItemSilent } from '@/composables/crud'
import { schema } from '@/utils/schemas/mobilitaetscheckEingabeZielOber'
import Checkbox from 'primevue/checkbox'
import MobilitaetscheckFormularEingabeZielUnterItem from '@/components/MobilitaetscheckFormularEingabeZielUnterItem.vue'

const mobilitaetscheckFormularEingabeZielUnterRefs = ref([])

const registerUnterRef = (el, index) => {
  if (el) mobilitaetscheckFormularEingabeZielUnterRefs.value[index] = el
}

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

const { defineField, handleSubmit, validate, errors, setFieldValue, setValues } = useForm({
  validationSchema: schema
})

const [tangiert] = defineField('tangiert')

onMounted(() => {})

watch(
  () => props.item,
  (newItem) => {
    if (!newItem) return
    const { tangiert, eingabeId, zielOberId } = props.item
    setValues({
      tangiert,
      eingabeId,
      zielOberId
    })
  },
  { immediate: true } // sofort beim ersten gesetzten Wert ausführen
)

const toggleTangiert = () => {
  setFieldValue('tangiert', !tangiert.value)
}

const onSubmit = handleSubmit(async (values) => {
  const refs = mobilitaetscheckFormularEingabeZielUnterRefs.value.filter((ref) => ref)

  // Step 1: Validate all sub-forms
  const validationResults = await Promise.all(refs.map((ref) => ref.validate?.()))
  const allValid = validationResults.every((result) => result?.valid === true)

  if (!allValid) {
    return false
  }

  await updateItemSilent({
    model: 'mobilitaetscheck/eingabe/ziel/ober',
    modelId: props.item.id,
    values
  })
  // Step 3: Submit all sub-forms
  await Promise.all(refs.map((ref) => ref.onSubmit?.()))
  return true
})

defineExpose({ onSubmit, validate })
</script>

<style scoped></style>
