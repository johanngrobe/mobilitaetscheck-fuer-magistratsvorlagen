import * as yup from 'yup'

// Validation schema
export const schema = yup.object({
  nr: yup.number().required('Angabe ist erforderlich'),
  name: yup.string().required('Angabe ist erforderlich'),
  zielOberId: yup.number().required('Angabe ist erforderlich')
})
