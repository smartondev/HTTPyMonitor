import {isNullOrUndefined} from "@/helpers/ConditionHelper";

export async function copyToClipboard(text: string | null | undefined, success: (() => void) | null = null, fail: (() => void) | null = null) {
    if (isNullOrUndefined(text)) {
        return
    }
    try {
        await navigator.clipboard.writeText(text ?? '');
        if (success) {
            success()
        }
    } catch {
        if (fail) {
            fail()
        }
    }
}