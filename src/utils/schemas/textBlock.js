import * as yup from 'yup'

// Validation schema
export const schema = yup.object({
  name: yup.string().required('Angabe ist erforderlich'),
  tagIds: yup.array().of(yup.number()).nullable(true),
  gemeindespezifisch: yup.boolean().default(false)
})
