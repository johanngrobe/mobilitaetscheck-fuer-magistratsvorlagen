import { number, string, object } from 'yup'

// Validation schema
export const schema = object({
  a1q1: number().required('Das ist ein Pflichtfeld'),
  a1q2: string().when('a1q1', {
    is: 1,
    then: (schema) => schema.required('Das ist ein Pflichtfeld'),
    otherwise: (schema) => schema.nullable(true)
  }),
  a1q3: number().when('a1q1', {
    is: 1,
    then: (schema) => schema.required('Das ist ein Pflichtfeld'),
    otherwise: (schema) => schema.nullable(true)
  }),
  a1q4: string().when('a1q3', {
    is: 1,
    then: (schema) => schema.required('Das ist ein Pflichtfeld'),
    otherwise: (schema) => schema.nullable(true)
  }),
  a1q5: string().when('a1q3', {
    is: 2,
    then: (schema) => schema.required('Das ist ein Pflichtfeld'),
    otherwise: (schema) => schema.nullable(true)
  }),
  a2q1: number().required('Das ist ein Pflichtfeld'),
  a2q2: number().when('a2q1', {
    is: 1,
    then: (schema) => schema.required('Das ist ein Pflichtfeld').min(0, 'Muss mindestens 0 sein'),
    otherwise: (schema) => schema.nullable(true)
  }),
  a2q3: number().when('a2q2', {
    is: (val) => [3, 4].includes(val),
    then: (schema) => schema.required('Das ist ein Pflichtfeld'),
    otherwise: (schema) => schema.nullable(true)
  }),
  a2q4: number().when('a2q3', {
    is: 1,
    then: (schema) => schema.required('Das ist ein Pflichtfeld'),
    otherwise: (schema) => schema.nullable(true)
  }),
  a2q5: string().when('a2q4', {
    is: (val) => typeof val === 'number',
    then: (schema) => schema.required('Das ist ein Pflichtfeld'),
    otherwise: (schema) => schema.nullable(true)
  }),
  a2q6: number().when('a2q2', {
    is: (val) => [1, 2].includes(val),
    then: (schema) => schema.required('Das ist ein Pflichtfeld'),
    otherwise: (schema) => schema.nullable(true)
  }),
  a2q7: string().when('a2q6', {
    is: (val) => typeof val === 'number',
    then: (schema) => schema.required('Das ist ein Pflichtfeld'),
    otherwise: (schema) => schema.nullable(true)
  }),
  a2q8: number().when('a2q2', {
    is: 1,
    then: (schema) => schema.required('Das ist ein Pflichtfeld'),
    otherwise: (schema) => schema.nullable(true)
  }),
  a2q9: string().when('a2q8', {
    is: 2,
    then: (schema) => schema.required('Das ist ein Pflichtfeld'),
    otherwise: (schema) => schema.nullable(true)
  }),
  a2q10: number().when('a2q2', {
    is: 1,
    then: (schema) => schema.required('Das ist ein Pflichtfeld'),
    otherwise: (schema) => schema.nullable(true)
  }),
  a2q11: number().when('a2q10', {
    is: 2,
    then: (schema) => schema.required('Das ist ein Pflichtfeld'),
    otherwise: (schema) => schema.nullable(true)
  }),
  a2q12: string().when('a2q2', {
    is: 1,
    then: (schema) => schema.required('Das ist ein Pflichtfeld'),
    otherwise: (schema) => schema.nullable(true)
  }),
  a2q13: string().when('a2q12', {
    is: 2,
    then: (schema) => schema.required('Das ist ein Pflichtfeld'),
    otherwise: (schema) => schema.nullable(true)
  }),
  a2q14: number().when('a2q2', {
    is: 1,
    then: (schema) => schema.required('Das ist ein Pflichtfeld'),
    otherwise: (schema) => schema.nullable(true)
  }),
  a2q15: string().when('a2q14', {
    is: 2,
    then: (schema) => schema.required('Das ist ein Pflichtfeld'),
    otherwise: (schema) => schema.nullable(true)
  }),
  a3q1: number().required('Das ist ein Pflichtfeld'),
  a3q2: number().when('a3q1', {
    is: 1,
    then: (schema) => schema.required('Das ist ein Pflichtfeld').min(0, 'Muss mindestens 0 sein'),
    otherwise: (schema) => schema.nullable(true)
  }),
  a3q3: string().when('a3q1', {
    is: 1,
    then: (schema) => schema.required('Das ist ein Pflichtfeld'),
    otherwise: (schema) => schema.nullable(true)
  }),
  a3q4: number().when('a3q1', {
    is: 1,
    then: (schema) => schema.required('Das ist ein Pflichtfeld'),
    otherwise: (schema) => schema.nullable(true)
  }),
  a3q5: string().when('a3q4', {
    is: 1,
    then: (schema) => schema.required('Das ist ein Pflichtfeld'),
    otherwise: (schema) => schema.nullable(true)
  }),
  a3q6: string().when('a3q4', {
    is: 2,
    then: (schema) => schema.required('Das ist ein Pflichtfeld'),
    otherwise: (schema) => schema.nullable(true)
  }),
  a4q1: number().required('Das ist ein Pflichtfeld'),
  a4q2: number().when('a4q1', {
    is: 1,
    then: (schema) => schema.required('Das ist ein Pflichtfeld').min(0, 'Muss mindestens 0 sein'),
    otherwise: (schema) => schema.nullable(true)
  }),
  a4q3: string().when('a4q1', {
    is: 1,
    then: (schema) => schema.required('Das ist ein Pflichtfeld'),
    otherwise: (schema) => schema.nullable(true)
  }),
  a4q4: number().when('a4q3', {
    is: (val) => !!val,
    then: (schema) => schema.required('Das ist ein Pflichtfeld'),
    otherwise: (schema) => schema.nullable(true)
  }),
  a5q1: number().required('Das ist ein Pflichtfeld'),
  a5q2: string().when('a5q1', {
    is: 1,
    then: (schema) => schema.required('Das ist ein Pflichtfeld'),
    otherwise: (schema) => schema.nullable(true)
  }),
  a5q3: string().when('a5q1', {
    is: 1,
    then: (schema) => schema.required('Das ist ein Pflichtfeld'),
    otherwise: (schema) => schema.nullable(true)
  }),
  a5q4: number().when('a5q1', {
    is: 1,
    then: (schema) => schema.required('Das ist ein Pflichtfeld'),
    otherwise: (schema) => schema.nullable(true)
  }),
  a6q1: number().required('Das ist ein Pflichtfeld'),
  a6q2: string().when('a6q1', {
    is: 1,
    then: (schema) => schema.required('Das ist ein Pflichtfeld'),
    otherwise: (schema) => schema.nullable(true)
  }),
  a6q3: number().when('a6q1', {
    is: 1,
    then: (schema) => schema.required('Das ist ein Pflichtfeld'),
    otherwise: (schema) => schema.nullable(true)
  }),
  a6q4: string().when('a6q3', {
    is: 1,
    then: (schema) => schema.required('Das ist ein Pflichtfeld'),
    otherwise: (schema) => schema.nullable(true)
  }),
  a6q5: string().when('a6q3', {
    is: 2,
    then: (schema) => schema.required('Das ist ein Pflichtfeld'),
    otherwise: (schema) => schema.nullable(true)
  }),
  a7q1: number().required('Das ist ein Pflichtfeld'),
  a7q2: string().when('a7q1', {
    is: 1,
    then: (schema) => schema.required('Das ist ein Pflichtfeld'),
    otherwise: (schema) => schema.nullable(true)
  }),
  a8q1: number().required('Das ist ein Pflichtfeld'),
  a8q2: string().when('a8q1', {
    is: 1,
    then: (schema) => schema.required('Das ist ein Pflichtfeld'),
    otherwise: (schema) => schema.nullable(true)
  })
})
