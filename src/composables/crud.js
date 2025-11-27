import { apiClient } from '@/services/axios'
import { toastService } from '@/services/toast'
import { toSnakeCase } from '@/composables/caseConvert'

export const fetchAutocomplete = async (event, model, field) => {
  const response = await apiClient.get(`/${model}/autocomplete`, {
    params: {
      field: toSnakeCase(field),
      query: event.query
    }
  })
  return response.data
}

export const fetchItem = async (api, query = {}) => {
  const response = await apiClient.get(api, { params: query })
  if (response.status === 204) {
    return null
  }
  return response.data
}

export const fetchItems = async (api, query = {}) => {
  const response = await apiClient.get(api, { params: query })
  if (response.status === 204) {
    return []
  }
  return response.data
}

export const createItem = async ({ model, values, detail }) => {
  try {
    const response = await apiClient.post(`/${model}`, values)
    toastService.add({
      severity: 'success',
      detail: detail.success
    })
    return response.data
  } catch (error) {
    toastService.add({
      severity: 'error',
      detail: detail.error
    })
  }
}

export const createItemSilent = async ({ model, values }) => {
  try {
    const response = await apiClient.post(`/${model}`, values)
    return response.data
  } catch (error) {
    console.error(error)
  }
}

export const copyItem = async ({ model, modelId, detail }) => {
  try {
    const response = await apiClient.post(`/${model}/eingabe/duplizieren/${modelId}`)
    toastService.add({
      severity: 'success',
      detail: detail.success
    })
    return response.data
  } catch (error) {
    toastService.add({
      severity: 'error',
      detail: detail.error
    })
  }
}

export const updateItem = async ({ model, modelId, values, detail }) => {
  try {
    const response = await apiClient.patch(`/${model}/${modelId}`, values)
    toastService.add({
      severity: 'success',
      detail: detail.success
    })
    return response.data
  } catch (error) {
    toastService.add({
      severity: 'error',
      detail: detail.error
    })
  }
}

export const updateItemSilent = async ({ model, modelId, values }) => {
  try {
    const response = await apiClient.patch(`/${model}/${modelId}`, values)
    return response.data
  } catch (error) {
    console.error(error)
  }
}

export const deleteItem = async ({ model, modelId, detail }) => {
  try {
    const response = await apiClient.delete(`/${model}/${modelId}`)
    toastService.add({
      severity: 'success',
      detail: detail.success
    })
    return response.data
  } catch (error) {
    toastService.add({
      severity: 'error',
      detail: detail.error
    })
  }
}

export const exportItem = async ({ model, modelId, detail }) => {
  try {
    const response = await apiClient.get(`/${model}/eingabe/export/${modelId}`, {
      responseType: 'blob'
    })
    // Create a download link for the received Blob
    const url = window.URL.createObjectURL(new Blob([response.data], { type: 'application/pdf' }))
    const link = document.createElement('a')
    link.href = url
    let fileName
    if (model === 'mobilitaetscheck') {
      fileName = `mobilitätscheck_${modelId}.pdf`
    } else if (model === 'klimacheck') {
      fileName = `klimacheck_${modelId}.pdf`
    } else {
      fileName = `export_${modelId}.pdf`
    }
    link.setAttribute('download', fileName) // The file name
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)

    toastService.add({
      severity: 'success',
      detail: detail.success
    })
  } catch (error) {
    toastService.add({
      severity: 'error',
      detail: detail.error
    })
  }
}
