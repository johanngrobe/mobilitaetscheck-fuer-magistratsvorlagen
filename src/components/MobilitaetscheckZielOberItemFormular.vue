<template>
  <div>
    <form @submit.prevent="onSubmit">
      <div>
        <div class="flex items-center gap-2 p-2" @click="toggleTarget">
          <Checkbox
            id="checkbox"
            v-model="target"
            :binary="true"
            class="flex-none"
            :invalid="!!errors.target"
            @click="toggleTarget"
          />
          <label for="checkbox" class="text-lg flex items-center justify-center gap-2 font-bold">
            <span>{{ props.item.mainObjective.no }}</span>
            <span>{{ props.item.mainObjective.label }}</span>
          </label>
        </div>
        <div v-if="target">
          <div v-for="subObjective in props.item.subObjectives" :key="subObjective.id">
            <MobilityObjectiveFormItemSub :editMode="props.editMode" :item="subObjective" />
          </div>
        </div>
      </div>
    </form>
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { useForm } from 'vee-validate'
import { schema } from '@/utils/schemas/mobilitaetscheckEingabeZielOber'
import Checkbox from 'primevue/checkbox'
import MobilityObjectiveFormItemSub from '@/components/MobilitaetscheckFormularZielUnterItem.vue'

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

const { defineField, handleSubmit, errors, setFieldValue, setValues } = useForm({
  validationSchema: schema
})

const [target] = defineField('target')

onMounted(() => {
  if (props.item) {
    setValues(props.item)
  }
})

const toggleTarget = () => {
  setFieldValue('target', !target.value)
}

const emit = defineEmits(['submit-item'])

const onSubmit = handleSubmit(async (values) => {
  emit('submit-item', values)
})
</script>

<style scoped></style>
