import Vue from 'vue'
import store from '@/store'
import Router from 'vue-router'
import Home from './views/Home.vue'
import Login from './views/Login.vue'
import About from './views/About.vue'
import Register from './views/Register.vue'

Vue.use(Router)

const checkAuth = (to, from, next) => {
  let authRequired = to.matched.some(record => record.meta.requiresAuth)
  if (!store.getters.authenticated) {
    return store.dispatch('me').then((response) => {
      if (authRequired) {
        return response.authenticated
      }
      return true
    })
  }
  return Promise.resolve(true)
}

const checkPermissions = (to, from, next) => {
  if (to.matched.some(record => record.meta.requiresOwner)) {
    let user = store.getters.user
    return Promise.resolve(user.id === parseInt(to.params.id, 10))
  }
  return Promise.resolve(true)
}

let router = new Router({
  mode: 'history',
  routes: [
    {
      path: '/',
      name: 'home',
      component: Home
    },
    {
      path: '/about',
      name: 'about',
      component: About
    },
    { path: '/login', component: Login, name: 'login' },
    { path: '/register', component: Register, name: 'register' }
  ]
})

router.beforeEach((to, from, next) => {
  checkAuth(to, from, next).then((authenticated) => {
    if (authenticated) {
      return checkPermissions(to, from, next)
    }
    return Promise.reject(new Error('Unauthenticated'))
  }).then((authorized) => {
    if (authorized) {
      return next()
    }
    return Promise.reject(new Error('Unauthorized'))
  }).catch((err) => {
    next(err)
  })
})

router.onError((err) => {
  console.error(err)
  store.dispatch('showAlert', {
    type: 'alert-danger',
    message: err.message,
    title: 'ERROR!'
  })
})

export default router
