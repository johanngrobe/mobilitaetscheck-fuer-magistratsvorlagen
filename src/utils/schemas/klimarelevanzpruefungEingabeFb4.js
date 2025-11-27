import { string, object } from 'yup'

// Validation schema
export const schema = object({
  d1q1: string().required('Das ist ein Pflichtfeld'),
  d2q1: string().required('Das ist ein Pflichtfeld')
})
