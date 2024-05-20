import "bootstrap/dist/css/bootstrap.min.css"
import "bootstrap"
import "bootstrap-icons/font/bootstrap-icons.css"
import './assets/main.scss'

import {createApp} from 'vue'
import App from './App.vue'
import router from './router'
import {createClient} from "@/services/RemoteWs";
import {createProvides} from "@/provides";
import {getWsUrl} from "@/helpers/EnvironmentHelper";

const app = createApp(App)
app.use(router)
createProvides(app)
const remoteWsClient = createClient(getWsUrl())
remoteWsClient.connect();
app.provide('remoteWsClient', remoteWsClient)

app.mount('#app')

