import { boolean, string, object } from 'yup'

// Validation schema
export const schema = object({
  name: string().required('Name ist erforderlich').label('Name'),
  f1: boolean().nullable(true),
  f2: boolean().nullable(true),
  f3: boolean().nullable(true),
  f4: boolean().nullable(true),
  f5: boolean()
    .nullable(true)
    .test('at-least-one-true', 'Mindestens ein Feld muss ausgewählt werden', function () {
      const { f1, f2, f3, f4, f5 } = this.parent
      return [f1, f2, f3, f4, f5].some((v) => v === true)
    })
})
