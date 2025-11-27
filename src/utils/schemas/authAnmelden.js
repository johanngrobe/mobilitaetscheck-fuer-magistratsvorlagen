import { object, string } from 'yup'

export const schema = object({
  email: string()
    .required('E-Mail ist erforderlich')
    .email('Ungültige E-Mail-Adresse')
    .label('E-Mail'),
  password: string()
    .required('Passwort ist erforderlich')
    .min(6, 'Passwort muss mindestens 6 Zeichen lang sein')
    .label('Passwort')
})
