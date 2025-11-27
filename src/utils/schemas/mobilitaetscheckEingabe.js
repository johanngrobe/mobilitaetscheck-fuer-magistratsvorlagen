import { object, string } from 'yup'

// Validation schema
export const schema = object({
  name: string().required('Angabe ist erforderlich')
})
