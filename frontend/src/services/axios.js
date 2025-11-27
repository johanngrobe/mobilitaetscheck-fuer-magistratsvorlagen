import axios from 'axios'
import applyCaseMiddleware from 'axios-case-converter'
import axiosRetry from 'axios-retry'
import { API_BASE_URL } from '@/utils/config'

axiosRetry(axios, {
  retries: 3, // Retry up to 3 times
  retryCondition: (error) => {
    // Retry only if the error is due to a network issue or 5xx status code
    return axiosRetry.isNetworkOrIdempotentRequestError(error) || error.response?.status >= 500
  },
  retryDelay: (retryCount) => {
    console.log(`Retry attempt #${retryCount}`)
    return retryCount * 1000 // Delay between retries
  }
})

export const apiClient = applyCaseMiddleware(
  axios.create({
    baseURL: API_BASE_URL,
    headers: {
      'Content-Type': 'application/json'
    },
    withCredentials: true
  })
)

// Add global response interceptor
apiClient.interceptors.response.use(
  (response) => response, // Pass successful responses through
  (error) => {
    let errorMessage = 'An unexpected error occurred.' // Default error message

    if (error.response) {
      // Handle HTTP response errors
      const status = error.response.status
      switch (status) {
        case 400:
          errorMessage = 'Bad Request. Please check your input.'
          break
        case 401:
          errorMessage = 'Unauthorized. Please log in again.'
          break
        case 404:
          return Promise.resolve({ data: [] }) // Handle 404 by returning an empty list
        case 500:
          errorMessage = 'Server error. Please try again later.'
          break
        default:
          errorMessage = 'An unexpected error occurred.'
      }
    } else if (error.request) {
      // Handle network errors (no response received)
      errorMessage = 'Network error. Please check your internet connection.'
    } else {
      // Handle unexpected errors (e.g., request setup issues)
      errorMessage = error.message || 'An unexpected error occurred.'
    }

    // Log the error message
    console.error(`Error: ${errorMessage}`)

    // Attach the error message to the error object and reject it
    error.message = errorMessage
    return Promise.reject(error)
  }
)
