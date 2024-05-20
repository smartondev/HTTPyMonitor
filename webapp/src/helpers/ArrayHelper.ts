export function findLastIndexOf<T>(array: T[], predicate: (value: T) => boolean, indexFrom?: number | null): number {
    for (let i = indexFrom ?? (array.length - 1); i >= 0; i--) {
        if (predicate(array[i])) {
            return i;
        }
    }
    return -1;
}