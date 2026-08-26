import * as yup from 'yup'
import YupPassword from 'yup-password'
YupPassword(yup)

export const schema = yup.object({
  vorname: yup.string().required('Vorname ist erforderlich').label('Vorname'),
  nachname: yup.string().required('Nachname ist erforderlich').label('Nachname'),
  password: yup
    .string()
    .min(8, 'Passwort muss mindestens 8 Zeichen lang sein')
    .minLowercase(1, 'Passwort muss mindestens 1 Kleinbuchstaben enthalten')
    .minUppercase(1, 'Passwort muss mindestens 1 Großbuchstaben enthalten')
    .minNumbers(1, 'Passwort muss mindestens 1 Zahl enthalten')
    .minSymbols(1, 'Passwort muss mindestens 1 Sonderzeichen enthalten')
    .required('Passwort ist erforderlich')
    .label('Passwort'),
  confirmPassword: yup
    .string()
    .oneOf([yup.ref('password')], 'Passwörter müssen übereinstimmen')
    .required('Passwortwiederholung ist erforderlich')
    .label('Passwort wiederholen'),
  datenschutzAkzeptiert: yup
    .boolean()
    .oneOf([true], 'Bitte stimmen Sie der Datenschutzerklärung zu.')
    .required('Bitte stimmen Sie der Datenschutzerklärung zu.')
    .label('Datenschutzerklärung'),
  nutzungsbedingungenAkzeptiert: yup
    .boolean()
    .oneOf([true], 'Bitte stimmen Sie den Nutzungsbedingungen zu.')
    .required('Bitte stimmen Sie den Nutzungsbedingungen zu.')
    .label('Nutzungsbedingungen'),
  weitereZustimmungAkzeptiert: yup
    .boolean()
    .oneOf([true], 'Bitte stimmen Sie zu.')
    .required('Bitte stimmen Sie zu.')
    .label('Weitere Zustimmung')
})
