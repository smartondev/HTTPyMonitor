import {computed} from "vue";
import type {RequestLogUi} from "@/types/RequestLogUi";
import {RequestLogPhase} from "@/types/RequestLog";

export default function useRequestLogUi(model: RequestLogUi) {
    const variant_by_status = computed(() => {
        if (typeof model?.response?.status === 'number') {
            if (model.response.status >= 200 && model.response.status < 300) {
                return 'variant-2xx';
            } else if (model.response.status >= 300 && model.response.status < 400) {
                return 'variant-3xx';
            } else {
                return 'variant-4xx-5xx';
            }
        }
        return 'variant-xxx';
    });
    const variant_by_method = computed(() => {
        if (typeof model?.request?.method === 'string') {
            return `variant-${model.request.method.toLowerCase()}`;
        }
        return '';
    });


    return {
        variant_by_status,
        variant_by_method,
    }
}

export function phase2string(phase: RequestLogPhase): string {
    switch (phase) {
        case RequestLogPhase.END:
            return 'End';
        case RequestLogPhase.REQUEST_HEAD:
            return 'Request HEAD read';
        case RequestLogPhase.REQUEST_BODY_READING:
            return 'Request BODY reading';
        case RequestLogPhase.REQUEST_FORWARD:
            return 'Request FORWARD';
        case RequestLogPhase.RESPONSE_BODY_READING:
            return 'Response BODY reading';
        case RequestLogPhase.RESPONSE_BODY_READ:
            return 'Response BODY read';
        default:
            return 'Unknown';
    }
}