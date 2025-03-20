import 'bootstrap/scss/bootstrap.scss'
import 'bootstrap-icons/font/bootstrap-icons.css'
import './assets/main.scss'

import '../vite-env.d.ts'
import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import { useWsClient } from '@/composables/useRemoteWs'
import { createProvides } from '@/provides'
import { getWsUrl } from '@/helpers/EnvironmentHelper'

const app = createApp(App)
app.use(router)
createProvides(app)
const remoteWsClient = useWsClient(getWsUrl())
remoteWsClient.connect()
app.provide('remoteWsClient', remoteWsClient)

app.mount('#app')
