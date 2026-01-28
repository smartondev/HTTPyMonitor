import 'bootstrap/scss/bootstrap.scss'
import 'bootstrap-icons/font/bootstrap-icons.css'
import './assets/main.scss'

import '../vite-env.d.ts'
import {createApp} from 'vue'
import App from './App.vue'
import router from './router'
import {wsClient} from '@/utils/wsClient'
import {createProvides} from '@/provides'
import {getWsUrl} from '@/utils/EnvironmentHelper'

const app = createApp(App)
app.use(router)
createProvides(app)
const remoteWsClient = wsClient(getWsUrl())
remoteWsClient.connect()

app.mount('#app')
