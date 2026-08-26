<template>
  <div class="rich-content-editor border rounded-md" :class="{ 'border-red-400': invalid }">
    <div v-if="editor" class="toolbar flex flex-wrap items-center gap-1 border-b p-1 bg-gray-50">
      <Select
        :modelValue="activeHeadingLevel"
        @update:modelValue="setHeading"
        :options="headingOptions"
        optionLabel="label"
        optionValue="value"
        class="w-36 mr-1"
        size="small"
      />

      <span class="toolbar-divider" />

      <button
        type="button"
        class="toolbar-btn"
        :class="{ 'is-active': editor.isActive('bold') }"
        title="Fett"
        @click="editor.chain().focus().toggleBold().run()"
      >
        <span class="glyph-bold">B</span>
      </button>
      <button
        type="button"
        class="toolbar-btn"
        :class="{ 'is-active': editor.isActive('italic') }"
        title="Kursiv"
        @click="editor.chain().focus().toggleItalic().run()"
      >
        <span class="glyph-italic">I</span>
      </button>
      <button
        type="button"
        class="toolbar-btn"
        :class="{ 'is-active': editor.isActive('underline') }"
        title="Unterstrichen"
        @click="editor.chain().focus().toggleUnderline().run()"
      >
        <span class="glyph-underline">U</span>
      </button>
      <button
        type="button"
        class="toolbar-btn"
        :class="{ 'is-active': editor.isActive('strike') }"
        title="Durchgestrichen"
        @click="editor.chain().focus().toggleStrike().run()"
      >
        <span class="glyph-strike">S</span>
      </button>

      <span class="toolbar-divider" />

      <button
        type="button"
        class="toolbar-btn"
        :class="{ 'is-active': editor.isActive('bulletList') }"
        title="Aufzählung"
        @click="editor.chain().focus().toggleBulletList().run()"
      >
        <i class="pi pi-list" />
      </button>
      <button
        type="button"
        class="toolbar-btn"
        :class="{ 'is-active': editor.isActive('orderedList') }"
        title="Nummerierte Liste"
        @click="editor.chain().focus().toggleOrderedList().run()"
      >
        <i class="pi pi-sort-numeric-down" />
      </button>
      <button
        type="button"
        class="toolbar-btn"
        :class="{ 'is-active': editor.isActive('blockquote') }"
        title="Zitat"
        @click="editor.chain().focus().toggleBlockquote().run()"
      >
        <i class="pi pi-comment" />
      </button>

      <span class="toolbar-divider" />

      <button
        type="button"
        class="toolbar-btn"
        :class="{ 'is-active': editor.isActive('link') }"
        title="Link"
        @click="toggleLink"
      >
        <i class="pi pi-link" />
      </button>
      <button type="button" class="toolbar-btn" title="Bild einfügen" @click="selectAndUploadImage">
        <i class="pi pi-image" />
      </button>
      <button
        type="button"
        class="toolbar-btn"
        title="Tabelle einfügen"
        @click="editor.chain().focus().insertTable({ rows: 3, cols: 3, withHeaderRow: true }).run()"
      >
        <i class="pi pi-table" />
      </button>

      <span class="toolbar-divider" />
      <button
        type="button"
        class="toolbar-btn"
        title="Spalte davor einfügen"
        :disabled="!editor.isActive('table')"
        @click="editor.chain().focus().addColumnBefore().run()"
      >
        <i class="pi pi-arrow-left" />
      </button>
      <button
        type="button"
        class="toolbar-btn"
        title="Spalte danach einfügen"
        :disabled="!editor.isActive('table')"
        @click="editor.chain().focus().addColumnAfter().run()"
      >
        <i class="pi pi-arrow-right" />
      </button>
      <button
        type="button"
        class="toolbar-btn"
        title="Spalte löschen"
        :disabled="!editor.isActive('table')"
        @click="editor.chain().focus().deleteColumn().run()"
      >
        <i class="pi pi-minus-circle" />
      </button>
      <button
        type="button"
        class="toolbar-btn"
        title="Zeile davor einfügen"
        :disabled="!editor.isActive('table')"
        @click="editor.chain().focus().addRowBefore().run()"
      >
        <i class="pi pi-arrow-up" />
      </button>
      <button
        type="button"
        class="toolbar-btn"
        title="Zeile danach einfügen"
        :disabled="!editor.isActive('table')"
        @click="editor.chain().focus().addRowAfter().run()"
      >
        <i class="pi pi-arrow-down" />
      </button>
      <button
        type="button"
        class="toolbar-btn"
        title="Zeile löschen"
        :disabled="!editor.isActive('table')"
        @click="editor.chain().focus().deleteRow().run()"
      >
        <i class="pi pi-minus-circle" />
      </button>
      <button
        type="button"
        class="toolbar-btn"
        title="Tabelle löschen"
        :disabled="!editor.isActive('table')"
        @click="editor.chain().focus().deleteTable().run()"
      >
        <i class="pi pi-trash" />
      </button>

      <span class="toolbar-divider" />

      <button
        type="button"
        class="toolbar-btn"
        title="Formatierung entfernen"
        @click="editor.chain().focus().unsetAllMarks().clearNodes().run()"
      >
        <i class="pi pi-eraser" />
      </button>
      <button
        type="button"
        class="toolbar-btn"
        title="Rückgängig"
        :disabled="!editor.can().undo()"
        @click="editor.chain().focus().undo().run()"
      >
        <i class="pi pi-undo" />
      </button>
      <button
        type="button"
        class="toolbar-btn"
        title="Wiederholen"
        :disabled="!editor.can().redo()"
        @click="editor.chain().focus().redo().run()"
      >
        <i class="pi pi-refresh" />
      </button>

      <span class="toolbar-divider" />

      <button
        type="button"
        class="toolbar-btn"
        :class="{ 'is-active': isSourceView }"
        title="HTML-Quelltext"
        @click="toggleSourceView"
      >
        <i class="pi pi-code" />
      </button>
    </div>

    <textarea
      v-if="isSourceView"
      v-model="sourceHtml"
      class="content-area source-view"
      :style="editorStyle"
      spellcheck="false"
    />
    <EditorContent v-else :editor="editor" class="content-area" :style="editorStyle" />
  </div>
</template>

<script setup>
import { onBeforeUnmount, computed, watch, ref } from 'vue'
import { useEditor, EditorContent } from '@tiptap/vue-3'
import StarterKit from '@tiptap/starter-kit'
import Underline from '@tiptap/extension-underline'
import Link from '@tiptap/extension-link'
import ImageExtension from '@tiptap/extension-image'
import { Table, TableRow, TableHeader, TableCell } from '@tiptap/extension-table'
import Select from 'primevue/select'
import { apiClient } from '@/services/axios'
import { useToast } from 'primevue/usetoast'

const props = defineProps({
  modelValue: {
    type: String,
    default: ''
  },
  editorStyle: {
    type: String,
    default: 'min-height: 320px'
  },
  invalid: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['update:modelValue'])

const toast = useToast()

const headingOptions = [
  { label: 'Absatz', value: 0 },
  { label: 'Überschrift 1', value: 1 },
  { label: 'Überschrift 2', value: 2 },
  { label: 'Überschrift 3', value: 3 }
]

const editor = useEditor({
  content: props.modelValue,
  extensions: [
    StarterKit.configure({ link: false, underline: false }),
    Underline,
    Link.configure({ openOnClick: false, autolink: true }),
    ImageExtension,
    Table.configure({ resizable: true }),
    TableRow,
    TableHeader,
    TableCell
  ],
  editorProps: {
    attributes: {
      class: 'tiptap-prose'
    }
  },
  onUpdate: ({ editor: instance }) => {
    emit('update:modelValue', instance.getHTML())
  }
})

const activeHeadingLevel = computed(() => {
  if (!editor.value) return 0
  for (const level of [1, 2, 3]) {
    if (editor.value.isActive('heading', { level })) return level
  }
  return 0
})

const setHeading = (level) => {
  if (!editor.value) return
  if (level === 0) {
    editor.value.chain().focus().setParagraph().run()
  } else {
    editor.value.chain().focus().toggleHeading({ level }).run()
  }
}

const toggleLink = () => {
  if (!editor.value) return
  if (editor.value.isActive('link')) {
    editor.value.chain().focus().unsetLink().run()
    return
  }
  const url = window.prompt('URL des Links')
  if (!url) return
  editor.value.chain().focus().setLink({ href: url }).run()
}

const selectAndUploadImage = () => {
  if (!editor.value) return
  const input = document.createElement('input')
  input.setAttribute('type', 'file')
  input.setAttribute('accept', 'image/*')
  input.onchange = async () => {
    const file = input.files?.[0]
    if (!file) return

    const formData = new FormData()
    formData.append('file', file)

    try {
      const res = await apiClient.post('/branding/assets', formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      })
      editor.value.chain().focus().setImage({ src: res.data.url }).run()
    } catch {
      toast.add({
        severity: 'error',
        summary: 'Fehler',
        detail: 'Bild konnte nicht hochgeladen werden.',
        life: 3000
      })
    }
  }
  input.click()
}

watch(
  () => props.modelValue,
  (value) => {
    if (!editor.value) return
    const isSame = editor.value.getHTML() === value
    if (!isSame) {
      editor.value.commands.setContent(value || '', { emitUpdate: false })
    }
  }
)

const isSourceView = ref(false)
const sourceHtml = ref('')

const toggleSourceView = () => {
  if (!editor.value) return
  if (isSourceView.value) {
    editor.value.commands.setContent(sourceHtml.value || '', { emitUpdate: true })
  } else {
    sourceHtml.value = editor.value.getHTML()
  }
  isSourceView.value = !isSourceView.value
}

onBeforeUnmount(() => {
  editor.value?.destroy()
})
</script>

<style scoped>
.toolbar-btn {
  @apply w-8 h-8 flex items-center justify-center rounded text-gray-600 hover:bg-gray-200 transition-colors;
}

.toolbar-btn.is-active {
  @apply bg-blue-100 text-blue-700 ring-1 ring-blue-400;
}

.toolbar-btn:disabled {
  @apply opacity-40 cursor-not-allowed hover:bg-transparent;
}

.toolbar-divider {
  @apply w-px h-6 bg-gray-300 mx-1;
}

.glyph-bold,
.glyph-italic,
.glyph-underline,
.glyph-strike {
  @apply text-sm leading-none;
  font-family: Georgia, 'Times New Roman', serif;
}

.glyph-bold {
  font-weight: 700;
}

.glyph-italic {
  font-style: italic;
}

.glyph-underline {
  text-decoration: underline;
}

.glyph-strike {
  text-decoration: line-through;
}

.content-area {
  @apply p-3 overflow-y-auto;
}

.source-view {
  @apply w-full text-sm resize-none outline-none;
  font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace;
}

:deep(.tiptap-prose) {
  outline: none;
  min-height: inherit;
}

:deep(.tiptap-prose h1) {
  @apply text-2xl font-bold mb-2 mt-2;
}

:deep(.tiptap-prose h2) {
  @apply text-xl font-bold mb-2 mt-2;
}

:deep(.tiptap-prose h3) {
  @apply text-lg font-bold mb-2 mt-2;
}

:deep(.tiptap-prose p) {
  @apply mb-2;
}

:deep(.tiptap-prose strong) {
  font-weight: 700;
}

:deep(.tiptap-prose em) {
  font-style: italic;
}

:deep(.tiptap-prose u) {
  text-decoration: underline;
}

:deep(.tiptap-prose s) {
  text-decoration: line-through;
}

:deep(.tiptap-prose ul) {
  @apply list-disc pl-6 mb-2;
}

:deep(.tiptap-prose ol) {
  @apply list-decimal pl-6 mb-2;
}

:deep(.tiptap-prose blockquote) {
  @apply border-l-4 border-gray-300 pl-4 italic text-gray-600 mb-2;
}

:deep(.tiptap-prose a) {
  @apply text-blue-600 underline;
}

:deep(.tiptap-prose img) {
  @apply max-w-full;
}

:deep(.tiptap-prose table) {
  border-collapse: collapse;
  table-layout: fixed;
  width: 100%;
  margin-bottom: 0.5rem;
}

:deep(.tiptap-prose table td),
:deep(.tiptap-prose table th) {
  border: 1px solid #d1d5db;
  padding: 0.375rem 0.5rem;
  vertical-align: top;
  position: relative;
}

:deep(.tiptap-prose table th) {
  font-weight: 600;
  background-color: #f9fafb;
  text-align: left;
}

:deep(.tiptap-prose .selectedCell) {
  background-color: rgba(59, 130, 246, 0.15);
}

:deep(.tiptap-prose .column-resize-handle) {
  position: absolute;
  right: -2px;
  top: 0;
  bottom: 0;
  width: 4px;
  background-color: #3b82f6;
  pointer-events: none;
}

:deep(.tiptap-prose.resize-cursor) {
  cursor: col-resize;
}
</style>
