export const isDevEnvironment = (): boolean => {
  return import.meta.env.VITE_APP_ENVIRONMENT === 'development'
}

export const isProdEnvironment = (): boolean => {
  return import.meta.env.VITE_APP_ENVIRONMENT === 'production'
}

export const getDownloadUrlPrefix = (): string => {
  return import.meta.env.VITE_APP_DOWNLOAD_URL_PREFIX
}

export const getWsUrl = (): string => {
  let url = import.meta.env.VITE_APP_WS_URL
  if (url.startsWith('/')) {
    url = `${window.location.protocol === 'https:' ? 'wss:' : 'ws:'}//${window.location.host}${url}`
  }
  return url
}

export const getAppVersion = (): string => {
  return import.meta.env.VITE_APP_VERSION
}
