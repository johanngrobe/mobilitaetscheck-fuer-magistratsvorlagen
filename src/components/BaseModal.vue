<template>
  <transition name="modal-fade">
    <div
      v-if="isVisible"
      tabindex="-1"
      class="fixed inset-0 z-50 flex justify-center items-center w-full h-full bg-black bg-opacity-50 backdrop-blur-md"
    >
      <div
        ref="modalContent"
        class="relative p-4 w-full max-w-6xl max-h-full overflow-y-auto"
        @touchmove.prevent
      >
        <!-- Modal content -->
        <div class="relative bg-white rounded-lg shadow dark:bg-gray-700">
          <!-- Modal header -->
          <div
            class="flex items-center justify-between p-4 md:p-5 border-b rounded-t dark:border-gray-600"
          >
            <!-- Slot for header content -->
            <h3 class="text-lg font-semibold text-gray-900 dark:text-white">
              <slot name="header"> </slot>
            </h3>
            <!-- Close button -->
            <button
              type="button"
              class="text-gray-400 bg-transparent hover:bg-gray-200 hover:text-gray-900 rounded-lg text-sm w-8 h-8 ms-auto inline-flex justify-center items-center dark:hover:bg-gray-600 dark:hover:text-white"
              @click="closeModal"
            >
              <svg
                class="w-3 h-3"
                aria-hidden="true"
                xmlns="http://www.w3.org/2000/svg"
                fill="none"
                viewBox="0 0 14 14"
              >
                <path
                  stroke="currentColor"
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="m1 1 6 6m0 0 6 6M7 7l6-6M7 7l-6 6"
                />
              </svg>
              <span class="sr-only">Close modal</span>
            </button>
          </div>
          <!-- Modal body -->
          <div class="p-4 md:p-5">
            <!-- Slot for body content -->
            <slot></slot>
          </div>
          <!-- Modal footer -->
          <div
            class="flex items-center p-4 md:p-5 border-t border-gray-200 rounded-b dark:border-gray-600"
          >
            <!-- Slot for footer content -->
            <slot name="footer">
              <!-- <BaseButton @click="closeModal" :outline="false"> Close </BaseButton> -->
            </slot>
          </div>
        </div>
      </div>
    </div>
  </transition>
</template>

<script setup>
import { ref, onBeforeUnmount, watch } from 'vue'
import { onClickOutside, useMagicKeys } from '@vueuse/core'

const keys = useMagicKeys()
const escape = keys['Escape']

const isVisible = defineModel()

// Function to close the modal
const closeModal = () => {
  isVisible.value = false
  // emit('update:modelValue', false)
  toggleBodyScroll(false)
}

// Disable body scroll when modal is open
const toggleBodyScroll = (isOpen) => {
  if (isOpen) {
    document.body.style.position = 'fixed'
    document.body.style.width = '100%'
  } else {
    document.body.style.position = ''
    document.body.style.width = ''
  }
}

// Ensure body scroll is restored when the component is destroyed
onBeforeUnmount(() => {
  toggleBodyScroll(false)
})

const getIgnoreElements = () => {
  let ignoreElements = [
    `[rolle=listbox]`,
    '[data-pc-section="overlay"]',
    '[data-pc-section="panel"]'
  ]
  return ignoreElements
}

watch(escape, (v) => {
  if (v) closeModal()
})

// Close modal when clicking outside the modal content
const modalContent = ref(null)
onClickOutside(modalContent, closeModal, {
  ignore: getIgnoreElements()
})
</script>

<style scoped>
/* Transition for modal fade in/out */
.modal-fade-enter-active,
.modal-fade-leave-active {
  transition: opacity 0.3s ease;
}
.modal-fade-enter-from,
.modal-fade-leave-to {
  opacity: 0;
}

/* Prevent scrolling on the page when the modal is open */
.no-scroll {
  overflow: hidden;
}
</style>
