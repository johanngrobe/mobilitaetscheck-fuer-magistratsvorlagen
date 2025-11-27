import * as yup from 'yup'

// Validation schema
export const schema = yup.object({
  // author: yup.string().required('Angabe ist erforderlich'),
  nr: yup.number().required('Angabe ist erforderlich'),
  name: yup.string().required('Angabe ist erforderlich')
})
