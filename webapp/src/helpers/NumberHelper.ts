export function toBytes(bytes: number | null | undefined): string | null {
    if (bytes === null || bytes === undefined) {
        return null;
    }
    if (bytes === 0) {
        return '0 Byte';
    }
    const sizes = ['Bytes', 'KBytes', 'MBytes', 'GBytes', 'TBytes'];
    const step = 1024;
    const i = Math.floor(Math.log(bytes) / Math.log(step));
    const fraction = i < 1 ? 0 : 1;
    return `${(bytes / Math.pow(step, i)).toFixed(fraction)} ${sizes[i]}`;
}

