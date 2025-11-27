import { object, string, number } from 'yup'

// Validation schema
export const schema = object({
  name: string().required('Angabe ist erforderlich'),
  klimarelevanzId: number().required('Angabe ist erforderlich'),
  auswirkungThg: number().when('klimarelevanzId', {
    is: 3,
    then: (schema) => schema.optional().nullable(true).oneOf([null, '']),
    otherwise: (schema) =>
      schema
        .integer('ImpactGhg muss eine ganze Zahl sein')
        .notOneOf([0], 'ImpactGhg darf nicht 0 sein')
        .min(-2, 'ImpactGhg muss zwischen -2 und 2 liegen')
        .max(2, 'ImpactGhg muss zwischen -2 und 2 liegen')
        .required('Bitte ausfüllen, wenn es klimarelevant ist')
  }),
  auswirkungKlimaanpassung: number().when('klimarelevanzId', {
    is: 3,
    then: (schema) => schema.optional().nullable(true).oneOf([null, '']),
    otherwise: (schema) =>
      schema
        .integer('ImpactAdaption muss eine ganze Zahl sein')
        .notOneOf([0], 'ImpactAdaption darf nicht 0 sein')
        .min(-2, 'ImpactAdaption muss zwischen -2 und 2 liegen')
        .max(2, 'ImpactAdaption muss zwischen -2 und 2 liegen')
        .required('Bitte ausfüllen, wenn es klimarelevant ist')
  }),
  auswirkungBeschreibung: string().when('klimarelevanzId', {
    is: 3,
    then: (schema) => schema.optional().nullable(true).oneOf([null, '']),
    otherwise: (schema) => schema.required('Bitte ausfüllen, wenn es klimarelevant ist')
  }),
  auswirkungDauerId: number().when('klimarelevanzId', {
    is: 3,
    then: (schema) => schema.optional().nullable(true).oneOf([null, '']),
    otherwise: (schema) => schema.required('Bitte ausfüllen, wenn es klimarelevant ist')
  }),
  alternativen: string().when('klimarelevanzId', {
    is: 3,
    then: (schema) => schema.optional().nullable(true).oneOf([null, '']),
    otherwise: (schema) => schema.required('Bitte ausfüllen, wenn es klimarelevant ist')
  })
})
