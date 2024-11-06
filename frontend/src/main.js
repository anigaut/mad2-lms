// import './assets/main.css'

import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import axios from 'axios'
import ToastPlugin from 'vue-toast-notification';
import 'vue-toast-notification/dist/theme-bootstrap.css';

axios.defaults.baseURL = 'http://127.0.0.1:5000/api/';
axios.defaults.headers.common["Authorization"] = `Bearer ${localStorage.getItem("accessToken")}`;

const app = createApp(App)

app.use(router)
app.use(ToastPlugin);
app.mount('#app')
