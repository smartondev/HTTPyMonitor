export const deepMerge = (target: any, source: any): void => {
  if (isObject(target) && isObject(source)) {
    Object.keys(source).forEach((key) => {
      if (isObject(source[key])) {
        if (!(key in target)) {
          target[key] = source[key]
        } else {
          deepMerge(target[key], source[key])
        }
      } else {
        target[key] = source[key]
      }
    })
  }
}

export const isObject = (item: any): boolean => {
  return item && typeof item === 'object' && !Array.isArray(item)
}
