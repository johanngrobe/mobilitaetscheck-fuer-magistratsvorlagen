<template>
  <div>
    <div class="tab-container">
      <ul class="tab-list">
        <li v-for="tab in tabs" :key="tab.name" class="tab-item">
          <a
            href="#"
            @click.prevent="selectTab(tab)"
            class="tab-link"
            :class="tab.name === selectedTab.name ? 'active-tab' : 'inactive-tab'"
            :aria-current="tab.name === selectedTab.name ? 'page' : undefined"
          >
            {{ tab.label }}
          </a>
        </li>
      </ul>
    </div>
    <div v-if="selectedTab">
      <slot :name="selectedTab.name"></slot>
    </div>
  </div>
</template>

<script setup>
import { watchEffect, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'

const props = defineProps({
  tabs: {
    type: Array,
    required: true
  },
  defaultTab: {
    type: Object,
    required: false
  },
  disableUrlAltering: {
    type: Boolean,
    default: false
  }
})

const route = useRoute()
const router = useRouter()

// Computed property to initialize or update `selectedTab`
const selectedTab = computed({
  get() {
    const tabParam = route.query.tab
    return props.tabs.find((tab) => tab.name === tabParam) || props.defaultTab || props.tabs[0]
  },
  set(newTab) {
    if (newTab && !props.disableUrlAltering) {
      router.push({ query: { ...route.query, tab: newTab.name } })
    }
  }
})

// Function to select tab when a button is clicked
const selectTab = (tab) => {
  if (!tab.disabled) {
    selectedTab.value = tab
  }
}

// Sync the URL query parameter when `selectedTab` changes
watchEffect(() => {
  if (!props.disableUrlAltering) {
    const currentTab = selectedTab.value
    if (currentTab && route.query.tab !== currentTab.name) {
      router.replace({
        query: {
          ...route.query,
          tab: currentTab.name
        }
      })
    }
  }
})
</script>

<style scoped>
.tab-container {
  @apply text-sm font-medium text-center text-gray-500 border-b border-gray-200 dark:text-gray-400 dark:border-gray-700;
}

.tab-list {
  @apply flex flex-wrap -mb-px;
}

.tab-item {
  @apply me-2;
}

.tab-link {
  @apply inline-block p-4 rounded-t-lg border-b-2;
}

.active-tab {
  @apply text-blue-600  border-blue-600 dark:text-blue-500 dark:border-blue-500;
}

.inactive-tab {
  @apply border-transparent hover:text-gray-600 hover:border-gray-300 dark:hover:text-gray-300;
}

.disabled-tab {
  @apply text-gray-400 cursor-not-allowed dark:text-gray-500;
}
</style>
