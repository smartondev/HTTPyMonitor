/// <reference types="vite/client" />

interface ImportMetaEnv {
  readonly VITE_APP_ENVIRONMENT: string;
  readonly VITE_APP_DOWNLOAD_URL_PREFIX: string;
  readonly VITE_APP_WS_URL: string;
  readonly VITE_APP_VERSION: string;
}

interface ImportMeta {
  readonly env: ImportMetaEnv;
}