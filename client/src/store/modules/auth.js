import api from '@/api'
import router from '@/router'
import {
  SUCCESS_LOGIN,
  SUCCESS_LOGOUT,
  UPDATE_ARTIST_PROFILE,
  UPDATE_USER
} from '../types'

const state = {
  user: null,
  authenticated: false
}

const getters = {
  user: state => state.user,
  authenticated: state => state.authenticated,
  profile: state => (state.user ? state.user.profile : {})
}

const actions = {
  login: ({ dispatch, commit }, data) => {
    return api.login(data).then((response) => {
      commit(SUCCESS_LOGIN, response.data)
      router.push('feed')
    }, (response) => {
      dispatch('setErrors', response.body.error, {root: true})
      dispatch('showAlert', {
        type: 'alert-danger',
        message: 'Login Failed!',
        title: 'Failure!'
      }, {root: true})
    })
  },
  logout: ({ dispatch, commit }) => {
    return api.logout().then()
      .finally((e) => {
        commit(SUCCESS_LOGOUT, {})
        router.push('/login')
      })
  },
  me: ({ dispatch, commit }) => {
    return api.getMe().then((response) => {
      commit(SUCCESS_LOGIN, response.data)
      return response.data
    }, (response) => {
      commit(SUCCESS_LOGIN, response.data)
      return response.data
    })
  },
  updateProfile: ({commit}, data) => {
    commit('UPDATE_ARTIST_PROFILE', data)
  },
  updateUser: ({commit}, data) => {
    commit('UPDATE_USER', data)
  },
  patchProfile: ({ dispatch, commit }, data) => {
    let {userId, profile} = data
    api.patchProfile(userId, {profile}).then((response) => {
      dispatch('showAlert', {
        type: 'alert-success',
        message: 'Update Profile Succeeded!',
        title: 'Success!'
      }, {root: true})
      dispatch('updateUser', {user: response.body})
      dispatch('clearErrors', null, {root: true})
      router.push('feed')
    }, (response) => {
      dispatch('setErrors', response.body.error, {root: true})
      dispatch('showAlert', {
        type: 'alert-danger',
        message: 'Update Profile Failed!',
        title: 'Failure!'
      }, {root: true})
    })
  }

}

const mutations = {
  [UPDATE_USER] (state, data) {
    let {user, authenticated} = data
    state.user = user
    state.authenticated = authenticated
  },
  [SUCCESS_LOGIN] (state, data) {
    let {user, authenticated} = data
    state.user = user
    state.authenticated = authenticated
  },
  [SUCCESS_LOGOUT] (state, data) {
    state.user = null
    state.authenticated = false
  },
  [UPDATE_ARTIST_PROFILE] (state, profile) {
    state.user.profile = Object.assign({}, state.user.profile, profile)
  }
}

export default {
  state,
  getters,
  actions,
  mutations
}
