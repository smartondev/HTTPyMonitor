import type {Ref} from 'vue'
import {computed, onMounted, onUnmounted, ref, watch} from "vue";

export default function useElapsedTimer(startTimestamp: number, endTimestamp: Ref<number | null>, stepMs: number = 200) {
    const endTimestampRef = ref<number>(endTimestamp.value ?? (new Date().getTime() / 1000))

    let timer: ReturnType<typeof setInterval> | null = null;

    const clearTimer = function () {
        if (timer === null) {
            return;
        }
        clearInterval(timer)
    }

    const startTimer = function () {
        clearTimer();
        timer = setInterval(() => {
            if (null !== endTimestamp.value) {
                endTimestampRef.value = endTimestamp.value ?? 0;
                return;
            }
            endTimestampRef.value = new Date().getTime() / 1000
        }, stepMs);
    }

    onMounted(() => {
        if (endTimestamp.value) {
            return;
        }
        startTimer()
    });
    watch(endTimestampRef, () => {
        if (endTimestamp.value) {
            clearTimer();
        } else {
            startTimer();
        }
    });
    onUnmounted(() => {
        clearTimer()
    });

    const diff = computed(() => {
        return endTimestampRef.value - startTimestamp
    });

    return {
        diff,
    }
}