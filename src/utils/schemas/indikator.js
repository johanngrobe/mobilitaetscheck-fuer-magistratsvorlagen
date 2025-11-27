import * as yup from 'yup'

// Validation schema
export const schema = yup.object({
  name: yup.string().required('Angabe ist erforderlich'),
  quelleUrl: yup.string().url('Ungültige URL').nullable(true),
  tagIds: yup.array().of(yup.number()).nullable(true),
  gemeindespezifisch: yup.boolean().default(false)
})
