import * as yup from 'yup'

// Validation schema
export const schema = yup.object({
  name: yup.string().required('Angabe ist erforderlich')
})
