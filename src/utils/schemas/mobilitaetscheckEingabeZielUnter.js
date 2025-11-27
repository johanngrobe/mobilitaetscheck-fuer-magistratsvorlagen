import * as yup from 'yup'

// Validation schema
export const schema = yup.object({
  eingabeZielOberId: yup.number().required('Angabe ist erforderlich'),
  zielUnterId: yup.number().required('Angabe ist erforderlich'),
  tangiert: yup.boolean().default(false),
  auswirkung: yup
    .number()
    .min(-3)
    .max(3)
    .when('tangiert', {
      is: true,
      then: (schema) => schema.required('Angabe ist erforderlich'),
      otherwise: (schema) => schema.nullable(true)
    }),
  auswirkungRaeumlichId: yup.number().nullable(true),
  // .when('tangiert', {
  //   is: true,
  //   then: (schema) => schema.required('Angabe ist erforderlich'),
  //   otherwise: (schema) => schema.nullable(true)
  // }),
  anmerkung: yup.string().nullable(true),
  indikatorIds: yup.array().of(yup.number()).nullable(true)
})
