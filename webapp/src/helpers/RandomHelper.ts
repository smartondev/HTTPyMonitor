export const randomBoolean = (): boolean => {
  return Math.random() >= 0.5
}

export const randomInt = (min: number, max: number): number => {
  return Math.floor(Math.random() * (max - min + 1)) + min
}
