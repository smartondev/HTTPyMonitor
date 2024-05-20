

export function deepMerge(target: any, source: any) {
  if (isObject(target) && isObject(source)) {
    Object.keys(source).forEach(key => {
      if (isObject(source[key])) {
        if (!(key in target)) {
          target[key] = source[key];
        } else {
          deepMerge(target[key], source[key]);
        }
      } else {
        target[key] = source[key];
      }
    });
  }
}
function isObject(item: any) {
  return (item && typeof item === 'object' && !Array.isArray(item));
}