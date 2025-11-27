import * as yup from 'yup'

export const schema = yup.object({
  email: yup
    .string()
    .required('E-Mail ist erforderlich')
    .email('Ungültige E-Mail-Adresse')
    .label('E-Mail'),
  vorname: yup.string().required('Vorname ist erforderlich').label('Vorname'),
  nachname: yup.string().required('Nachname ist erforderlich').label('Nachname'),
  gemeindeId: yup.number().required('Gemeinde ist erforderlich').label('Gemeinde'),
  rolleId: yup.number().required('Rolle ist erforderlich').label('Rolle')
})
