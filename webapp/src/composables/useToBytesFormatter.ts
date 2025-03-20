import type { NullableString } from '@/types/Nullable'
import type { MaybeNumber } from '@/types/Maybe'

const sizeUnits = ['Bytes', 'KBytes', 'MBytes', 'GBytes', 'TBytes']
const unitStep = 1024

const useToBytesFormatter = (bytes: MaybeNumber): NullableString => {
  if (bytes === null || bytes === undefined) {
    return null
  }
  if (bytes < 0) {
    throw new Error('bytes must be greater than or equal to 0')
  }
  if (bytes === 0) {
    return '0 Byte'
  }
  const i = Math.floor(Math.log(bytes) / Math.log(unitStep))
  const fraction = i < 1 ? 0 : 1
  return `${(bytes / Math.pow(unitStep, i)).toFixed(fraction)} ${sizeUnits[i]}`
}

export default useToBytesFormatter
