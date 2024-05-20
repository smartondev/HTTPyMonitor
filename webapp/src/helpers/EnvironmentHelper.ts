export function isDevEnvironment(): boolean {
    return import.meta.env.VITE_APP_ENVIRONMENT === 'development';
}

export function isProdEnvironment(): boolean {
    return import.meta.env.VITE_APP_ENVIRONMENT === 'production';
}

export function getDownloadUrlPrefix(): string {
    return import.meta.env.VITE_APP_DOWNLOAD_URL_PREFIX;
}

export function getWsUrl(): string {
    let url = import.meta.env.VITE_APP_WS_URL;
    if (url.startsWith('/')) {
        url = `${(window.location.protocol === 'https:' ? 'wss:' : 'ws:')}//${window.location.host}${url}`;
    }
    console.log(url)
    return url;
}

export function getAppVersion(): string {
    return import.meta.env.VITE_APP_VERSION;
}


