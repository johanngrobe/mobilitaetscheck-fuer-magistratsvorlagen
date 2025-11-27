import { number, string, object } from 'yup'

// Validation schema
export const schema = object({
  c1q1: number().required('Das ist ein Pflichtfeld'),
  c1q2: number().when('c1q1', {
    is: 1,
    then: number().required('Das ist ein Pflichtfeld'),
    otherwise: number().nullable(true)
  }),
  c1q3: string().when('c1q2', {
    is: 1,
    then: (schema) => schema.required('Das ist ein Pflichtfeld'),
    otherwise: string().nullable(true)
  }),
  c1q4: number().when('c1q1', {
    is: 1,
    then: number().required('Das ist ein Pflichtfeld'),
    otherwise: number().nullable(true)
  }),
  c1q5: string().when('c1q4', {
    is: 1,
    then: (schema) => schema.required('Das ist ein Pflichtfeld'),
    otherwise: string().nullable(true)
  }),
  c1q6: number().when('c1q1', {
    is: 1,
    then: number().required('Das ist ein Pflichtfeld'),
    otherwise: number().nullable(true)
  }),
  c1q7: string().when('c1q6', {
    is: 1,
    then: (schema) => schema.required('Das ist ein Pflichtfeld'),
    otherwise: string().nullable(true)
  }),
  c1q8: number().when('c1q1', {
    is: 1,
    then: number().required('Das ist ein Pflichtfeld'),
    otherwise: number().nullable(true)
  }),
  c1q9: string().when('c1q8', {
    is: 1,
    then: (schema) => schema.required('Das ist ein Pflichtfeld'),
    otherwise: string().nullable(true)
  }),
  c2q1: number().required('Das ist ein Pflichtfeld'),
  c2q2: number().when('c2q1', {
    is: 1,
    then: number()
      .required('Das ist ein Pflichtfeld')

      .min(0, 'Muss mindestens 0 sein'),
    otherwise: number().nullable(true)
  }),
  c2q3: string().when('c2q2', {
    is: 1,
    then: (schema) => schema.required('Das ist ein Pflichtfeld'),
    otherwise: string().nullable(true)
  }),
  c2q4: number().when('c2q1', {
    is: 1,
    then: number().required('Das ist ein Pflichtfeld'),
    otherwise: number().nullable(true)
  }),
  c2q5: string().when('c2q4', {
    is: 1,
    then: (schema) => schema.required('Das ist ein Pflichtfeld'),
    otherwise: string().nullable(true)
  }),
  c2q6: number().when('c2q1', {
    is: 1,
    then: number().required('Das ist ein Pflichtfeld'),
    otherwise: number().nullable(true)
  }),
  c2q7: string().when('c2q6', {
    is: 1,
    then: (schema) => schema.required('Das ist ein Pflichtfeld'),
    otherwise: string().nullable(true)
  }),
  c2q8: number().when('c2q1', {
    is: 1,
    then: number().required('Das ist ein Pflichtfeld'),
    otherwise: number().nullable(true)
  }),
  c2q9: string().when('c2q8', {
    is: 1,
    then: (schema) => schema.required('Das ist ein Pflichtfeld'),
    otherwise: string().nullable(true)
  })
})
