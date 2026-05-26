import { number, string, object } from 'yup'

// Validation schema
export const schema = object({
  c1q1: number().required('Seite 1, Frage 1'),
  c1q2: number().when('c1q1', {
    is: 1,
    then: (schema) => schema.required('Seite 1, Frage 2'),
    otherwise: (schema) => schema.nullable(true)
  }),
  c1q3: string().when(['c1q1', 'c1q2'], {
    is: (c1q1, c1q2) => c1q1 === 1 && c1q2 === 1,
    then: (schema) => schema.required('Seite 1, Frage 3'),
    otherwise: (schema) => schema.nullable(true)
  }),
  c1q4: number().when('c1q1', {
    is: 1,
    then: (schema) => schema.required('Seite 1, Frage 4'),
    otherwise: (schema) => schema.nullable(true)
  }),
  c1q5: string().when(['c1q1', 'c1q4'], {
    is: (c1q1, c1q4) => c1q1 === 1 && c1q4 === 1,
    then: (schema) => schema.required('Seite 1, Frage 5'),
    otherwise: (schema) => schema.nullable(true)
  }),
  c1q6: number().when('c1q1', {
    is: 1,
    then: (schema) => schema.required('Seite 1, Frage 6'),
    otherwise: (schema) => schema.nullable(true)
  }),
  c1q7: string().when(['c1q1', 'c1q6'], {
    is: (c1q1, c1q6) => c1q1 === 1 && c1q6 === 1,
    then: (schema) => schema.required('Seite 1, Frage 7'),
    otherwise: (schema) => schema.nullable(true)
  }),
  c1q8: number().when('c1q1', {
    is: 1,
    then: (schema) => schema.required('Seite 1, Frage 8'),
    otherwise: (schema) => schema.nullable(true)
  }),
  c1q9: string().when(['c1q1', 'c1q8'], {
    is: (c1q1, c1q8) => c1q1 === 1 && c1q8 === 1,
    then: (schema) => schema.required('Seite 1, Frage 9'),
    otherwise: (schema) => schema.nullable(true)
  }),
  c2q1: number().required('Seite 2, Frage 1'),
  c2q2: number().when('c2q1', {
    is: 1,
    then: (schema) => schema.required('Seite 2, Frage 2'),
    otherwise: (schema) => schema.nullable(true)
  }),
  c2q3: string().when(['c2q1', 'c2q2'], {
    is: (c2q1, c2q2) => c2q1 === 1 && c2q2 === 1,
    then: (schema) => schema.required('Seite 2, Frage 3'),
    otherwise: (schema) => schema.nullable(true)
  }),
  c2q4: number().when('c2q1', {
    is: 1,
    then: (schema) => schema.required('Seite 2, Frage 4'),
    otherwise: (schema) => schema.nullable(true)
  }),
  c2q5: string().when(['c2q1', 'c2q4'], {
    is: (c2q1, c2q4) => c2q1 === 1 && c2q4 === 1,
    then: (schema) => schema.required('Seite 2, Frage 5'),
    otherwise: (schema) => schema.nullable(true)
  }),
  c2q6: number().when('c2q1', {
    is: 1,
    then: (schema) => schema.required('Seite 2, Frage 6'),
    otherwise: (schema) => schema.nullable(true)
  }),
  c2q7: string().when(['c2q1', 'c2q6'], {
    is: (c2q1, c2q6) => c2q1 === 1 && c2q6 === 1,
    then: (schema) => schema.required('Seite 2, Frage 7'),
    otherwise: (schema) => schema.nullable(true)
  }),
  c2q8: number().when('c2q1', {
    is: 1,
    then: (schema) => schema.required('Seite 2, Frage 8'),
    otherwise: (schema) => schema.nullable(true)
  }),
  c2q9: string().when(['c2q1', 'c2q8'], {
    is: (c2q1, c2q8) => c2q1 === 1 && c2q8 === 1,
    then: (schema) => schema.required('Seite 2, Frage 9'),
    otherwise: (schema) => schema.nullable(true)
  })
})
