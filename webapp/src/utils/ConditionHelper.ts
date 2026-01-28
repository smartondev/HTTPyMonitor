export const isUndefined = (value: any): boolean => {
  return value === undefined
}

export const isNotUndefined = (value: any): boolean => {
  return !isUndefined(value)
}

export const isNull = (value: any): boolean => {
  return value === null
}

export const isNotNull = (value: any): boolean => {
  return !isNull(value)
}

export const isNullOrUndefined = (value: any): boolean => {
  return isUndefined(value) || isNull(value)
}

export const isNotNullNorUndefined = (value: any): boolean => {
  return !isNullOrUndefined(value)
}
