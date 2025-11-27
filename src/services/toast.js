let toastInstance = null

export const toastService = {
  defaultOptions: {
    life: 3000 // Default duration in milliseconds
  },

  add(msg) {
    const toast = getToast()
    if (toast) {
      // Set default summaries based on severity
      const severityDefaults = {
        error: 'Fehler',
        success: 'Erfolgreich'
      }

      // Merge default options and dynamically set summary based on severity
      const mergedMessage = {
        ...this.defaultOptions,
        summary: msg.summary || severityDefaults[msg.severity] || '',
        ...msg // Overwrite if summary is explicitly provided
      }

      toast.add(mergedMessage)
    } else {
      console.error('Toast instance not found. Ensure it is initialized.')
    }
  }
}

function getToast() {
  return toastInstance
}

export function setupToast(app, toast) {
  toastInstance = toast
  app.config.globalProperties.$toast = toastService
}
