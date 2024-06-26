export function randomBoolean(): boolean {
    return Math.random() >= 0.5;
}

export function randomInt(min: number, max: number): number {
    return Math.floor(Math.random() * (max - min + 1)) + min;
}