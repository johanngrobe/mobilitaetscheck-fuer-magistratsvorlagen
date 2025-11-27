/**
 * Transformation function to set a field to null if `carsharingFaktor` is null.
 *
 * @param {any} value - The current value of the field being transformed.
 * @param {any} originalValue - The original value before transformation.
 * @param {Object} context - The Yup transformation context.
 * @returns {any} - Returns `null` if `carsharingFaktor` is null; otherwise, returns the value.
 */
export function setToNull(value, originalValue, context) {
  if (context.parent.carsharingFaktor === null) {
    return null // Automatically set to null if carsharingFaktor is null
  }
  return value
}

export function parseDate(value, originalValue) {
  if (originalValue) {
    const date = new Date(originalValue)
    return new Date(Date.UTC(date.getFullYear(), date.getMonth(), date.getDate()))
  }
  return value
}
