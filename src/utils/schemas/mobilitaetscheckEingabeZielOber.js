import * as yup from 'yup'

// Validation schema
export const schema = yup.object({
  eingabeId: yup.number().required('Angabe ist erforderlich'),
  zielOberId: yup.number().required('Angabe ist erforderlich'),
  tangiert: yup.boolean().default(false)
})
