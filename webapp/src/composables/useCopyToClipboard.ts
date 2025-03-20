import { isNullOrUndefined } from '@/helpers/ConditionHelper'
import type { MaybeString } from '@/types/Maybe'
import type { Nullable } from '@/types/Nullable'

const useCopyToClipboard = async (
  text: MaybeString,
  success: Nullable<() => void> = null,
  fail: Nullable<() => void> = null
) => {
  if (isNullOrUndefined(text)) {
    return
  }
  try {
    await navigator.clipboard.writeText(text ?? '')
    if (success) {
      success()
    }
  } catch {
    if (fail) {
      fail()
    }
  }
}

export default useCopyToClipboard
