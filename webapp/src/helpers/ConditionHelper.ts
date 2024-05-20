export function isUndefined(value: any): boolean {
    return value === undefined;
}

export function isNotUndefined(value: any): boolean {
    return !isUndefined(value);
}

export function isNull(value: any): boolean {
    return value === null;
}

export function isNotNull(value: any): boolean {
    return !isNull(value);
}

export function isNullOrUndefined(value: any): boolean {
    return isUndefined(value) || isNull(value);
}

export function isNotNullNorUndefined(value: any): boolean {
    return !isNullOrUndefined(value);
}