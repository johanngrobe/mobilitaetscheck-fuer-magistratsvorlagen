export const parseStringtoDate = (value) => {
  if (value) {
    const date = new Date(value)
    return new Date(Date.UTC(date.getFullYear(), date.getMonth(), date.getDate()))
  }
  return value
}
