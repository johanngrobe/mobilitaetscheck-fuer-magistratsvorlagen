<template>
  <Transition name="fade" mode="out-in">
    <div
      v-if="visible"
      class="relative max-w p-4 m-1 bg-white border border-gray-200 rounded-lg shadow dark:bg-gray-800 dark:border-gray-700 items-center content-center"
    >
      <!-- Close button, shown only if the closeable prop is true -->
      <button
        v-if="closeable"
        @click="closeCard"
        class="absolute top-5 right-5 p-1 text-gray-500 dark:text-gray-400 hover:text-gray-700 dark:hover:text-gray-300"
      >
        <img src="../assets/icons/MaterialSymbolsCancel.svg" alt="Close" class="w-6 h-6" />
      </button>
      <div class="gap-2">
        <div @click="toggleCollapse" class="cursor-pointer items-center">
          <slot name="header"></slot>
        </div>

        <Transition name="collapse">
          <div v-if="!isCollapsed">
            <slot></slot>
          </div>
        </Transition>
      </div>
    </div>
  </Transition>
</template>

<script setup>
import { ref } from 'vue'

// Props to control collapsible behavior, initial visibility, and close button visibility
const props = defineProps({
  collapsible: {
    type: Boolean,
    default: false
  },
  initiallyCollapsed: {
    type: Boolean,
    default: false
  },
  closeable: {
    type: Boolean,
    default: false
  },
  visible: {
    type: Boolean,
    default: true
  }
})

const isCollapsed = ref(props.initiallyCollapsed)
const visible = ref(props.visible)

// Method to toggle collapse
function toggleCollapse() {
  if (props.collapsible) {
    isCollapsed.value = !isCollapsed.value
  }
}

// Method to close the card
function closeCard() {
  visible.value = false
}
</script>

<style scoped>
/* Fade transition for showing and hiding the card */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

/* Collapse transition for showing and hiding content */
.collapse-enter-active,
.collapse-leave-active {
  transition: max-height 0.3s ease;
}
.collapse-enter-from,
.collapse-leave-to {
  max-height: 0;
  overflow: hidden;
}
</style>
