export const toCamelCase = (e) => {
  return e.replace(/_([a-z])/g, (g) => g[1].toUpperCase())
}

export const toSnakeCase = (str) => {
  return (
    str &&
    str
      .match(/[A-Z]{2,}(?=[A-Z][a-z]+[0-9]*|\b)|[A-Z]?[a-z]+[0-9]*|[A-Z]|[0-9]+/g)
      .map((x) => x.toLowerCase())
      .join('_')
  )
}
