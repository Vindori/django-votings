import Vue from 'vue'
import Router from 'vue-router'
import App from '@/App.vue'

Vue.use(Router);

export default new Router({
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
