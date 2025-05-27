import { createApp } from 'vue'
import './style.css'
import App from './App.vue'
import ArcoVue from '@arco-design/web-vue'
import '@arco-design/web-vue/dist/arco.css'
// 导入图标库
import { IconSearch, IconArrowLeft, IconPlus } from '@arco-design/web-vue/es/icon'

const app = createApp(App)
app.use(ArcoVue)
// 全局注册图标
app.component('IconSearch', IconSearch)
app.component('IconArrowLeft', IconArrowLeft)
app.component('IconPlus', IconPlus)
app.mount('#app')
