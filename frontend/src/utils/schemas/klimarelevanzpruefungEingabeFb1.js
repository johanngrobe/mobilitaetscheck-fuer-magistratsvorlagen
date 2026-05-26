import { number, string, object } from 'yup'

// Validation schema
export const schema = object({
  a1q1: number().required('Seite 1, Frage 1'),
  a1q2: string().when('a1q1', {
    is: 1,
    then: (schema) => schema.required('Seite 1, Frage 2'),
    otherwise: (schema) => schema.nullable(true)
  }),
  a1q3: number().when('a1q1', {
    is: 1,
    then: (schema) => schema.required('Seite 1, Frage 3'),
    otherwise: (schema) => schema.nullable(true)
  }),
  a1q4: string().when(['a1q1', 'a1q3'], {
    is: (a1q1, a1q3) => a1q1 === 1 && a1q3 === 1,
    then: (schema) => schema.required('Seite 1, Frage 4'),
    otherwise: (schema) => schema.nullable(true)
  }),
  a1q5: string().when(['a1q1', 'a1q3'], {
    is: (a1q1, a1q3) => a1q1 === 1 && a1q3 === 2,
    then: (schema) => schema.required('Seite 1, Frage 4'),
    otherwise: (schema) => schema.nullable(true)
  }),
  a2q1: number().required('Seite 2, Frage 1'),
  a2q2: number().when('a2q1', {
    is: 1,
    then: (schema) =>
      schema.required('Seite 2, Frage 2').min(0, 'Seite 2, Frage 2: Muss mindestens 0 sein'),
    otherwise: (schema) => schema.nullable(true)
  }),
  a2q3: number().when(['a2q1', 'a2q2'], {
    is: (a2q1, a2q2) => a2q1 === 1 && [3, 4].includes(a2q2),
    then: (schema) => schema.required('Seite 2, Frage 3'),
    otherwise: (schema) => schema.nullable(true)
  }),
  a2q4: number().when(['a2q1', 'a2q2', 'a2q3'], {
    is: (a2q1, a2q2, a2q3) => a2q1 === 1 && [3, 4].includes(a2q2) && a2q3 === 1,
    then: (schema) => schema.required('Seite 2, Frage 4'),
    otherwise: (schema) => schema.nullable(true)
  }),
  a2q5: string().when(['a2q1', 'a2q2', 'a2q3', 'a2q4'], {
    is: (a2q1, a2q2, a2q3, a2q4) =>
      a2q1 === 1 && [3, 4].includes(a2q2) && a2q3 === 1 && typeof a2q4 === 'number',
    then: (schema) => schema.required('Seite 2, Frage 5'),
    otherwise: (schema) => schema.nullable(true)
  }),
  a2q6: number().when(['a2q1', 'a2q2'], {
    is: (a2q1, a2q2) => a2q1 === 1 && [1, 2].includes(a2q2),
    then: (schema) => schema.required('Seite 2, Frage 3'),
    otherwise: (schema) => schema.nullable(true)
  }),
  a2q7: string().when(['a2q1', 'a2q2', 'a2q6'], {
    is: (a2q1, a2q2, a2q6) => a2q1 === 1 && [1, 2].includes(a2q2) && typeof a2q6 === 'number',
    then: (schema) => schema.required('Seite 2, Frage 4'),
    otherwise: (schema) => schema.nullable(true)
  }),
  a2q8: number().when('a2q1', {
    is: 1,
    then: (schema) => schema.required('Seite 2, Frage 5'),
    otherwise: (schema) => schema.nullable(true)
  }),
  a2q9: string().when(['a2q1', 'a2q8'], {
    is: (a2q1, a2q8) => a2q1 === 1 && a2q8 === 2,
    then: (schema) => schema.required('Seite 2, Frage 6'),
    otherwise: (schema) => schema.nullable(true)
  }),
  a2q10: number().when('a2q1', {
    is: 1,
    then: (schema) => schema.required('Seite 2, Frage 7'),
    otherwise: (schema) => schema.nullable(true)
  }),
  a2q11: string().when(['a2q1', 'a2q10'], {
    is: (a2q1, a2q10) => a2q1 === 1 && a2q10 === 2,
    then: (schema) => schema.required('Seite 2, Frage 8'),
    otherwise: (schema) => schema.nullable(true)
  }),
  a2q12: number().when('a2q1', {
    is: 1,
    then: (schema) => schema.required('Seite 2, Frage 9'),
    otherwise: (schema) => schema.nullable(true)
  }),
  a2q13: string().when(['a2q1', 'a2q12'], {
    is: (a2q1, a2q12) => a2q1 === 1 && a2q12 === 2,
    then: (schema) => schema.required('Seite 2, Frage 10'),
    otherwise: (schema) => schema.nullable(true)
  }),
  a2q14: number().when('a2q1', {
    is: 1,
    then: (schema) => schema.required('Seite 2, Frage 11'),
    otherwise: (schema) => schema.nullable(true)
  }),
  a2q15: string().when(['a2q1', 'a2q14'], {
    is: (a2q1, a2q14) => a2q1 === 1 && a2q14 === 2,
    then: (schema) => schema.required('Seite 2, Frage 12'),
    otherwise: (schema) => schema.nullable(true)
  }),
  a3q1: number().required('Seite 3, Frage 1'),
  a3q2: number().when('a3q1', {
    is: 1,
    then: (schema) =>
      schema.required('Seite 3, Frage 2').min(0, 'Seite 3, Frage 2: Muss mindestens 0 sein'),
    otherwise: (schema) => schema.nullable(true)
  }),
  a3q3: string().when('a3q1', {
    is: 1,
    then: (schema) => schema.required('Seite 3, Frage 3'),
    otherwise: (schema) => schema.nullable(true)
  }),
  a3q4: number().when('a3q1', {
    is: 1,
    then: (schema) => schema.required('Seite 3, Frage 4'),
    otherwise: (schema) => schema.nullable(true)
  }),
  a3q5: string().when(['a3q1', 'a3q4'], {
    is: (a3q1, a3q4) => a3q1 === 1 && a3q4 === 1,
    then: (schema) => schema.required('Seite 3, Frage 5'),
    otherwise: (schema) => schema.nullable(true)
  }),
  a3q6: string().when(['a3q1', 'a3q4'], {
    is: (a3q1, a3q4) => a3q1 === 1 && a3q4 === 2,
    then: (schema) => schema.required('Seite 3, Frage 5'),
    otherwise: (schema) => schema.nullable(true)
  }),
  a4q1: number().required('Seite 4, Frage 1'),
  a4q2: number().when('a4q1', {
    is: 1,
    then: (schema) =>
      schema.required('Seite 4, Frage 2').min(0, 'Seite 4, Frage 2: Muss mindestens 0 sein'),
    otherwise: (schema) => schema.nullable(true)
  }),
  a4q3: string().when('a4q1', {
    is: 1,
    then: (schema) => schema.required('Seite 4, Frage 3'),
    otherwise: (schema) => schema.nullable(true)
  }),
  a4q4: number().when(['a4q1', 'a4q3'], {
    is: (a4q1, a4q3) => a4q1 === 1 && !!a4q3,
    then: (schema) => schema.required('Seite 4, Frage 4'),
    otherwise: (schema) => schema.nullable(true)
  }),
  a5q1: number().required('Seite 5, Frage 1'),
  a5q2: number().when('a5q1', {
    is: 1,
    then: (schema) =>
      schema.required('Seite 5, Frage 2').min(0, 'Seite 5, Frage 2: Muss mindestens 0 sein'),
    otherwise: (schema) => schema.nullable(true)
  }),
  a5q3: string().when('a5q1', {
    is: 1,
    then: (schema) => schema.required('Seite 5, Frage 3'),
    otherwise: (schema) => schema.nullable(true)
  }),
  a5q5: string().when('a5q1', {
    is: 1,
    then: (schema) => schema.required('Seite 5, Frage 4'),
    otherwise: (schema) => schema.nullable(true)
  }),
  a5q4: number().when('a5q1', {
    is: 1,
    then: (schema) => schema.required('Seite 5, Frage 5'),
    otherwise: (schema) => schema.nullable(true)
  }),
  a6q1: number().required('Seite 6, Frage 1'),
  a6q2: string().when('a6q1', {
    is: 1,
    then: (schema) => schema.required('Seite 6, Frage 2'),
    otherwise: (schema) => schema.nullable(true)
  }),
  a6q3: number().when('a6q1', {
    is: 1,
    then: (schema) => schema.required('Seite 6, Frage 3'),
    otherwise: (schema) => schema.nullable(true)
  }),
  a6q4: string().when(['a6q1', 'a6q3'], {
    is: (a6q1, a6q3) => a6q1 === 1 && a6q3 === 1,
    then: (schema) => schema.required('Seite 6, Frage 4'),
    otherwise: (schema) => schema.nullable(true)
  }),
  a6q5: string().when(['a6q1', 'a6q3'], {
    is: (a6q1, a6q3) => a6q1 === 1 && a6q3 === 2,
    then: (schema) => schema.required('Seite 6, Frage 4'),
    otherwise: (schema) => schema.nullable(true)
  }),
  a7q1: number().required('Seite 7, Frage 1'),
  a7q2: string().when('a7q1', {
    is: 1,
    then: (schema) => schema.required('Seite 7, Frage 2'),
    otherwise: (schema) => schema.nullable(true)
  }),
  a8q1: number().required('Seite 8, Frage 1'),
  a8q2: string().when('a8q1', {
    is: 1,
    then: (schema) => schema.required('Seite 8, Frage 2'),
    otherwise: (schema) => schema.nullable(true)
  })
})
