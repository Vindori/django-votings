import Vue from 'vue'
import App from './App'
import { apiUrl } from '@/config';
import axios from 'axios';
import VueFlashMessage from 'vue-flash-message';
import VModal from 'vue-js-modal'
import FixedHeader from 'vue-fixed-header'
import VueApexCharts from 'vue-apexcharts';
import VueRouter from 'vue-router'

 
require('vue-flash-message/dist/vue-flash-message.min.css');

axios.defaults.baseURL = apiUrl;
axios.defaults.withCredentials = true;

Vue.prototype.$http = axios;
Vue.config.productionTip = false;

Vue.use(VueFlashMessage);
Vue.use(VModal);
Vue.use(VueRouter);

var router = new VueRouter({
    routes: [
        {
            path: '/',
            name: 'Main',
            component: App
        },
        {
            path: '/:id',
            name: 'ShowPoll',
            component: App
        }
    ]
})

Vue.component('fixed-header', FixedHeader);
Vue.component('apexchart', VueApexCharts);

new Vue({
  router,
  el: '#app',
  components: { App },
  template: '<App/>'
});
