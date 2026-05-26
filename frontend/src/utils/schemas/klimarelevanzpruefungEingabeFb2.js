import { number, string, object } from 'yup'

// Validation schema
export const schema = object({
  b1q1: number().required('Seite 1, Frage 1'),
  b1q2: number().when('b1q1', {
    is: 1,
    then: (schema) => schema.required('Seite 1, Frage 2'),
    otherwise: (schema) => schema.nullable(true)
  }),
  b1q3: string().when(['b1q1', 'b1q2'], {
    is: (b1q1, b1q2) => b1q1 === 1 && b1q2 === 2,
    then: (schema) => schema.required('Seite 1, Frage 3'),
    otherwise: (schema) => schema.nullable(true)
  }),
  b1q4: number().when('b1q1', {
    is: 1,
    then: (schema) => schema.required('Seite 1, Frage 4'),
    otherwise: (schema) => schema.nullable(true)
  }),
  b1q5: string().when(['b1q1', 'b1q4'], {
    is: (b1q1, b1q4) => b1q1 === 1 && b1q4 === 2,
    then: (schema) => schema.required('Seite 1, Frage 5'),
    otherwise: (schema) => schema.nullable(true)
  }),
  b1q6: number().when('b1q1', {
    is: 1,
    then: (schema) => schema.required('Seite 1, Frage 6'),
    otherwise: (schema) => schema.nullable(true)
  }),
  b1q7: string().when(['b1q1', 'b1q6'], {
    is: (b1q1, b1q6) => b1q1 === 1 && b1q6 === 1,
    then: (schema) => schema.required('Seite 1, Frage 7'),
    otherwise: (schema) => schema.nullable(true)
  }),
  b1q8: string().when(['b1q1', 'b1q6'], {
    is: (b1q1, b1q6) => b1q1 === 1 && b1q6 === 2,
    then: (schema) => schema.required('Seite 1, Frage 8'),
    otherwise: (schema) => schema.nullable(true)
  }),
  b1q9: number().when('b1q1', {
    is: 1,
    then: (schema) => schema.required('Seite 1, Frage 9'),
    otherwise: (schema) => schema.nullable(true)
  }),
  b1q10: string().when(['b1q1', 'b1q9'], {
    is: (b1q1, b1q9) => b1q1 === 1 && b1q9 === 1,
    then: (schema) => schema.required('Seite 1, Frage 10'),
    otherwise: (schema) => schema.nullable(true)
  }),
  b1q11: string().when(['b1q1', 'b1q9'], {
    is: (b1q1, b1q9) => b1q1 === 1 && b1q9 === 2,
    then: (schema) => schema.required('Seite 1, Frage 11'),
    otherwise: (schema) => schema.nullable(true)
  }),
  b1q12: number().when('b1q1', {
    is: 1,
    then: (schema) => schema.required('Seite 1, Frage 12'),
    otherwise: (schema) => schema.nullable(true)
  }),
  b1q13: string().when(['b1q1', 'b1q12'], {
    is: (b1q1, b1q12) => b1q1 === 1 && b1q12 === 1,
    then: (schema) => schema.required('Seite 1, Frage 13'),
    otherwise: (schema) => schema.nullable(true)
  }),
  b1q14: string().when(['b1q1', 'b1q12'], {
    is: (b1q1, b1q12) => b1q1 === 1 && b1q12 === 2,
    then: (schema) => schema.required('Seite 1, Frage 14'),
    otherwise: (schema) => schema.nullable(true)
  }),
  b1q15: number().when('b1q1', {
    is: 1,
    then: (schema) => schema.required('Seite 1, Frage 15'),
    otherwise: (schema) => schema.nullable(true)
  }),
  b1q16: string().when(['b1q1', 'b1q15'], {
    is: (b1q1, b1q15) => b1q1 === 1 && b1q15 === 1,
    then: (schema) => schema.required('Seite 1, Frage 16'),
    otherwise: (schema) => schema.nullable(true)
  }),
  b1q17: string().when(['b1q1', 'b1q15'], {
    is: (b1q1, b1q15) => b1q1 === 1 && b1q15 === 2,
    then: (schema) => schema.required('Seite 1, Frage 17'),
    otherwise: (schema) => schema.nullable(true)
  }),
  b1q18: number().when('b1q1', {
    is: 1,
    then: (schema) => schema.required('Seite 1, Frage 18'),
    otherwise: (schema) => schema.nullable(true)
  }),
  b1q19: string().when(['b1q1', 'b1q18'], {
    is: (b1q1, b1q18) => b1q1 === 1 && b1q18 === 1,
    then: (schema) => schema.required('Seite 1, Frage 19'),
    otherwise: (schema) => schema.nullable(true)
  }),
  b1q20: string().when(['b1q1', 'b1q18'], {
    is: (b1q1, b1q18) => b1q1 === 1 && b1q18 === 2,
    then: (schema) => schema.required('Seite 1, Frage 20'),
    otherwise: (schema) => schema.nullable(true)
  }),
  b2q1: number().required('Seite 2, Frage 1'),
  b2q2: string().when('b2q1', {
    is: 1,
    then: (schema) => schema.required('Seite 2, Frage 2'),
    otherwise: (schema) => schema.nullable(true)
  }),
  b2q3: string().when('b2q1', {
    is: 1,
    then: (schema) => schema.required('Seite 2, Frage 3'),
    otherwise: (schema) => schema.nullable(true)
  }),
  b2q4: number().when('b2q1', {
    is: 1,
    then: (schema) => schema.required('Seite 2, Frage 4'),
    otherwise: (schema) => schema.nullable(true)
  }),
  b2q5: string().when(['b2q1', 'b2q4'], {
    is: (b2q1, b2q4) => b2q1 === 1 && b2q4 === 1,
    then: (schema) => schema.required('Seite 2, Frage 5'),
    otherwise: (schema) => schema.nullable(true)
  })
})
